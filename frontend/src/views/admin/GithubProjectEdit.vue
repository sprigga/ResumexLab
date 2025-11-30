<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useResumeStore } from '@/stores/resume'

const resumeStore = useResumeStore()
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const formData = ref({
  name_zh: '',
  name_en: '',
  description_zh: '',
  description_en: '',
  url: '',
  display_order: 0,
})

onMounted(async () => {
  await loadGithubProjects()
})

const loadGithubProjects = async () => {
  loading.value = true
  try {
    await resumeStore.fetchGithubProjects()
  } catch (error) {
    ElMessage.error('Failed to load GitHub projects')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    name_zh: '',
    name_en: '',
    description_zh: '',
    description_en: '',
    url: '',
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
      await resumeStore.updateGithubProject(formData.value.id, formData.value)
      ElMessage.success('GitHub project updated successfully')
    } else {
      await resumeStore.createGithubProject(formData.value)
      ElMessage.success('GitHub project created successfully')
    }
    dialogVisible.value = false
    await loadGithubProjects()
  } catch (error) {
    ElMessage.error('Failed to save GitHub project')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure to delete this GitHub project?',
      'Warning',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )

    loading.value = true
    await resumeStore.deleteGithubProject(id)
    ElMessage.success('Deleted successfully')
    await loadGithubProjects()
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
  <div class="github-project-edit">
    <div class="header">
      <h1>Manage GitHub Projects</h1>
      <el-button type="primary" @click="handleAdd">Add New</el-button>
    </div>

    <el-card v-loading="loading">
      <el-table :data="resumeStore.githubProjects" stripe>
        <el-table-column prop="name_zh" label="Name (中文)" width="200" />
        <el-table-column prop="name_en" label="Name (English)" width="200" />
        <el-table-column prop="description_zh" label="Description (中文)" width="250" show-overflow-tooltip />
        <el-table-column prop="description_en" label="Description (English)" width="250" show-overflow-tooltip />
        <el-table-column prop="url" label="URL" width="250">
          <template #default="{ row }">
            <a :href="row.url" target="_blank" rel="noopener noreferrer">{{ row.url }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="display_order" label="Order" width="80" />
        <el-table-column label="Actions" width="150" fixed="right">
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
      :title="isEditing ? 'Edit GitHub Project' : 'Add GitHub Project'"
      width="80%"
    >
      <el-form :model="formData" label-width="180px" label-position="top">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Project Name (中文)">
              <el-input v-model="formData.name_zh" placeholder="專案名稱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Project Name (English)">
              <el-input v-model="formData.name_en" placeholder="Project Name" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Description (中文)">
              <el-input
                v-model="formData.description_zh"
                type="textarea"
                :rows="4"
                placeholder="專案描述"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Description (English)">
              <el-input
                v-model="formData.description_en"
                type="textarea"
                :rows="4"
                placeholder="Project Description"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item label="GitHub URL">
              <el-input v-model="formData.url" placeholder="https://github.com/username/repository" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="Display Order">
              <el-input-number v-model="formData.display_order" :min="0" style="width: 100%" />
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
/* 已新增於 2025-11-30 */
/* 原因：創建 GitHub 專案管理介面 */
.github-project-edit {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.github-project-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.github-project-edit h1 {
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

:deep(.el-table a) {
  color: #409eff;
  text-decoration: none;
}

:deep(.el-table a:hover) {
  text-decoration: underline;
}

@media (prefers-color-scheme: light) {
  .github-project-edit h1 {
    color: #213547;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
