import api from './index'

export const enrollFace = (formData) => api.post('/faces/enroll', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const getMyFaces = () => api.get('/faces/my')
export const deleteFace = (id) => api.delete(`/faces/${id}`)
export const verifyFace = (formData) => api.post('/faces/verify', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const faceAccess = (formData) => api.post('/faces/access', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
