import apiClient from './axios'

export const resumeAPI = {
  // Personal Info
  // 已修改於 2025-11-29，原因：FastAPI 路由使用尾部斜線
  getPersonalInfo() {
    return apiClient.get('/personal-info/')
  },

  updatePersonalInfo(data) {
    return apiClient.put('/personal-info/', data)
  },

  // Work Experience
  getWorkExperiences() {
    return apiClient.get('/work-experience/')
  },

  getWorkExperience(id) {
    return apiClient.get(`/work-experience/${id}`)
  },

  createWorkExperience(data) {
    return apiClient.post('/work-experience/', data)
  },

  updateWorkExperience(id, data) {
    return apiClient.put(`/work-experience/${id}`, data)
  },

  deleteWorkExperience(id) {
    return apiClient.delete(`/work-experience/${id}`)
  },

  // Projects
  // 已新增於 2025-11-30，原因：新增專案管理功能
  getProjects() {
    return apiClient.get('/projects/')
  },

  getProject(id) {
    return apiClient.get(`/projects/${id}`)
  },

  createProject(data) {
    return apiClient.post('/projects/', data)
  },

  updateProject(id, data) {
    return apiClient.put(`/projects/${id}`, data)
  },

  deleteProject(id) {
    return apiClient.delete(`/projects/${id}`)
  },

  // Education
  // 已新增於 2025-11-30，原因：新增教育背景管理功能
  getEducation() {
    return apiClient.get('/education/')
  },

  createEducation(data) {
    return apiClient.post('/education/', data)
  },

  updateEducation(id, data) {
    return apiClient.put(`/education/${id}`, data)
  },

  deleteEducation(id) {
    return apiClient.delete(`/education/${id}`)
  },

  // Certifications
  // 已新增於 2025-11-30，原因：新增證照管理功能
  getCertifications() {
    return apiClient.get('/certifications/')
  },

  createCertification(data) {
    return apiClient.post('/certifications/', data)
  },

  updateCertification(id, data) {
    return apiClient.put(`/certifications/${id}`, data)
  },

  deleteCertification(id) {
    return apiClient.delete(`/certifications/${id}`)
  },

  // Languages
  // 已新增於 2025-11-30，原因：新增語言能力管理功能
  getLanguages() {
    return apiClient.get('/languages/')
  },

  createLanguage(data) {
    return apiClient.post('/languages/', data)
  },

  updateLanguage(id, data) {
    return apiClient.put(`/languages/${id}`, data)
  },

  deleteLanguage(id) {
    return apiClient.delete(`/languages/${id}`)
  },

  // Publications
  // 已新增於 2025-11-30，原因：新增學術著作管理功能
  getPublications() {
    return apiClient.get('/publications/')
  },

  createPublication(data) {
    return apiClient.post('/publications/', data)
  },

  updatePublication(id, data) {
    return apiClient.put(`/publications/${id}`, data)
  },

  deletePublication(id) {
    return apiClient.delete(`/publications/${id}`)
  },

  // GitHub Projects
  // 已新增於 2025-11-30，原因：新增 GitHub 專案管理功能
  getGithubProjects() {
    return apiClient.get('/github-projects/')
  },

  createGithubProject(data) {
    return apiClient.post('/github-projects/', data)
  },

  updateGithubProject(id, data) {
    return apiClient.put(`/github-projects/${id}`, data)
  },

  deleteGithubProject(id) {
    return apiClient.delete(`/github-projects/${id}`)
  },
}
