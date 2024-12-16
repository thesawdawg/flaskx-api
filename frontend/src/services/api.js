import axios from 'axios'

const API_BASE_URL = '/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  getUsers() {
    return apiClient.get('/users')
  },
  createUser(userData) {
    return apiClient.post('/users', userData)
  }
}
