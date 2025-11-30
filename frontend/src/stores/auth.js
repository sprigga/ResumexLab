import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(username, password) {
    try {
      const response = await authAPI.login(username, password)
      token.value = response.data.access_token
      localStorage.setItem('token', token.value)

      // Verify and get user info
      await verifyToken()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  async function verifyToken() {
    try {
      const response = await authAPI.verify()
      user.value = response.data
      return true
    } catch (error) {
      logout()
      throw error
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    verifyToken,
    logout,
  }
})
