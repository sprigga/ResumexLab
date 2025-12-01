import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/ResumeView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/test-api',
    name: 'TestAPI',
    component: () => import('@/components/APITestComponent.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/admin/login',
    name: 'Login',
    component: () => import('@/views/admin/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/admin',
    // 原本設定 (已註解於 2025-11-30，原因：修復 Vue Router 警告 - 父路由不應有名稱，空路徑子路由應有名稱)
    // name: 'Admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Admin',
        redirect: '/admin/dashboard',
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/admin/DashboardView.vue'),
      },
      {
        path: 'personal-info',
        name: 'PersonalInfo',
        component: () => import('@/views/admin/PersonalInfoEdit.vue'),
      },
      {
        path: 'work-experience',
        name: 'WorkExperience',
        component: () => import('@/views/admin/WorkExperienceEdit.vue'),
      },
      // 已新增於 2025-11-30，原因：新增專案管理路由
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/admin/ProjectEdit.vue'),
      },
      // 已新增於 2025-11-30，原因：新增教育背景管理路由
      {
        path: 'education',
        name: 'Education',
        component: () => import('@/views/admin/EducationEdit.vue'),
      },
      // 已新增於 2025-11-30，原因：新增證照與語言管理路由
      {
        path: 'certifications',
        name: 'Certifications',
        component: () => import('@/views/admin/CertificationEdit.vue'),
      },
      // 已新增於 2025-11-30，原因：新增學術著作管理路由
      {
        path: 'publications',
        name: 'Publications',
        component: () => import('@/views/admin/PublicationEdit.vue'),
      },
      // 已新增於 2025-11-30，原因：新增 GitHub 專案管理路由
      {
        path: 'github-projects',
        name: 'GithubProjects',
        component: () => import('@/views/admin/GithubProjectEdit.vue'),
      },
      // 已新增於 2025-11-30，原因：新增匯入履歷資料管理路由
      {
        path: 'import-data',
        name: 'ImportData',
        component: () => import('@/views/admin/ImportDataView.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/admin/login')
  } else if (to.path === '/admin/login' && authStore.isAuthenticated) {
    next('/admin/dashboard')
  } else {
    next()
  }
})

export default router
