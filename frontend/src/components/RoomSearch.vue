<template>
  <div class="p-4 max-w-5xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">Search Rooms</h2>

    <!-- Filters -->
    <div class="mb-6 flex gap-2 flex-wrap items-end">
      <div>
        <label class="block mb-1">Check-In</label>
        <input v-model="checkIn" type="date" class="border p-2 rounded w-full" />
      </div>
      <div>
        <label class="block mb-1">Check-Out</label>
        <input v-model="checkOut" type="date" class="border p-2 rounded w-full" />
      </div>
      <div>
        <label class="block mb-1">Min Price</label>
        <input v-model.number="minPrice" type="number" placeholder="Min" class="border p-2 rounded w-full" />
      </div>
      <div>
        <label class="block mb-1">Max Price</label>
        <input v-model.number="maxPrice" type="number" placeholder="Max" class="border p-2 rounded w-full" />
      </div>
      <button @click="searchRooms" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        Search
      </button>
    </div>

    <!-- Room List -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="room in rooms" :key="room.id" class="border rounded shadow p-4 hover:shadow-lg transition">
        <h3 class="font-bold text-lg mb-2">{{ room.name || room.number || 'Room' }}</h3>
        <p class="mb-2"><strong>Price:</strong> ${{ room.price }}</p>
        <p class="mb-2"><strong>Capacity:</strong> {{ room.capacity }}</p>
        <p class="mb-2"><strong>Amenities:</strong> {{(room.amenities?.map(a => a.name) || []).join(', ') || '-'}}</p>
        <div class="flex gap-2 mt-2">
          <router-link :to="`/rooms/${room.id}`" class="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600">
            View Detail
          </router-link>
          <router-link :to="`/book/${room.id}`" class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
            Book
          </router-link>
        </div>
      </div>
      <div v-if="rooms.length === 0" class="col-span-full text-center text-gray-500 py-10">
        No rooms found.
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

export default {
  setup() {
    const rooms = ref<any[]>([])

    // Default check-in/out dates
    const today = new Date()
    const tomorrow = new Date()
    tomorrow.setDate(today.getDate() + 1)
    const formatDate = (date: Date) => date.toISOString().split('T')[0]

    const checkIn = ref(formatDate(today))
    const checkOut = ref(formatDate(tomorrow))
    const minPrice = ref<number | null>(null)
    const maxPrice = ref<number | null>(null)

    const searchRooms = async () => {
      const params: any = {}
      if (checkIn.value) params.check_in = checkIn.value
      if (checkOut.value) params.check_out = checkOut.value
      if (minPrice.value) params.min_price = minPrice.value
      if (maxPrice.value) params.max_price = maxPrice.value

      try {
        const res = await api.get('/rooms', { params })
        rooms.value = res.data
      } catch (err: any) {
        console.error('Failed to fetch rooms', err)
      }
    }

    // Load initial rooms on mount
    onMounted(() => {
      searchRooms()
    })

    return { rooms, checkIn, checkOut, minPrice, maxPrice, searchRooms }
  }
}
</script>

<style scoped>
/* Optional hover effect for room cards */
.room-card {
  transition: transform 0.2s;
}

.room-card:hover {
  transform: scale(1.05);
}
</style>
