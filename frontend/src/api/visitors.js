import api from './index'

export const createVisitor = (data) => api.post('/visitors', data)
export const getVisitors = (params) => api.get('/visitors', { params })
export const getMyVisitors = (params) => api.get('/visitors/my', { params })
export const getVisitor = (id) => api.get(`/visitors/${id}`)
export const approveVisitor = (id) => api.put(`/visitors/${id}/approve`)
export const rejectVisitor = (id) => api.put(`/visitors/${id}/reject`)
export const completeVisitor = (id) => api.put(`/visitors/${id}/complete`)
