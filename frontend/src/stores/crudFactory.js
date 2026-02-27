import { ref } from 'vue'

/**
 * Creates a set of CRUD store functions for a given entity.
 * Reduces the repeated fetch/create/update/delete pattern across all entity types.
 *
 * @param {Ref} items - The ref array holding the entity list
 * @param {Ref} loading - Shared loading state ref
 * @param {Ref} error - Shared error state ref
 * @param {object} api - Object with getAll, create, update, delete API methods
 * @returns {object} - { fetchAll, create, update, remove }
 */
export function createEntityActions(items, loading, error, api) {
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

  return { fetchAll, create, update, remove }
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
