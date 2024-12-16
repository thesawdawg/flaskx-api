<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <Navbar />
    <main class="container mx-auto px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>

<style>
body {
  @apply text-gray-800;
}
</style>
