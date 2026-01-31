<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useResumeStore } from '@/stores/resume'

const resumeStore = useResumeStore()
const loading = ref(false)
const formData = ref({
  name_zh: '',
  name_en: '',
  phone: '',
  email: '',
  address_zh: '',
  address_en: '',
  objective_zh: '',
  objective_en: '',
  personality_zh: '',
  personality_en: '',
  summary_zh: '',
  summary_en: '',
})

onMounted(async () => {
  loading.value = true
  try {
    const data = await resumeStore.fetchPersonalInfo()
    if (data) {
      formData.value = { ...data }
    }
  } catch (error) {
    console.error('Failed to load personal info:', error)
  } finally {
    loading.value = false
  }
})

const handleSave = async () => {
  loading.value = true
  try {
    await resumeStore.updatePersonalInfo(formData.value)
    ElMessage.success('Personal information updated successfully')
  } catch (error) {
    ElMessage.error('Failed to update personal information')
    console.error('Save error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="personal-info-edit">
    <h1>Edit Personal Information</h1>

    <el-card v-loading="loading">
      <el-form :model="formData" label-width="120px" label-position="top">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Name (Chinese)">
              <el-input v-model="formData.name_zh" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Name (English)">
              <el-input v-model="formData.name_en" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Phone">
              <el-input v-model="formData.phone" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Email">
              <el-input v-model="formData.email" type="email" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Address (Chinese)">
              <el-input v-model="formData.address_zh" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Address (English)">
              <el-input v-model="formData.address_en" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Career Objective (Chinese)">
              <el-input v-model="formData.objective_zh" type="textarea" :rows="3" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Career Objective (English)">
              <el-input v-model="formData.objective_en" type="textarea" :rows="3" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Professional Summary (Chinese)">
              <el-input
                v-model="formData.summary_zh"
                type="textarea"
                :rows="4"
                :input-style="{ whiteSpace: 'pre-wrap' }"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Professional Summary (English)">
              <el-input
                v-model="formData.summary_en"
                type="textarea"
                :rows="4"
                :input-style="{ whiteSpace: 'pre-wrap' }"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="loading">
            Save
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
/* Applying global styles from style.css - Updated on 2025-11-29 */
/* Reason: Matching dark gradient background theme from ResumeView.vue and style.css */
.personal-info-edit {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  /* Gradient background from black to deep blue to gray - matches style.css */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%) !important;
  color: rgba(255, 255, 255, 0.87);
  padding: 20px;
  position: relative;
}

/* Vignette effect - subtle inner shadow */
.personal-info-edit::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  box-shadow: inset 0 0 200px rgba(0, 0, 0, 0.5);
  z-index: 0;
}

/* Ensure content is above vignette */
.personal-info-edit > * {
  position: relative;
  z-index: 1;
}

.personal-info-edit h1 {
  margin: 0 0 20px 0;
  /* Original color - commented out on 2025-11-29 */
  /* Reason: Adjusting text color for dark gradient background */
  /* color: #2c3e50; */
  color: rgba(255, 255, 255, 0.95);
  font-size: 3.2em;
  line-height: 1.1;
}

/* Card styles with dark gradient background - Updated on 2025-11-29 */
/* Reason: Matching ResumeView.vue card styling for consistency */
:deep(.el-card) {
  padding: 2em;
  /* Original background - commented out on 2025-11-29 */
  /* Reason: Making card background consistent with dark gradient theme */
  /* background-color: rgba(255, 255, 255, 0.95); */
  /* backdrop-filter: blur(10px); */

  /* New background matching the gradient */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%) !important;
  color: rgba(255, 255, 255, 0.87) !important;
  border: none !important;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

/* Form label styling - Added on 2025-11-29 */
/* Reason: Making form labels match the work experience section text color */
:deep(.el-form-item__label) {
  color: rgba(255, 255, 255, 0.95) !important;
  font-weight: 500;
}

/* Input and textarea styling - Added on 2025-11-29 */
/* Reason: Making input fields visible on dark background */
:deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  background-color: transparent !important;
  color: rgba(255, 255, 255, 0.87) !important;
}

:deep(.el-textarea__inner) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: rgba(255, 255, 255, 0.87) !important;
  white-space: pre-wrap !important; /* Preserve line breaks and whitespace */
}

/* Input placeholder styling */
:deep(.el-input__inner::placeholder),
:deep(.el-textarea__inner::placeholder) {
  color: rgba(255, 255, 255, 0.4) !important;
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

:deep(.el-button--primary) {
  background-color: #646cff !important;
  border-color: #646cff !important;
  color: white !important;
}

:deep(.el-button--primary:hover) {
  background-color: #535bf2 !important;
  border-color: #535bf2 !important;
}

:deep(.el-button:focus),
:deep(.el-button:focus-visible) {
  outline: 4px auto -webkit-focus-ring-color;
}

/* Loading overlay - Added on 2025-11-29 */
/* Reason: Make loading overlay background transparent to match gradient */
:deep(.el-loading-mask) {
  background-color: rgba(0, 0, 0, 0.5) !important;
}

/* Light mode specific styles */
@media (prefers-color-scheme: light) {
  .personal-info-edit {
    color: #213547;
    background: #ffffff !important;
  }

  .personal-info-edit::before {
    display: none;
  }

  .personal-info-edit h1 {
    color: #213547;
  }

  :deep(.el-card) {
    background: #ffffff !important;
    color: #213547 !important;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }

  :deep(.el-form-item__label) {
    color: #606266 !important;
  }

  :deep(.el-input__wrapper) {
    background-color: #ffffff !important;
    box-shadow: 0 0 0 1px #dcdfe6 inset !important;
  }

  :deep(.el-input__inner),
  :deep(.el-textarea__inner) {
    background-color: #ffffff !important;
    color: #606266 !important;
    border-color: #dcdfe6 !important;
  }

  :deep(.el-textarea__inner) {
    white-space: pre-wrap !important; /* Preserve line breaks in light mode */
  }

  :deep(.el-input__inner::placeholder),
  :deep(.el-textarea__inner::placeholder) {
    color: #a8abb2 !important;
  }
}
</style>
