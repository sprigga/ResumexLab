<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

const loginForm = ref({
  username: '',
  password: '',
})

const loading = ref(false)

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('Please enter username and password')
    return
  }

  loading.value = true
  try {
    await authStore.login(loginForm.value.username, loginForm.value.password)
    ElMessage.success(t('auth.loginSuccess'))
    router.push('/admin/dashboard')
  } catch (error) {
    ElMessage.error(t('auth.loginFailed'))
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>{{ t('auth.login') }}</h2>
        </div>
      </template>

      <el-form :model="loginForm" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input
            v-model="loginForm.username"
            :placeholder="t('auth.username')"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="loginForm.password"
            type="password"
            :placeholder="t('auth.password')"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%"
          >
            {{ t('auth.login') }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="footer">
        <el-link type="primary" @click="router.push('/')">
          {{ t('nav.resume') }}
        </el-link>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
/* Applying global styles from style.css */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  /* Original gradient - commented out on 2025-11-29 */
  /* Reason: Applying consistent gradient background style from style.css */
  /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */

  /* New gradient background from black to deep blue to gray */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%);
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: relative;
}

/* Vignette effect - subtle inner shadow */
.login-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  box-shadow: inset 0 0 200px rgba(0, 0, 0, 0.5);
  z-index: 0;
}

/* Ensure content is above vignette */
.login-container > * {
  position: relative;
  z-index: 1;
}

.login-card {
  width: 400px;
  max-width: 90%;
  padding: 2em;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.card-header h2 {
  margin: 0;
  text-align: center;
  color: #2c3e50;
  font-size: 3.2em;
  line-height: 1.1;
}

.footer {
  text-align: center;
  margin-top: 20px;
}

/* Button styles from style.css */
:deep(.el-button) {
  border-radius: 8px;
  font-family: inherit;
  cursor: pointer;
  transition: border-color 0.25s;
}

:deep(.el-button:hover) {
  border-color: #646cff;
}

:deep(.el-button:focus),
:deep(.el-button:focus-visible) {
  outline: 4px auto -webkit-focus-ring-color;
}

/* Link styles from style.css */
:deep(.el-link) {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}

:deep(.el-link:hover) {
  color: #535bf2;
}

@media (prefers-color-scheme: light) {
  .login-container {
    /* Light mode: use white background instead of gradient */
    background: #ffffff;
  }

  .login-container::before {
    /* Remove vignette in light mode */
    display: none;
  }

  .login-card {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }

  :deep(.el-link:hover) {
    color: #747bff;
  }
}
</style>
