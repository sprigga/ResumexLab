import { defineStore } from 'pinia'
import { ref } from 'vue'
import { resumeAPI } from '@/api/resume'
import { createEntityActions, createAsyncAction } from './crudFactory'

export const useResumeStore = defineStore('resume', () => {
  // State
  const personalInfo = ref(null)
  const workExperiences = ref([])
  const projects = ref([])
  const education = ref([])
  const certifications = ref([])
  const languages = ref([])
  const publications = ref([])
  const githubProjects = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Personal Info (custom: no list, special update pattern)
  async function fetchPersonalInfo() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getPersonalInfo()
      personalInfo.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updatePersonalInfo(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updatePersonalInfo(data)
      personalInfo.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Entity CRUD actions generated via factory
  const weActions = createEntityActions(workExperiences, loading, error, {
    getAll: resumeAPI.getWorkExperiences,
    create: resumeAPI.createWorkExperience,
    update: resumeAPI.updateWorkExperience,
    delete: resumeAPI.deleteWorkExperience,
  })

  const projActions = createEntityActions(projects, loading, error, {
    getAll: resumeAPI.getProjects,
    create: resumeAPI.createProject,
    update: resumeAPI.updateProject,
    delete: resumeAPI.deleteProject,
  })

  const eduActions = createEntityActions(education, loading, error, {
    getAll: resumeAPI.getEducation,
    create: resumeAPI.createEducation,
    update: resumeAPI.updateEducation,
    delete: resumeAPI.deleteEducation,
  })

  const certActions = createEntityActions(certifications, loading, error, {
    getAll: resumeAPI.getCertifications,
    create: resumeAPI.createCertification,
    update: resumeAPI.updateCertification,
    delete: resumeAPI.deleteCertification,
  })

  const langActions = createEntityActions(languages, loading, error, {
    getAll: resumeAPI.getLanguages,
    create: resumeAPI.createLanguage,
    update: resumeAPI.updateLanguage,
    delete: resumeAPI.deleteLanguage,
  })

  const pubActions = createEntityActions(publications, loading, error, {
    getAll: resumeAPI.getPublications,
    create: resumeAPI.createPublication,
    update: resumeAPI.updatePublication,
    delete: resumeAPI.deletePublication,
  })

  const ghActions = createEntityActions(githubProjects, loading, error, {
    getAll: resumeAPI.getGithubProjects,
    create: resumeAPI.createGithubProject,
    update: resumeAPI.updateGithubProject,
    delete: resumeAPI.deleteGithubProject,
  })

  // Project attachment name (special PATCH operation)
  async function updateProjectAttachmentName(id, attachmentName) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updateProjectAttachmentName(id, attachmentName)
      const index = projects.value.findIndex(p => p.id === id)
      if (index !== -1) {
        projects.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Import/Export actions (one-off, no list management)
  const importPdf = createAsyncAction(loading, error, resumeAPI.importPdf.bind(resumeAPI))
  const importResumeData = createAsyncAction(loading, error, resumeAPI.importResumeData)
  const createDatabase = createAsyncAction(loading, error, resumeAPI.createDatabase)
  // exportDatabase returns the full response (blob), not response.data
  async function exportDatabase() {
    loading.value = true
    error.value = null
    try {
      return await resumeAPI.exportDatabase()
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  const importDatabase = createAsyncAction(loading, error, resumeAPI.importDatabase.bind(resumeAPI))

  return {
    // State
    personalInfo,
    workExperiences,
    projects,
    education,
    certifications,
    languages,
    publications,
    githubProjects,
    loading,
    error,

    // Personal Info
    fetchPersonalInfo,
    updatePersonalInfo,

    // Work Experience (named aliases for backward compatibility)
    fetchWorkExperiences: weActions.fetchAll,
    createWorkExperience: weActions.create,
    updateWorkExperience: weActions.update,
    deleteWorkExperience: weActions.remove,

    // Projects
    fetchProjects: projActions.fetchAll,
    createProject: projActions.create,
    updateProject: projActions.update,
    deleteProject: projActions.remove,
    updateProjectAttachmentName,

    // Education
    fetchEducation: eduActions.fetchAll,
    createEducation: eduActions.create,
    updateEducation: eduActions.update,
    deleteEducation: eduActions.remove,

    // Certifications
    fetchCertifications: certActions.fetchAll,
    createCertification: certActions.create,
    updateCertification: certActions.update,
    deleteCertification: certActions.remove,

    // Languages
    fetchLanguages: langActions.fetchAll,
    createLanguage: langActions.create,
    updateLanguage: langActions.update,
    deleteLanguage: langActions.remove,

    // Publications
    fetchPublications: pubActions.fetchAll,
    createPublication: pubActions.create,
    updatePublication: pubActions.update,
    deletePublication: pubActions.remove,

    // GitHub Projects
    fetchGithubProjects: ghActions.fetchAll,
    createGithubProject: ghActions.create,
    updateGithubProject: ghActions.update,
    deleteGithubProject: ghActions.remove,

    // Import/Export
    importPdf,
    importResumeData,
    createDatabase,
    exportDatabase,
    importDatabase,
  }
})
