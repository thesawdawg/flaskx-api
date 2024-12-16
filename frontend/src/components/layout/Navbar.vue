<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="bg-primary-600 text-white">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
      <RouterLink to="/" class="text-2xl font-bold">
        Flask Dynamic App
      </RouterLink>
      <div class="space-x-4">
        <RouterLink 
          to="/" 
          class="hover:bg-primary-700 px-3 py-2 rounded transition"
        >
          Home
        </RouterLink>
        <RouterLink 
          to="/users" 
          class="hover:bg-primary-700 px-3 py-2 rounded transition"
        >
          User Management
        </RouterLink>
      </div>
    </div>
  </nav>
</template>
