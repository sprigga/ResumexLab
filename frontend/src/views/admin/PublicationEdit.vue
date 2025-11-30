<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useResumeStore } from '@/stores/resume'

const resumeStore = useResumeStore()
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const formData = ref({
  title: '',
  authors: '',
  publication: '',
  year: null,
  pages: '',
  display_order: 0,
})

onMounted(async () => {
  await loadPublications()
})

const loadPublications = async () => {
  loading.value = true
  try {
    await resumeStore.fetchPublications()
  } catch (error) {
    ElMessage.error('Failed to load publications')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    title: '',
    authors: '',
    publication: '',
    year: null,
    pages: '',
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
      await resumeStore.updatePublication(formData.value.id, formData.value)
      ElMessage.success('Publication updated successfully')
    } else {
      await resumeStore.createPublication(formData.value)
      ElMessage.success('Publication created successfully')
    }
    dialogVisible.value = false
    await loadPublications()
  } catch (error) {
    ElMessage.error('Failed to save publication')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure to delete this publication?',
      'Warning',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )

    loading.value = true
    await resumeStore.deletePublication(id)
    ElMessage.success('Deleted successfully')
    await loadPublications()
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
  <div class="publication-edit">
    <div class="header">
      <h1>Manage Publications</h1>
      <el-button type="primary" @click="handleAdd">Add New</el-button>
    </div>

    <el-card v-loading="loading">
      <el-table :data="resumeStore.publications" stripe>
        <el-table-column prop="title" label="Title" width="300" />
        <el-table-column prop="authors" label="Authors" width="200" />
        <el-table-column prop="publication" label="Publication" width="200" />
        <el-table-column prop="year" label="Year" width="100" />
        <el-table-column prop="pages" label="Pages" width="100" />
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
      :title="isEditing ? 'Edit Publication' : 'Add Publication'"
      width="80%"
    >
      <el-form :model="formData" label-width="150px" label-position="top">
        <el-form-item label="Title">
          <el-input v-model="formData.title" />
        </el-form-item>

        <el-form-item label="Authors">
          <el-input v-model="formData.authors" placeholder="e.g., John Doe, Jane Smith" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Publication">
              <el-input v-model="formData.publication" placeholder="Journal or Conference name" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="Year">
              <el-input-number v-model="formData.year" :min="1900" :max="2100" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="Pages">
              <el-input v-model="formData.pages" placeholder="e.g., 1-10" />
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
/* Reason: Managing publication data in admin panel */
.publication-edit {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.publication-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.publication-edit h1 {
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
  .publication-edit h1 {
    color: #213547;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
