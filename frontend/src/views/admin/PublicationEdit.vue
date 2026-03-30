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
    title: '', authors: '', publication: '',
    year: null, pages: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchPublications(),
  create: (data) => resumeStore.createPublication(data),
  update: (id, data) => resumeStore.updatePublication(id, data),
  delete: (id) => resumeStore.deletePublication(id),
  entityName: 'Publication',
})

onMounted(loadData)
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
.publication-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
