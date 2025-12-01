<script setup>
import { ref, onMounted } from 'vue'
import { resumeAPI } from '@/api/resume' // 使用與 ResumeView 相同的 API

const testData = ref(null)
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  console.log('Testing API access...')
  loading.value = true
  error.value = null
  
  try {
    // 測試獲取個人信息
    const response = await resumeAPI.getPersonalInfo()
    testData.value = response.data
    console.log('✅ Successfully fetched personal info:', response.data)
  } catch (err) {
    console.error('❌ Error fetching data:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div style="padding: 20px;">
    <h1>API Connection Test</h1>
    
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">
      <p style="color: red;">Error: {{ error }}</p>
      <pre>{{ error }}</pre>
    </div>
    <div v-else-if="testData">
      <h2>Success! Retrieved Data:</h2>
      <p><strong>Name:</strong> {{ testData.name_en || testData.name }}</p>
      <p><strong>Email:</strong> {{ testData.email }}</p>
      <p><strong>Phone:</strong> {{ testData.phone }}</p>
    </div>
    <div v-else>
      <p>No data retrieved</p>
    </div>
  </div>
</template>