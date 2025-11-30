<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  ElMessage.success(t('auth.logoutSuccess'))
  router.push('/admin/login')
}

// 已修改於 2025-11-30，原因：新增各類履歷資料管理選單項目
const menuItems = [
  { path: '/admin/dashboard', label: 'Dashboard', icon: 'Odometer' },
  { path: '/admin/personal-info', label: 'Personal Info', icon: 'User' },
  { path: '/admin/work-experience', label: 'Work Experience', icon: 'Briefcase' },
  { path: '/admin/projects', label: 'Projects', icon: 'Management' },
  { path: '/admin/education', label: 'Education', icon: 'School' },
  { path: '/admin/certifications', label: 'Certifications', icon: 'Medal' },
  { path: '/admin/publications', label: 'Publications', icon: 'Reading' },
  // 已新增於 2025-11-30，原因：新增 GitHub 專案管理選單項目
  { path: '/admin/github-projects', label: 'GitHub Projects', icon: 'Link' },
  { path: '/admin/import-data', label: 'Import Data', icon: 'Upload' },
]
</script>

<template>
  <el-container class="admin-layout">
    <el-aside width="200px">
      <div class="logo">
        <h2>Admin</h2>
      </div>
      <el-menu
        :default-active="route.path"
        router
        class="el-menu-vertical"
      >
        <el-menu-item
          v-for="item in menuItems"
          :key="item.path"
          :index="item.path"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>
        <div class="header-content">
          <h3>Resume Management System</h3>
          <div class="header-actions">
            <el-button text @click="router.push('/')">
              View Resume
            </el-button>
            <el-button type="danger" @click="handleLogout">
              {{ t('nav.logout') }}
            </el-button>
          </div>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
/* Applying global styles from style.css */
.admin-layout {
  height: 100vh;
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #263445;
}

.logo h2 {
  margin: 0;
  color: #fff;
  font-size: 3.2em;
  line-height: 1.1;
}

.el-menu-vertical {
  border: none;
  background-color: #304156;
}

:deep(.el-menu-item) {
  color: #bfcbd9;
}

:deep(.el-menu-item:hover),
:deep(.el-menu-item.is-active) {
  background-color: #263445 !important;
  color: #646cff !important;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h3 {
  margin: 0;
  color: #2c3e50;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.el-main {
  /* Original background - commented out on 2025-11-29 */
  /* Reason: Applying gradient background style from style.css */
  /* background-color: #f0f2f5; */

  /* New gradient background from black to deep blue to gray */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%);
  padding: 20px;
  position: relative;
}

/* Vignette effect for main content area */
.el-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  box-shadow: inset 0 0 150px rgba(0, 0, 0, 0.4);
  z-index: 0;
}

/* Ensure content is above vignette */
.el-main > * {
  position: relative;
  z-index: 1;
}

/* Button styles from style.css */
:deep(.el-button) {
  border-radius: 8px;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
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

/* Light mode specific styles */
@media (prefers-color-scheme: light) {
  .header-content h3 {
    color: #213547;
  }

  .el-main {
    /* Light mode: use light gray background instead of gradient */
    background: #f0f2f5;
  }

  .el-main::before {
    /* Remove vignette in light mode */
    display: none;
  }

  :deep(.el-menu-item:hover),
  :deep(.el-menu-item.is-active) {
    color: #747bff !important;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
