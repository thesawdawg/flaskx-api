<script setup>
import { ref, onMounted } from 'vue'
</script>

<template>
  <div class="text-center">
    <h1>Welcome to Flask Dynamic App</h1>
    <p class="mt-4 text-lg text-gray-600">
      A modern, scalable web application built with Flask and Vue.js
    </p>
    <div class="mt-8 grid md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-primary-600">User Management</h2>
        <p class="mt-2">Create, view, and manage user accounts seamlessly.</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-primary-600">Responsive Design</h2>
        <p class="mt-2">Fully responsive UI that works on desktop and mobile.</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-primary-600">Modern Stack</h2>
        <p class="mt-2">Powered by Flask, Vue.js, and Tailwind CSS.</p>
      </div>
    </div>
  </div>
</template>
