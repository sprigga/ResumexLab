<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useResumeStore } from '@/stores/resume'

const resumeStore = useResumeStore()
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const formData = ref({
  work_experience_id: null,
  title_zh: '',
  title_en: '',
  description_zh: '',
  description_en: '',
  technologies: '',
  tools: '',
  environment: '',
  start_date: '',
  end_date: '',
  display_order: 0,
  // New attachment fields - added on 2025-12-22
  // Reason: Support file attachment functionality
  attachment_name: '',
  attachment_path: '',
  attachment_size: 0,
  attachment_type: '',
  attachment_url: '',
})

onMounted(async () => {
  await loadProjects()
})

const loadProjects = async () => {
  loading.value = true
  try {
    await Promise.all([
      resumeStore.fetchProjects(),
      resumeStore.fetchWorkExperiences()
    ])
  } catch (error) {
    ElMessage.error('Failed to load projects or work experiences')
  } finally {
    loading.value = false
  }
}

// File upload state - added on 2025-12-22
// Reason: Track file upload status and data
const selectedFile = ref(null)
const fileUploading = ref(false)
const uploadRef = ref(null)

const resetForm = () => {
  formData.value = {
    work_experience_id: null,
    title_zh: '',
    title_en: '',
    description_zh: '',
    description_en: '',
    technologies: '',
    tools: '',
    environment: '',
    start_date: '',
    end_date: '',
    display_order: 0,
    // Reset attachment fields - added on 2025-12-22
    attachment_name: '',
    attachment_path: '',
    attachment_size: 0,
    attachment_type: '',
    attachment_url: '',
  }
  // Reset file upload state - added on 2025-12-22
  selectedFile.value = null
  // Reset upload component - added on 2025-12-22
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

const handleAdd = () => {
  resetForm()
  isEditing.value = false
  dialogVisible.value = true
}

const handleEdit = (row) => {
  formData.value = { ...row }
  isEditing.value = true
  dialogVisible.value = true
}

// File upload handler - modified on 2025-12-22
// Reason: Handle file selection and validation with better state management
const handleFileChange = (uploadFile, uploadFiles) => {
  const file = uploadFile.raw
  if (file) {
    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024
    if (file.size > maxSize) {
      ElMessage.error('File size must be less than 10MB')
      // Clear the upload
      if (uploadRef.value) {
        uploadRef.value.clearFiles()
      }
      return false
    }

    // Validate file type
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'image/jpeg', 'image/jpg', 'image/png']
    const allowedExtensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png']
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'))

    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      ElMessage.error('Invalid file type. Allowed types: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG')
      // Clear the upload
      if (uploadRef.value) {
        uploadRef.value.clearFiles()
      }
      return false
    }

    selectedFile.value = file
    formData.value.attachment_name = file.name
    formData.value.attachment_size = file.size
    formData.value.attachment_type = file.type
    return true
  }
  return false
}

// Remove current attachment - added on 2025-12-22
// Reason: Handle removal of existing attachment in edit mode
const removeCurrentAttachment = () => {
  formData.value.attachment_name = ''
  formData.value.attachment_path = ''
  formData.value.attachment_size = 0
  formData.value.attachment_type = ''
  formData.value.attachment_url = ''
}

// Remove selected file - added on 2025-12-22
// Reason: Handle removal of newly selected file
const removeSelectedFile = () => {
  selectedFile.value = null
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

// Handle dialog close - added on 2025-12-22
// Reason: Reset upload state when dialog closes
const handleDialogClose = () => {
  // Reset file selection when dialog closes
  selectedFile.value = null
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

// Updated save method with file upload support for both create and edit - modified on 2025-12-22
// Reason: Handle file upload for both creating and updating projects
const handleSave = async () => {
  loading.value = true
  fileUploading.value = true

  try {
    if (isEditing.value) {
      // For editing, check if a new file is selected
      if (selectedFile.value) {
        await updateProjectWithFile()
      } else {
        await resumeStore.updateProject(formData.value.id, formData.value)
      }
      ElMessage.success('Project updated successfully')
    } else {
      // For creating, use the file upload API if a file is selected
      if (selectedFile.value) {
        await createProjectWithFile()
      } else {
        await resumeStore.createProject(formData.value)
      }
      ElMessage.success('Project created successfully')
    }
    dialogVisible.value = false
    await loadProjects()
    // Reset upload component after successful save - added on 2025-12-22
    if (uploadRef.value) {
      uploadRef.value.clearFiles()
    }
  } catch (error) {
    ElMessage.error('Failed to save project')
  } finally {
    loading.value = false
    fileUploading.value = false
  }
}

// Create project with file - added on 2025-12-22
// Reason: Handle file upload API call
// Fixed on 2025-12-22: Include all form fields even if empty, as backend expects them
const createProjectWithFile = async () => {
  const formDataToSend = new FormData()

  // Add form fields - include all fields even if empty/null, as backend expects them
  Object.keys(formData.value).forEach(key => {
    if (key !== 'attachment_url' && key !== 'id') {  // Exclude attachment_url and id from form data
      const value = formData.value[key]
      // Convert undefined/null to empty string for form data
      formDataToSend.append(key, value !== null && value !== undefined ? value : '')
    }
  })

  // Add file
  if (selectedFile.value) {
    formDataToSend.append('file', selectedFile.value)
  }

  const token = localStorage.getItem('token')
  const response = await fetch('/api/projects/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formDataToSend
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Upload failed')
  }

  return response.json()
}

// Update project with file - added on 2025-12-22
// Reason: Handle file upload for updates
// Fixed on 2025-12-22: Include all form fields even if empty, as backend expects them
const updateProjectWithFile = async () => {
  const formDataToSend = new FormData()

  // Add form fields - include all fields even if empty/null, as backend expects them
  Object.keys(formData.value).forEach(key => {
    if (key !== 'attachment_url' && key !== 'id') {  // Exclude attachment_url and id from form data
      const value = formData.value[key]
      // Convert undefined/null to empty string for form data
      formDataToSend.append(key, value !== null && value !== undefined ? value : '')
    }
  })

  // Add file
  if (selectedFile.value) {
    formDataToSend.append('file', selectedFile.value)
  }

  // Note: Don't append id to FormData as it should be in URL path parameter

  const token = localStorage.getItem('token')
  const response = await fetch(`/api/projects/${formData.value.id}/upload`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formDataToSend
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Upload failed')
  }

  return response.json()
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure to delete this project?',
      'Warning',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )

    loading.value = true
    await resumeStore.deleteProject(id)
    ElMessage.success('Deleted successfully')
    await loadProjects()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete')
    }
  } finally {
    loading.value = false
  }
}

const getCompanyName = (workExperienceId) => {
  if (!workExperienceId || !resumeStore.workExperiences) return 'N/A'
  const workExp = resumeStore.workExperiences.find(we => we.id === workExperienceId)
  return workExp ? (workExp.company_en || workExp.company_zh || 'N/A') : 'N/A'
}

// Handle file download - modified on 2025-12-22
// Reason: Simplified with proper proxy configuration and improved error handling
const handleDownload = async (url, fileName) => {
  try {
    // Use the URL directly - proxy will handle the routing to backend
    // Modified on 2025-12-22: Removed manual URL construction since Vite proxy handles /uploads
    const response = await fetch(url)
    if (!response.ok) {
      if (response.status === 404) {
        ElMessage.error('File not found on server. The file may have been deleted.')
        // Reload projects to update UI with latest data
        await loadProjects()
      } else {
        ElMessage.error(`Failed to download file: ${response.status} ${response.statusText}`)
      }
      return
    }

    // Download the file
    const blob = await response.blob()
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = downloadUrl
    a.download = fileName || 'download'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    document.body.removeChild(a)

    ElMessage.success('File downloaded successfully')
  } catch (error) {
    console.error('Download error:', error)
    ElMessage.error('Failed to download file: ' + error.message)
  }
}
</script>

<template>
  <div class="project-edit">
    <div class="header">
      <h1>Manage Projects</h1>
      <el-button type="primary" @click="handleAdd">Add New</el-button>
    </div>

    <el-card v-loading="loading">
      <el-table :data="resumeStore.projects" stripe>
        <el-table-column prop="title_en" label="Title" width="250" />
        <el-table-column label="Period" width="200">
          <template #default="{ row }">
            {{ row.start_date || 'N/A' }} - {{ row.end_date || 'Present' }}
          </template>
        </el-table-column>
        <el-table-column prop="technologies" label="Technologies" width="200" />
        <!-- Attachment column - added on 2025-12-22 -->
        <!-- Reason: Display attachment information in table -->
        <el-table-column label="Attachment" width="150">
          <template #default="{ row }">
            <div v-if="row.attachment_name">
              <el-tooltip :content="row.attachment_name" placement="top">
                <el-button
                  v-if="row.attachment_url"
                  size="small"
                  type="primary"
                  link
                  @click="handleDownload(row.attachment_url, row.attachment_name)"
                >
                  <el-icon><Document /></el-icon>
                  <span style="margin-left: 5px">{{ row.attachment_name.substring(0, 15) }}...</span>
                </el-button>
                <span v-else style="color: #999;">
                  <el-icon><Document /></el-icon>
                  <span style="margin-left: 5px">{{ row.attachment_name.substring(0, 15) }}...</span>
                  <span style="margin-left: 5px; font-size: 12px;">(File missing)</span>
                </span>
              </el-tooltip>
              <div style="font-size: 12px; color: #999;">
                {{ row.attachment_size ? (row.attachment_size / 1024).toFixed(1) + 'KB' : 'Size unknown' }}
              </div>
            </div>
            <span v-else style="color: #ccc;">No attachment</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">Edit</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? 'Edit Project' : 'Add Project'"
      width="80%"
      @close="handleDialogClose"
    >
      <el-form :model="formData" label-width="150px" label-position="top">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="Company">
              <el-tag type="info" size="large">{{ getCompanyName(formData.work_experience_id) || 'N/A' }}</el-tag>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Title (Chinese)">
              <el-input v-model="formData.title_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Title (English)">
              <el-input v-model="formData.title_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Description (Chinese)">
              <el-input v-model="formData.description_zh" type="textarea" :rows="5" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Description (English)">
              <el-input v-model="formData.description_en" type="textarea" :rows="5" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="Technologies">
              <el-input v-model="formData.technologies" placeholder="e.g., Vue, React" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Tools">
              <el-input v-model="formData.tools" placeholder="e.g., Git, Docker" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Environment">
              <el-input v-model="formData.environment" placeholder="e.g., Linux, AWS" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="Start Date">
              <el-date-picker
                v-model="formData.start_date"
                type="date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="End Date">
              <el-date-picker
                v-model="formData.end_date"
                type="date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <!-- Modified on 2025-11-30: Added display_order field -->
          <!-- Reason: Allow users to control project sorting order (0=newest, 10=oldest) -->
          <el-col :span="8">
            <el-form-item label="Display Order">
              <el-input-number
                v-model="formData.display_order"
                :min="0"
                :max="999"
                style="width: 100%"
                placeholder="0=newest, higher=older"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- File upload section - added on 2025-12-22 -->
        <!-- Reason: Allow users to attach files to projects -->
        <!-- Updated on 2025-12-22: Enable file upload for both create and edit modes -->
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="Attachment">
              <!-- Show upload component for both create and edit modes -->
              <div>
                <el-upload
                  ref="uploadRef"
                  :auto-upload="false"
                  :show-file-list="false"
                  :on-change="handleFileChange"
                  :limit="1"
                  accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
                >
                  <el-button type="primary">{{ isEditing ? 'Change File' : 'Select File' }}</el-button>
                  <template #tip>
                    <div class="el-upload__tip">
                      Supported formats: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG (Max 10MB)
                    </div>
                  </template>
                </el-upload>

                <!-- Show current attachment info for edit mode -->
                <div v-if="isEditing && formData.attachment_name && !selectedFile" style="margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-radius: 4px;">
                  <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                      <el-icon><Document /></el-icon>
                      <span style="margin-left: 8px;">{{ formData.attachment_name }}</span>
                      <span v-if="formData.attachment_size" style="margin-left: 10px; color: #999;">
                        ({{ (formData.attachment_size / 1024).toFixed(1) }}KB)
                      </span>
                      <el-button
                        v-if="formData.attachment_url"
                        size="small"
                        type="primary"
                        @click="handleDownload(formData.attachment_url, formData.attachment_name)"
                        style="margin-left: 10px;"
                      >
                        <el-icon><Download /></el-icon>
                        Download
                      </el-button>
                      <span v-else style="margin-left: 10px; color: #ff6b6b; font-size: 12px;">
                        (File missing)
                      </span>
                    </div>
                    <el-button size="small" type="danger" @click="removeCurrentAttachment">
                      Remove Current
                    </el-button>
                  </div>
                </div>

                <!-- Show selected file info -->
                <div v-if="selectedFile" style="margin-top: 10px; padding: 10px; background-color: #f5f5f5; border-radius: 4px;">
                  <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                      <el-icon><Document /></el-icon>
                      <span style="margin-left: 8px;">{{ selectedFile.name }}</span>
                      <span style="margin-left: 10px; color: #999;">({{ (selectedFile.size / 1024).toFixed(1) }}KB)</span>
                    </div>
                    <el-button size="small" type="danger" @click="removeSelectedFile">
                      Remove New
                    </el-button>
                  </div>
                </div>

                <!-- Show no attachment message for create mode -->
                <div v-if="!isEditing && !formData.attachment_name && !selectedFile" style="margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-radius: 4px; color: #999;">
                  No attachment selected
                </div>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSave" :loading="loading || fileUploading">
          {{ fileUploading ? 'Uploading...' : 'Save' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* Applying global styles from style.css */
/* Created on 2025-11-30 */
/* Reason: Managing project data in admin panel */
.project-edit {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.project-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.project-edit h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 3.2em;
  line-height: 1.1;
}

:deep(.el-card) {
  padding: 2em;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

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

:deep(.el-textarea__inner) {
  text-align: left;
}

@media (prefers-color-scheme: light) {
  .project-edit h1 {
    color: #213547;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
