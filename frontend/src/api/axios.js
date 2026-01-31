import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,  // 30 秒（原本 10 秒）- 優化於 2025-01-31 for GCP e2-micro
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors and retries
// 修改於 2025-01-31: 加入自動重試機制for timeout 和 5xx 錯誤
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const config = error.config

    // 逾時或 5xx 錯誤時重試（最多 2 次）
    if (!config.__retryCount &&
        (error.code === 'ECONNABORTED' || error.response?.status >= 500)) {
      config.__retryCount = config.__retryCount || 0
      if (config.__retryCount < 2) {
        config.__retryCount += 1
        await new Promise(resolve => setTimeout(resolve, 1000))  // 等待 1 秒後重試
        return apiClient(config)
      }
    }

    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token')
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
