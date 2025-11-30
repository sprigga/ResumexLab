<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useResumeStore } from '@/stores/resume'

const resumeStore = useResumeStore()
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const formData = ref({
  school_zh: '',
  school_en: '',
  degree_zh: '',
  degree_en: '',
  major_zh: '',
  major_en: '',
  start_date: '',
  end_date: '',
  description_zh: '',
  description_en: '',
  display_order: 0,
})

onMounted(async () => {
  await loadEducation()
})

const loadEducation = async () => {
  loading.value = true
  try {
    await resumeStore.fetchEducation()
  } catch (error) {
    ElMessage.error('Failed to load education')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    school_zh: '',
    school_en: '',
    degree_zh: '',
    degree_en: '',
    major_zh: '',
    major_en: '',
    start_date: '',
    end_date: '',
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
      await resumeStore.updateEducation(formData.value.id, formData.value)
      ElMessage.success('Education updated successfully')
    } else {
      await resumeStore.createEducation(formData.value)
      ElMessage.success('Education created successfully')
    }
    dialogVisible.value = false
    await loadEducation()
  } catch (error) {
    ElMessage.error('Failed to save education')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure to delete this education record?',
      'Warning',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )

    loading.value = true
    await resumeStore.deleteEducation(id)
    ElMessage.success('Deleted successfully')
    await loadEducation()
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
  <div class="education-edit">
    <div class="header">
      <h1>Manage Education</h1>
      <el-button type="primary" @click="handleAdd">Add New</el-button>
    </div>

    <el-card v-loading="loading">
      <el-table :data="resumeStore.education" stripe>
        <el-table-column prop="school_en" label="School" width="250" />
        <el-table-column prop="degree_en" label="Degree" width="150" />
        <el-table-column prop="major_en" label="Major" width="200" />
        <el-table-column label="Period" width="200">
          <template #default="{ row }">
            {{ row.start_date }} - {{ row.end_date }}
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
      :title="isEditing ? 'Edit Education' : 'Add Education'"
      width="80%"
    >
      <el-form :model="formData" label-width="150px" label-position="top">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="School (Chinese)">
              <el-input v-model="formData.school_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="School (English)">
              <el-input v-model="formData.school_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Degree (Chinese)">
              <el-input v-model="formData.degree_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Degree (English)">
              <el-input v-model="formData.degree_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Major (Chinese)">
              <el-input v-model="formData.major_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Major (English)">
              <el-input v-model="formData.major_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Start Date">
              <el-date-picker
                v-model="formData.start_date"
                type="date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="End Date">
              <el-date-picker
                v-model="formData.end_date"
                type="date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
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
/* Created on 2025-11-30 */
/* Reason: Managing education data in admin panel */
.education-edit {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.education-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.education-edit h1 {
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
  .education-edit h1 {
    color: #213547;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
