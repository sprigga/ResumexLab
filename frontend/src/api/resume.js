import apiClient from './axios'
import { createCrudApi } from './createCrudApi'

// Entity CRUD APIs generated via factory
const workExperienceApi = createCrudApi('work-experience')
const projectsApi = createCrudApi('projects')
const educationApi = createCrudApi('education')
const certificationsApi = createCrudApi('certifications')
const languagesApi = createCrudApi('languages')
const publicationsApi = createCrudApi('publications')
const githubProjectsApi = createCrudApi('github-projects')

export const resumeAPI = {
  // Personal Info (custom: no list/delete)
  getPersonalInfo: () => apiClient.get('/personal-info/'),
  updatePersonalInfo: (data) => apiClient.put('/personal-info/', data),

  // Work Experience
  getWorkExperiences: () => workExperienceApi.getAll(),
  getWorkExperience: (id) => workExperienceApi.get(id),
  createWorkExperience: (data) => workExperienceApi.create(data),
  updateWorkExperience: (id, data) => workExperienceApi.update(id, data),
  deleteWorkExperience: (id) => workExperienceApi.delete(id),

  // Projects
  getProjects: () => projectsApi.getAll(),
  getProject: (id) => projectsApi.get(id),
  createProject: (data) => projectsApi.create(data),
  updateProject: (id, data) => projectsApi.update(id, data),
  deleteProject: (id) => projectsApi.delete(id),
  updateProjectAttachmentName: (id, attachmentName) =>
    apiClient.patch(`/projects/${id}/attachment-name`, { attachment_name: attachmentName }),

  // Education
  getEducation: () => educationApi.getAll(),
  createEducation: (data) => educationApi.create(data),
  updateEducation: (id, data) => educationApi.update(id, data),
  deleteEducation: (id) => educationApi.delete(id),

  // Certifications
  getCertifications: () => certificationsApi.getAll(),
  createCertification: (data) => certificationsApi.create(data),
  updateCertification: (id, data) => certificationsApi.update(id, data),
  deleteCertification: (id) => certificationsApi.delete(id),

  // Languages
  getLanguages: () => languagesApi.getAll(),
  createLanguage: (data) => languagesApi.create(data),
  updateLanguage: (id, data) => languagesApi.update(id, data),
  deleteLanguage: (id) => languagesApi.delete(id),

  // Publications
  getPublications: () => publicationsApi.getAll(),
  createPublication: (data) => publicationsApi.create(data),
  updatePublication: (id, data) => publicationsApi.update(id, data),
  deletePublication: (id) => publicationsApi.delete(id),

  // GitHub Projects
  getGithubProjects: () => githubProjectsApi.getAll(),
  createGithubProject: (data) => githubProjectsApi.create(data),
  updateGithubProject: (id, data) => githubProjectsApi.update(id, data),
  deleteGithubProject: (id) => githubProjectsApi.delete(id),

  // Import / Export (special: FormData or blob responses)
  importPdf(file, importType = 'pdf_extraction') {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('import_type', importType)
    return apiClient.post('/import/pdf/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  importResumeData: () => apiClient.post('/import/resume-data/'),
  createDatabase: () => apiClient.post('/import/database/'),
  exportDatabase: () => apiClient.get('/import/database/export/', { responseType: 'blob' }),
  importDatabase(file) {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/import/database/import/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
}
