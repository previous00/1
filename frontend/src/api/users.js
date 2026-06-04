import api from './index'

export const getUsers = (params) => api.get('/users', { params })
export const getUser = (id) => api.get(`/users/${id}`)
export const updateUser = (id, data) => api.put(`/users/${id}`, data)
export const toggleUserStatus = (id, data) => api.put(`/users/${id}/status`, data)
export const deleteUser = (id) => api.delete(`/users/${id}`)
