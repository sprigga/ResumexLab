<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useResumeStore } from '@/stores/resume'

const resumeStore = useResumeStore()
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const formData = ref({
  company_zh: '',
  company_en: '',
  position_zh: '',
  position_en: '',
  location_zh: '',
  location_en: '',
  start_date: '',
  end_date: '',
  is_current: false,
  description_zh: '',
  description_en: '',
  display_order: 0,
})

onMounted(async () => {
  await loadWorkExperiences()
})

const loadWorkExperiences = async () => {
  loading.value = true
  try {
    await resumeStore.fetchWorkExperiences()
  } catch (error) {
    ElMessage.error('Failed to load work experiences')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    company_zh: '',
    company_en: '',
    position_zh: '',
    position_en: '',
    location_zh: '',
    location_en: '',
    start_date: '',
    end_date: '',
    is_current: false,
    description_zh: '',
    description_en: '',
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
      await resumeStore.updateWorkExperience(formData.value.id, formData.value)
      ElMessage.success('Work experience updated successfully')
    } else {
      await resumeStore.createWorkExperience(formData.value)
      ElMessage.success('Work experience created successfully')
    }
    dialogVisible.value = false
    await loadWorkExperiences()
  } catch (error) {
    ElMessage.error('Failed to save work experience')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure to delete this work experience?',
      'Warning',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )

    loading.value = true
    await resumeStore.deleteWorkExperience(id)
    ElMessage.success('Deleted successfully')
    await loadWorkExperiences()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete')
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="work-experience-edit">
    <div class="header">
      <h1>Manage Work Experience</h1>
      <el-button type="primary" @click="handleAdd">Add New</el-button>
    </div>

    <el-card v-loading="loading">
      <el-table :data="resumeStore.workExperiences" stripe>
        <el-table-column prop="company_en" label="Company" width="200" />
        <el-table-column prop="position_en" label="Position" width="180" />
        <el-table-column label="Period" width="200">
          <template #default="{ row }">
            {{ row.start_date }} - {{ row.is_current ? 'Present' : row.end_date }}
          </template>
        </el-table-column>
        <el-table-column prop="location_en" label="Location" width="150" />
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
      :title="isEditing ? 'Edit Work Experience' : 'Add Work Experience'"
      width="80%"
    >
      <el-form :model="formData" label-width="150px" label-position="top">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Company (Chinese)">
              <el-input v-model="formData.company_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Company (English)">
              <el-input v-model="formData.company_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Position (Chinese)">
              <el-input v-model="formData.position_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Position (English)">
              <el-input v-model="formData.position_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Location (Chinese)">
              <el-input v-model="formData.location_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Location (English)">
              <el-input v-model="formData.location_en" />
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
                :disabled="formData.is_current"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Current Position">
              <el-checkbox v-model="formData.is_current">Is Current</el-checkbox>
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
.work-experience-edit {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.work-experience-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.work-experience-edit h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 3.2em;
  line-height: 1.1;
}

/* Card styles with transparency for gradient background */
:deep(.el-card) {
  padding: 2em;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
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

/* Textarea text alignment - Added on 2025-11-29 */
/* Reason: Set textarea text to left-align for better readability */
:deep(.el-textarea__inner) {
  text-align: left;
}

/* Light mode specific styles */
@media (prefers-color-scheme: light) {
  .work-experience-edit h1 {
    color: #213547;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
