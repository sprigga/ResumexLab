import { defineStore } from 'pinia'
import { ref } from 'vue'
import { resumeAPI } from '@/api/resume'

export const useResumeStore = defineStore('resume', () => {
  const personalInfo = ref(null)
  const workExperiences = ref([])
  // 已新增於 2025-11-30，原因：新增各類履歷資料的狀態管理
  const projects = ref([])
  const education = ref([])
  const certifications = ref([])
  const languages = ref([])
  const publications = ref([])
  const githubProjects = ref([])
  const loading = ref(false)
  const error = ref(null)

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

  async function fetchWorkExperiences() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getWorkExperiences()
      workExperiences.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createWorkExperience(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.createWorkExperience(data)
      workExperiences.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateWorkExperience(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updateWorkExperience(id, data)
      const index = workExperiences.value.findIndex(exp => exp.id === id)
      if (index !== -1) {
        workExperiences.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteWorkExperience(id) {
    loading.value = true
    error.value = null
    try {
      await resumeAPI.deleteWorkExperience(id)
      workExperiences.value = workExperiences.value.filter(exp => exp.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Projects - 已新增於 2025-11-30
  async function fetchProjects() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getProjects()
      projects.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createProject(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.createProject(data)
      projects.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateProject(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updateProject(id, data)
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

  async function deleteProject(id) {
    loading.value = true
    error.value = null
    try {
      await resumeAPI.deleteProject(id)
      projects.value = projects.value.filter(p => p.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Education - 已新增於 2025-11-30
  async function fetchEducation() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getEducation()
      education.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createEducation(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.createEducation(data)
      education.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateEducation(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updateEducation(id, data)
      const index = education.value.findIndex(e => e.id === id)
      if (index !== -1) {
        education.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteEducation(id) {
    loading.value = true
    error.value = null
    try {
      await resumeAPI.deleteEducation(id)
      education.value = education.value.filter(e => e.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Certifications - 已新增於 2025-11-30
  async function fetchCertifications() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getCertifications()
      certifications.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCertification(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.createCertification(data)
      certifications.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCertification(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updateCertification(id, data)
      const index = certifications.value.findIndex(c => c.id === id)
      if (index !== -1) {
        certifications.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteCertification(id) {
    loading.value = true
    error.value = null
    try {
      await resumeAPI.deleteCertification(id)
      certifications.value = certifications.value.filter(c => c.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Languages - 已新增於 2025-11-30
  async function fetchLanguages() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getLanguages()
      languages.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createLanguage(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.createLanguage(data)
      languages.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateLanguage(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updateLanguage(id, data)
      const index = languages.value.findIndex(l => l.id === id)
      if (index !== -1) {
        languages.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteLanguage(id) {
    loading.value = true
    error.value = null
    try {
      await resumeAPI.deleteLanguage(id)
      languages.value = languages.value.filter(l => l.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Publications - 已新增於 2025-11-30
  async function fetchPublications() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getPublications()
      publications.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createPublication(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.createPublication(data)
      publications.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updatePublication(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updatePublication(id, data)
      const index = publications.value.findIndex(p => p.id === id)
      if (index !== -1) {
        publications.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deletePublication(id) {
    loading.value = true
    error.value = null
    try {
      await resumeAPI.deletePublication(id)
      publications.value = publications.value.filter(p => p.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // GitHub Projects - 已新增於 2025-11-30
  async function fetchGithubProjects() {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.getGithubProjects()
      githubProjects.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createGithubProject(data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.createGithubProject(data)
      githubProjects.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateGithubProject(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await resumeAPI.updateGithubProject(id, data)
      const index = githubProjects.value.findIndex(g => g.id === id)
      if (index !== -1) {
        githubProjects.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteGithubProject(id) {
    loading.value = true
    error.value = null
    try {
      await resumeAPI.deleteGithubProject(id)
      githubProjects.value = githubProjects.value.filter(g => g.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
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
    fetchPersonalInfo,
    updatePersonalInfo,
    fetchWorkExperiences,
    createWorkExperience,
    updateWorkExperience,
    deleteWorkExperience,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
    fetchEducation,
    createEducation,
    updateEducation,
    deleteEducation,
    fetchCertifications,
    createCertification,
    updateCertification,
    deleteCertification,
    fetchLanguages,
    createLanguage,
    updateLanguage,
    deleteLanguage,
    fetchPublications,
    createPublication,
    updatePublication,
    deletePublication,
    fetchGithubProjects,
    createGithubProject,
    updateGithubProject,
    deleteGithubProject,
  }
})
