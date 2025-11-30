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
    path: '/admin/login',
    name: 'Login',
    component: () => import('@/views/admin/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
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
