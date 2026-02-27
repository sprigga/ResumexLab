import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

/**
 * Composable that encapsulates the repeated CRUD panel pattern:
 * dialog visibility, loading state, form data, and CRUD handlers.
 *
 * @param {object} config
 * @param {object} config.defaultForm   - Plain object with default empty form values
 * @param {Function} config.fetch       - () => Promise  — load all items
 * @param {Function} config.create      - (data) => Promise — create new item
 * @param {Function} config.update      - (id, data) => Promise — update item
 * @param {Function} config.delete      - (id) => Promise — delete item
 * @param {string}  config.entityName   - Human-readable name for messages (e.g. "Education")
 */
export function useCrudPanel({ defaultForm, fetch, create, update, delete: del, entityName }) {
  const loading = ref(false)
  const dialogVisible = ref(false)
  const isEditing = ref(false)
  const formData = ref({ ...defaultForm })

  const resetForm = () => {
    formData.value = { ...defaultForm }
  }

  const loadData = async () => {
    loading.value = true
    try {
      await fetch()
    } catch {
      ElMessage.error(`Failed to load ${entityName}`)
    } finally {
      loading.value = false
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
        await update(formData.value.id, formData.value)
        ElMessage.success(`${entityName} updated successfully`)
      } else {
        await create(formData.value)
        ElMessage.success(`${entityName} created successfully`)
      }
      dialogVisible.value = false
      await fetch()
    } catch {
      ElMessage.error(`Failed to save ${entityName}`)
    } finally {
      loading.value = false
    }
  }

  const handleDelete = async (id) => {
    try {
      await ElMessageBox.confirm(
        `Are you sure to delete this ${entityName}?`,
        'Warning',
        { confirmButtonText: 'Confirm', cancelButtonText: 'Cancel', type: 'warning' }
      )
      loading.value = true
      await del(id)
      ElMessage.success('Deleted successfully')
      await fetch()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error(`Failed to delete ${entityName}`)
      }
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    dialogVisible,
    isEditing,
    formData,
    loadData,
    handleAdd,
    handleEdit,
    handleSave,
    handleDelete,
  }
}
