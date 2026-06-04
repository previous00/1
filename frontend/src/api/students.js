import api from './index'

export const getStudents = (params) => api.get('/students', { params })
export const getStudent = (id) => api.get(`/students/${id}`)
export const createStudent = (data) => api.post('/students', data)
export const updateStudent = (id, data) => api.put(`/students/${id}`, data)
export const checkinStudent = (id, data) => api.put(`/students/${id}/checkin`, data)
export const checkoutStudent = (id) => api.put(`/students/${id}/checkout`)
