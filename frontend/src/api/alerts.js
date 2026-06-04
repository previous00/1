import api from './index'

export const getAlerts = (params) => api.get('/alerts', { params })
export const getAlert = (id) => api.get(`/alerts/${id}`)
export const markAlertRead = (id) => api.put(`/alerts/${id}/read`)
export const resolveAlert = (id) => api.put(`/alerts/${id}/resolve`)
export const getUnreadCount = () => api.get('/alerts/unread-count')
