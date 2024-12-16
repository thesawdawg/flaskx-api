<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const newUser = ref({
  username: '',
  email: '',
  password: ''
})
const loading = ref(false)
const error = ref(null)

const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/api/v1/users/')
    users.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch users'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const createUser = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.post('/api/v1/users/', newUser.value)
    users.value.push(response.data)
    newUser.value = { username: '', email: '', password: '' }
  } catch (err) {
    error.value = 'Failed to create user'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)
</script>

<template>
  <div>
    <h1>User Management</h1>
    
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ error }}
    </div>

    <div class="grid md:grid-cols-2 gap-6">
      <div>
        <h2>Create User</h2>
        <form @submit.prevent="createUser" class="bg-white p-6 rounded-lg shadow-md">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Username</label>
            <input 
              v-model="newUser.username" 
              type="text" 
              required 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
            >
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
            <input 
              v-model="newUser.email" 
              type="email" 
              required 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
            >
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Password</label>
            <input 
              v-model="newUser.password" 
              type="password" 
              required 
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
            >
          </div>
          <button 
            type="submit" 
            :disabled="loading"
            class="bg-primary-600 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded"
          >
            {{ loading ? 'Creating...' : 'Create User' }}
          </button>
        </form>
      </div>
      
      <div>
        <h2>User List</h2>
        <div v-if="loading" class="text-center py-4">Loading users...</div>
        <div v-else-if="users.length === 0" class="text-center py-4">No users found</div>
        <ul v-else class="bg-white shadow-md rounded-lg overflow-hidden">
          <li 
            v-for="user in users" 
            :key="user.id" 
            class="px-6 py-4 border-b last:border-b-0 hover:bg-gray-50 transition"
          >
            <div class="flex justify-between">
              <div>
                <p class="font-bold">{{ user.username }}</p>
                <p class="text-gray-600">{{ user.email }}</p>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
