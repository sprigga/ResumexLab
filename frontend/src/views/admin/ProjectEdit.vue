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

const handleSave = async () => {
  loading.value = true
  try {
    if (isEditing.value) {
      await resumeStore.updateProject(formData.value.id, formData.value)
      ElMessage.success('Project updated successfully')
    } else {
      await resumeStore.createProject(formData.value)
      ElMessage.success('Project created successfully')
    }
    dialogVisible.value = false
    await loadProjects()
  } catch (error) {
    ElMessage.error('Failed to save project')
  } finally {
    loading.value = false
  }
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
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSave" :loading="loading">Save</el-button>
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
