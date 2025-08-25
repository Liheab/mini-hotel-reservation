<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Navigation Bar -->
    <nav class="bg-blue-600 text-white p-4 flex justify-between items-center">
      <div class="flex gap-4">
        <router-link to="/" class="hover:underline font-semibold">Home</router-link>
        <router-link to="/bookings" class="hover:underline">My Bookings</router-link>
      </div>
      <div class="flex gap-4">
        <router-link to="/staff" class="hover:underline">Staff Dashboard</router-link>
      </div>
    </nav>

    <!-- Main content -->
    <main class="p-6 flex-1 max-w-6xl mx-auto w-full">
      <router-view></router-view>
    </main>

  </div>
</template>

<script lang="ts">
export default { name: 'App' }
</script>

<style scoped>
/* Optional: smooth link hover effects */
a:hover {
  text-decoration: underline;
}
</style>
