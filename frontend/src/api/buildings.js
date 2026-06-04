import api from './index'

export const getBuildings = () => api.get('/buildings')
export const createBuilding = (data) => api.post('/buildings', data)
export const updateBuilding = (id, data) => api.put(`/buildings/${id}`, data)
export const deleteBuilding = (id) => api.delete(`/buildings/${id}`)
export const getBuildingRooms = (id) => api.get(`/buildings/${id}/rooms`)

export const getRooms = (params) => api.get('/rooms', { params })
export const createRoom = (data) => api.post('/rooms', data)
export const updateRoom = (id, data) => api.put(`/rooms/${id}`, data)
export const deleteRoom = (id) => api.delete(`/rooms/${id}`)
