<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">Staff Dashboard</h1>

    <!-- Success / Error Messages -->
    <div v-if="successMessage" class="mb-4 p-2 bg-green-100 border border-green-300 text-green-800 rounded">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="mb-4 p-2 bg-red-100 border border-red-300 text-red-800 rounded">
      {{ errorMessage }}
    </div>

    <!-- Tabs -->
    <div class="flex gap-2 mb-6">
      <button @click="activeTab = 'rooms'"
        :class="activeTab === 'rooms' ? 'px-4 py-2 bg-blue-600 text-white rounded' : 'px-4 py-2 bg-gray-200 rounded'">
        Rooms
      </button>
      <button @click="activeTab = 'bookings'"
        :class="activeTab === 'bookings' ? 'px-4 py-2 bg-blue-600 text-white rounded' : 'px-4 py-2 bg-gray-200 rounded'">
        Bookings
      </button>
    </div>

    <!-- ROOMS TABLE -->
    <section v-if="activeTab === 'rooms'">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Rooms</h2>
        <router-link to="/staff/rooms/add"
          class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition">+ Add Room</router-link>
      </div>
      <!-- Search -->
      <div class="mb-2">
        <input v-model="roomSearch" type="text" placeholder="Search by number, name, type ..."
          class="border p-1 rounded w-64" />
      </div>


      <div class="overflow-x-auto bg-white rounded shadow">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="p-2 border">ID</th>
              <th class="p-2 border">Number</th>
              <th class="p-2 border">Name</th>
              <th class="p-2 border">Type</th>
              <th class="p-2 border">Price</th>
              <th class="p-2 border">Capacity</th>
              <th class="p-2 border">Description</th>
              <th class="p-2 border">Amenities</th>
              <th class="p-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="room in filteredRooms" :key="room.id" class="hover:bg-gray-50">
              <td class="p-2 border">{{ room.id }}</td>
              <td class="p-2 border">{{ room.number || '-' }}</td>
              <td class="p-2 border">{{ room.name || '-' }}</td>
              <td class="p-2 border">{{ room.room_type || '-' }}</td>
              <td class="p-2 border">${{ room.price || '-' }}</td>
              <td class="p-2 border">{{ room.capacity || '-' }}</td>
              <td class="p-2 border">{{ room.description || '-' }}</td>
              <td class="p-2 border">{{(room.amenities?.map(a => a.name) || []).join(', ') || '-'}}</td>
              <td class="p-2 border">
                <div class="flex items-center gap-4">
                  <router-link :to="`/staff/rooms/${room.id}/edit`" class="text-blue-600 hover:underline">
                    Edit
                  </router-link>
                  <button @click="confirmDelete(room.id)" class="text-red-600 hover:underline">Delete</button>
                </div>
              </td>
            </tr>

            <tr v-if="filteredRooms.length === 0">
              <td colspan="9" class="p-4 text-center text-gray-500">No rooms found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- BOOKINGS TABLE -->
    <section v-if="activeTab === 'bookings'" class="mt-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Bookings</h2>
      </div>

      <!-- Filters -->
      <div class="flex gap-2 mb-4 flex-wrap items-end">

        <div>
          <label class="block mb-1 text-sm">Check-in From</label>
          <input v-model="filterCheckInFrom" type="date" class="border p-2 rounded" />
        </div>
        <div>
          <label class="block mb-1 text-sm">Check-in To</label>
          <input v-model="filterCheckInTo" type="date" class="border p-2 rounded" />
        </div>
        <div>
          <label class="block mb-1 text-sm">Status</label>
          <select v-model="filterStatus" class="border p-2 rounded">
            <option value="">All</option>
            <option value="CONFIRMED">Confirmed</option>
            <option value="CANCELLED">Cancelled</option>
            <option value="PENDING">Pending</option>
          </select>
        </div>
        <button @click="applyFilters" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Apply
          Filters</button>
        <button @click="resetFilters"
          class="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400">Reset</button>
      </div>

      <div class="overflow-x-auto bg-white rounded shadow">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="p-2 border">ID</th>
              <th class="p-2 border">Guest</th>
              <th class="p-2 border">Room</th>
              <th class="p-2 border">Status</th>
              <th class="p-2 border">Check-in</th>
              <th class="p-2 border">Check-out</th>
              <th class="p-2 border">Total Price</th>
              <th class="p-2 border">Payment</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in filteredBookings" :key="booking.id" class="hover:bg-gray-50 cursor-pointer"
              @click="goToBookingDetail(booking.id)">
              <td class="p-2 border">{{ booking.id }}</td>
              <td class="p-2 border">{{ booking.guest.first_name }} {{ booking.guest.last_name }}</td>
              <td class="p-2 border">{{ booking.room.number || booking.room.name || '-' }}</td>
              <td class="p-2 border">{{ booking.status }}</td>
              <td class="p-2 border">{{ booking.check_in }}</td>
              <td class="p-2 border">{{ booking.check_out }}</td>
              <td class="p-2 border">${{ booking.total_price }}</td>
              <td class="p-2 border">{{ booking.payment_status }}</td>
            </tr>

            <tr v-if="filteredBookings.length === 0">
              <td colspan="8" class="p-4 text-center text-gray-500">No bookings found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/api'

const router = useRouter()
const route = useRoute()

const activeTab = ref<'rooms' | 'bookings'>('rooms')
const rooms = ref<any[]>([])
const bookings = ref<any[]>([])
const filteredBookings = ref<any[]>([])
const errorMessage = ref('')
const successMessage = ref('')
const today = new Date()
const tomorrow = new Date()
tomorrow.setDate(today.getDate() + 7)
const formatDate = (date: Date) => date.toISOString().split('T')[0]

// Rooms search
const roomSearch = ref('')

// Filter states
const filterStatus = ref('')
const filterCheckInFrom = ref(formatDate(today))
const filterCheckInTo = ref(formatDate(tomorrow))


// Load data
const loadRooms = async () => {
  try {
    const res = await api.get('/rooms')
    rooms.value = res.data
  } catch (err: any) {
    console.error(err)
    errorMessage.value = 'Failed to load rooms'
  }
}

const loadBookings = async () => {
  try {
    const res = await api.get('/bookings')
    bookings.value = res.data
    filteredBookings.value = [...bookings.value]
  } catch (err: any) {
    console.error(err)
    errorMessage.value = 'Failed to load bookings'
  }
}

const filteredRooms = computed(() => {
  const search = roomSearch.value.toLowerCase()
  return rooms.value.filter(r => {
    return (
      r.number?.toLowerCase().includes(search) ||
      r.name?.toLowerCase().includes(search) ||
      r.room_type?.toLowerCase().includes(search) ||
      r.description?.toLowerCase().includes(search) ||
      r.price?.toString().toLowerCase().includes(search) ||
      r.capacity?.toString().toLowerCase().includes(search) ||
      r.amenities?.some(a => a.name.toLowerCase().includes(search))
    )
  })
})

onMounted(async () => {
  if (route.query.success) {
    successMessage.value = String(route.query.success)
    setTimeout(() => (successMessage.value = ''), 3000)
  }
  await Promise.all([loadRooms(), loadBookings()])
})

// Filter methods
const applyFilters = () => {
  filteredBookings.value = bookings.value.filter((b) => {
    let statusMatch = true
    let checkInMatch = true

    if (filterStatus.value) statusMatch = b.status === filterStatus.value
    if (filterCheckInFrom.value) checkInMatch = new Date(b.check_in) >= new Date(filterCheckInFrom.value)
    if (checkInMatch && filterCheckInTo.value) checkInMatch = new Date(b.check_in) <= new Date(filterCheckInTo.value)

    return statusMatch && checkInMatch
  })
}

const resetFilters = () => {
  filterStatus.value = ''
  filterCheckInFrom.value = ''
  filterCheckInTo.value = ''
  filteredBookings.value = [...bookings.value]
}

// Room actions
const confirmDelete = (id: number) => {
  if (window.confirm('Are you sure you want to delete this room?')) {
    deleteRoom(id)
  }
}

const deleteRoom = async (id: number) => {
  try {
    await api.delete(`/rooms/${id}`)
    rooms.value = rooms.value.filter(r => r.id !== id)
    successMessage.value = 'Room deleted successfully'
    setTimeout(() => (successMessage.value = ''), 3000)
  } catch (err: any) {
    console.error(err)
    errorMessage.value = 'Failed to delete room'
  }
}

// Navigate to booking detail
const goToBookingDetail = (id: number) => {
  router.push(`/staff/bookings/${id}`)
}
</script>
