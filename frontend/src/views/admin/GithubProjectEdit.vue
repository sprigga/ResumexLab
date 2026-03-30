<script setup>
import { onMounted } from 'vue'
import { useResumeStore } from '@/stores/resume'
import { useCrudPanel } from '@/composables/useCrudPanel'

const resumeStore = useResumeStore()

const {
  loading, dialogVisible, isEditing, formData,
  loadData, handleAdd, handleEdit, handleSave, handleDelete,
} = useCrudPanel({
  defaultForm: {
    name_zh: '', name_en: '',
    description_zh: '', description_en: '',
    url: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchGithubProjects(),
  create: (data) => resumeStore.createGithubProject(data),
  update: (id, data) => resumeStore.updateGithubProject(id, data),
  delete: (id) => resumeStore.deleteGithubProject(id),
  entityName: 'GitHub project',
})

onMounted(loadData)
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
.github-project-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

:deep(.el-table a) {
  color: #409eff;
  text-decoration: none;
}

:deep(.el-table a:hover) {
  text-decoration: underline;
}
</style>
