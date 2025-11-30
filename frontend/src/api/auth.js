import apiClient from './axios'

export const authAPI = {
  // Login
  login(username, password) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    return apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Verify token
  verify() {
    return apiClient.get('/auth/verify')
  },

  // Logout
  logout() {
    return apiClient.post('/auth/logout')
  },
}
