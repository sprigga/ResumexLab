import { ref } from 'vue'

/**
 * Creates a set of CRUD store functions for a given entity.
 * Reduces the repeated fetch/create/update/delete pattern across all entity types.
 *
 * Each call creates its own isolated loading/error refs to avoid race conditions
 * when multiple entity actions run concurrently.
 *
 * @param {Ref} items - The ref array holding the entity list
 * @param {object} api - Object with getAll, create, update, delete API methods
 * @returns {object} - { fetchAll, create, update, remove, loading, error }
 */
export function createEntityActions(items, api) {
  const loading = ref(false)
  const error = ref(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const response = await api.getAll()
      items.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    loading.value = true
    error.value = null
    try {
      const response = await api.create(data)
      items.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function update(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await api.update(id, data)
      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function remove(id) {
    loading.value = true
    error.value = null
    try {
      await api.delete(id)
      items.value = items.value.filter(item => item.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return { fetchAll, create, update, remove, loading, error }
}

/**
 * Creates a simple async wrapper that sets loading/error state.
 * Used for one-off operations (import, export) that don't manage a list.
 */
export function createAsyncAction(loading, error, apiFn) {
  return async (...args) => {
    loading.value = true
    error.value = null
    try {
      const response = await apiFn(...args)
      return response.data ?? response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
}
