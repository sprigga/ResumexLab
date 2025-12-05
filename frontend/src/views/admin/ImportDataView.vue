<script setup>
// 已修改於 2025-12-05，原因：移除 PDF 匯入、範例履歷資料和資料庫管理功能
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useResumeStore } from '@/stores/resume'

const resumeStore = useResumeStore()
const loading = ref(false)
const importStatus = ref('')

// 已移除於 2025-12-05，原因：移除 PDF 檔案匯入功能
// 原函式：handleFileImport、triggerFileInput

// 已移除於 2025-12-05，原因：移除範例履歷資料匯入功能
// 原函式：handleImportResumeData

// 已移除於 2025-12-05，原因：移除資料庫管理功能
// 原函式：handleCreateDatabase

// 已新增於 2025-11-30，原因：新增資料庫匯出功能以方便遷移主機
const handleExportDatabase = async () => {
  try {
    loading.value = true
    importStatus.value = '開始匯出資料庫...'

    const response = await resumeStore.exportDatabase()

    // Create a download link for the blob
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url

    // Extract filename from Content-Disposition header or use default
    const contentDisposition = response.headers['content-disposition']
    let filename = 'resume_db_backup.db'
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/)
      if (filenameMatch) {
        filename = filenameMatch[1]
      }
    }

    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)

    importStatus.value = '資料庫匯出完成！'
    ElMessage.success('資料庫匯出成功')
  } catch (error) {
    ElMessage.error('匯出失敗: ' + (error.message || '未知錯誤'))
    console.error('Export error:', error)
  } finally {
    loading.value = false
  }
}

// 已新增於 2025-11-30，原因：新增資料庫匯入功能以方便遷移主機
const dbInputRef = ref(null)

const triggerDbFileInput = () => {
  if (dbInputRef.value) {
    dbInputRef.value.click()
  }
}

const handleDatabaseImport = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.name.toLowerCase().endsWith('.db')) {
    ElMessage.error('僅支援 .db 資料庫檔案')
    return
  }

  try {
    await ElMessageBox.confirm(
      '此操作將取代現有資料庫，系統會自動建立備份。是否繼續？',
      '確認匯入資料庫',
      {
        confirmButtonText: '確認',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    loading.value = true
    importStatus.value = `開始匯入資料庫: ${file.name}`

    await resumeStore.importDatabase(file)
    importStatus.value = '資料庫匯入完成！'
    ElMessage.success('資料庫匯入成功，現有資料庫已備份')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('匯入失敗: ' + (error.message || '未知錯誤'))
      console.error('Database import error:', error)
    }
  } finally {
    loading.value = false
    // Reset file input
    event.target.value = ''
  }
}
</script>

<template>
  <div class="import-data">
    <!-- 已修改於 2025-12-05，原因：更新標題，僅保留資料庫管理功能 -->
    <h1>資料庫管理</h1>

    <el-card v-loading="loading">
      <div class="import-options">
        <!-- 已移除於 2025-12-05，原因：移除 PDF 檔案匯入區塊 -->
        <!-- 已移除於 2025-12-05，原因：移除範例履歷資料匯入區塊 -->
        <!-- 已移除於 2025-12-05，原因：移除資料庫管理（重建）區塊 -->

        <!-- 保留資料庫匯出和匯入功能 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <h3>資料庫匯出</h3>
            <p>下載資料庫檔案以進行備份或遷移</p>

            <el-button
              type="success"
              @click="handleExportDatabase"
              :disabled="loading"
            >
              匯出資料庫
            </el-button>

            <div v-if="importStatus" class="status-message">
              {{ importStatus }}
            </div>
          </el-col>

          <el-col :span="12">
            <h3>資料庫匯入</h3>
            <p>上傳資料庫檔案以還原或遷移資料（將自動備份現有資料庫）</p>

            <div class="upload-section">
              <input
                ref="dbInputRef"
                type="file"
                accept=".db"
                @change="handleDatabaseImport"
                id="db-upload"
                style="display: none;"
              />
              <el-button
                type="warning"
                @click="triggerDbFileInput"
                :disabled="loading"
              >
                選擇資料庫檔案
              </el-button>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.import-data {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.import-data h1 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 3.2em;
  line-height: 1.1;
}

.import-options h3 {
  margin: 20px 0 10px 0;
  color: #304156;
}

.import-options p {
  color: #606266;
  margin-bottom: 15px;
}

.upload-section {
  margin: 20px 0;
}

/* 已移除於 2025-12-05，原因：移除 PDF 上傳相關樣式 */

.status-message {
  margin-top: 15px;
  padding: 10px;
  background: #f0f9ff;
  border: 1px solid #d9ecff;
  border-radius: 4px;
  color: #409eff;
}

/* 已移除於 2025-12-05，原因：不再需要分隔線樣式 */
</style>