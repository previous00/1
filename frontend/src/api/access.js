import api from './index'

export const getAccessLogs = (params) => api.get('/access/logs', { params })
export const getMyAccessLogs = (params) => api.get('/access/logs/my', { params })
export const getAccessLog = (id) => api.get(`/access/logs/${id}`)
export const manualEntry = (data) => api.post('/access/manual', data)
