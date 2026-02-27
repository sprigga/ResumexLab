<script setup>
import { onMounted } from 'vue'
import { useResumeStore } from '@/stores/resume'
import { useCrudPanel } from '@/composables/useCrudPanel'

const resumeStore = useResumeStore()

// Certifications panel
const {
  loading,
  dialogVisible: certDialogVisible,
  isEditing: isEditingCert,
  formData: certFormData,
  loadData: loadCerts,
  handleAdd: handleAddCert,
  handleEdit: handleEditCert,
  handleSave: handleSaveCert,
  handleDelete: handleDeleteCert,
} = useCrudPanel({
  defaultForm: {
    name_zh: '', name_en: '',
    issuer: '', issue_date: '',
    certificate_number: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchCertifications(),
  create: (data) => resumeStore.createCertification(data),
  update: (id, data) => resumeStore.updateCertification(id, data),
  delete: (id) => resumeStore.deleteCertification(id),
  entityName: 'Certification',
})

// Languages panel
const {
  loading: langLoading,
  dialogVisible: langDialogVisible,
  isEditing: isEditingLang,
  formData: langFormData,
  loadData: loadLangs,
  handleAdd: handleAddLang,
  handleEdit: handleEditLang,
  handleSave: handleSaveLang,
  handleDelete: handleDeleteLang,
} = useCrudPanel({
  defaultForm: {
    language_zh: '', language_en: '',
    proficiency_zh: '', proficiency_en: '',
    test_name: '', score: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchLanguages(),
  create: (data) => resumeStore.createLanguage(data),
  update: (id, data) => resumeStore.updateLanguage(id, data),
  delete: (id) => resumeStore.deleteLanguage(id),
  entityName: 'Language',
})

onMounted(async () => {
  await Promise.all([loadCerts(), loadLangs()])
})
</script>

<template>
  <div class="certification-edit">
    <!-- Certifications Section -->
    <div class="section">
      <div class="header">
        <h1>Manage Certifications</h1>
        <el-button type="primary" @click="handleAddCert">Add New</el-button>
      </div>

      <el-card v-loading="loading">
        <el-table :data="resumeStore.certifications" stripe>
          <el-table-column prop="name_en" label="Name" width="250" />
          <el-table-column prop="issuer" label="Issuer" width="200" />
          <el-table-column prop="issue_date" label="Issue Date" width="150" />
          <el-table-column prop="certificate_number" label="Certificate #" width="150" />
          <el-table-column label="Actions" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="handleEditCert(row)">Edit</el-button>
              <el-button size="small" type="danger" @click="handleDeleteCert(row.id)">
                Delete
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- Languages Section -->
    <div class="section">
      <div class="header">
        <h1>Manage Languages</h1>
        <el-button type="primary" @click="handleAddLang">Add New</el-button>
      </div>

      <el-card v-loading="loading">
        <el-table :data="resumeStore.languages" stripe>
          <el-table-column prop="language_en" label="Language" width="150" />
          <el-table-column prop="proficiency_en" label="Proficiency" width="150" />
          <el-table-column prop="test_name" label="Test Name" width="150" />
          <el-table-column prop="score" label="Score" width="100" />
          <el-table-column label="Actions" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="handleEditLang(row)">Edit</el-button>
              <el-button size="small" type="danger" @click="handleDeleteLang(row.id)">
                Delete
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- Certification Dialog -->
    <el-dialog
      v-model="certDialogVisible"
      :title="isEditingCert ? 'Edit Certification' : 'Add Certification'"
      width="70%"
    >
      <el-form :model="certFormData" label-width="150px" label-position="top">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Name (Chinese)">
              <el-input v-model="certFormData.name_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Name (English)">
              <el-input v-model="certFormData.name_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Issuer">
              <el-input v-model="certFormData.issuer" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Issue Date">
              <el-date-picker
                v-model="certFormData.issue_date"
                type="date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="Certificate Number">
          <el-input v-model="certFormData.certificate_number" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="certDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSaveCert" :loading="loading">Save</el-button>
      </template>
    </el-dialog>

    <!-- Language Dialog -->
    <el-dialog
      v-model="langDialogVisible"
      :title="isEditingLang ? 'Edit Language' : 'Add Language'"
      width="70%"
    >
      <el-form :model="langFormData" label-width="150px" label-position="top">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Language (Chinese)">
              <el-input v-model="langFormData.language_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Language (English)">
              <el-input v-model="langFormData.language_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Proficiency (Chinese)">
              <el-input v-model="langFormData.proficiency_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Proficiency (English)">
              <el-input v-model="langFormData.proficiency_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Test Name">
              <el-input v-model="langFormData.test_name" placeholder="e.g., TOEFL, IELTS" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Score">
              <el-input v-model="langFormData.score" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <el-button @click="langDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSaveLang" :loading="loading">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* Applying global styles from style.css */
/* Created on 2025-11-30 */
/* Reason: Managing certification and language data in admin panel */
.certification-edit {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.section {
  margin-bottom: 40px;
}

.certification-edit .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.certification-edit h1 {
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
  .certification-edit h1 {
    color: #213547;
  }

  :deep(.el-card) {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
