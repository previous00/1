import api from './index'

export const getOverview = () => api.get('/statistics/overview')
export const getAccessTrend = (params) => api.get('/statistics/access-trend', { params })
export const getBuildingRank = () => api.get('/statistics/building-rank')
export const getHourly = () => api.get('/statistics/hourly')
export const getAlertsSummary = () => api.get('/statistics/alerts-summary')
