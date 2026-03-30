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
    school_zh: '', school_en: '',
    degree_zh: '', degree_en: '',
    major_zh: '', major_en: '',
    start_date: '', end_date: '',
    description_zh: '', description_en: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchEducation(),
  create: (data) => resumeStore.createEducation(data),
  update: (id, data) => resumeStore.updateEducation(id, data),
  delete: (id) => resumeStore.deleteEducation(id),
  entityName: 'Education',
})

onMounted(loadData)
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
.education-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
