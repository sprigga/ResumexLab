import apiClient from './axios'

/**
 * Factory function that creates a standard CRUD API object for a given entity path.
 * Generates: getAll, get(id), create(data), update(id, data), delete(id)
 */
export function createCrudApi(entityPath) {
  return {
    getAll: () => apiClient.get(`/${entityPath}/`),
    get: (id) => apiClient.get(`/${entityPath}/${id}`),
    create: (data) => apiClient.post(`/${entityPath}/`, data),
    update: (id, data) => apiClient.put(`/${entityPath}/${id}`, data),
    delete: (id) => apiClient.delete(`/${entityPath}/${id}`),
  }
}
