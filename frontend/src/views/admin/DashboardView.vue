<script setup>
import { ref } from 'vue'

const stats = ref([
  { title: 'Personal Info', value: '1', icon: 'User', color: '#409eff' },
  { title: 'Work Experience', value: '0', icon: 'Briefcase', color: '#67c23a' },
  { title: 'Education', value: '0', icon: 'School', color: '#e6a23c' },
  { title: 'Projects', value: '0', icon: 'Document', color: '#f56c6c' },
])
</script>

<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :sm="12" :md="6" v-for="stat in stats" :key="stat.title">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.color }">
              <el-icon size="30"><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ stat.value }}</p>
              <p class="stat-title">{{ stat.title }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Quick Actions</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/admin/personal-info')">
              Edit Personal Info
            </el-button>
            <el-button type="success" @click="$router.push('/admin/work-experience')">
              Manage Work Experience
            </el-button>
            <el-button @click="$router.push('/')">
              View Resume
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
/* Applying global styles from style.css */
.dashboard {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.dashboard h1 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 3.2em;
  line-height: 1.1;
}

.stat-card {
  margin-bottom: 20px;
  padding: 2em;
}

/* Card styles with transparency for gradient background */
:deep(.el-card) {
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
  color: #2c3e50;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin: 5px 0 0 0;
}

.quick-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
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
  .dashboard h1,
  .stat-value {
    color: #213547;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
