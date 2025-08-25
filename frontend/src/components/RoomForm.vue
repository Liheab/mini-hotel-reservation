<template>
  <div class="p-4 max-w-3xl mx-auto">
    <h2 class="text-xl font-bold mb-4">{{ roomId ? 'Edit Room' : 'Add Room' }}</h2>

    <form @submit.prevent="submitRoom" class="grid grid-cols-1 md:grid-cols-2 gap-4">

      <!-- Room Number -->
      <div>
        <label for="roomNumber" class="block font-medium mb-1">Room Number *</label>
        <input id="roomNumber" v-model="number" type="text" placeholder="Enter room number"
          class="border p-2 w-full rounded" />
        <p v-if="errors.number" class="text-red-600 mt-1 text-sm">
          {{ Array.isArray(errors.number) ? errors.number[0] : errors.number }}
        </p>
      </div>

      <!-- Room Name -->
      <div>
        <label for="roomName" class="block font-medium mb-1">Room Name *</label>
        <input id="roomName" v-model="name" type="text" placeholder="Enter room name"
          class="border p-2 w-full rounded" />
        <p v-if="errors.name" class="text-red-600 mt-1 text-sm">
          {{ Array.isArray(errors.name) ? errors.name[0] : errors.name }}
        </p>
      </div>

      <!-- Room Type -->
      <div>
        <label for="roomType" class="block font-medium mb-1">Room Type *</label>
        <select id="roomType" v-model="roomType" class="border p-2 w-full rounded">
          <option value="">Select room type</option>
          <option v-for="type in room_type_options" :key="type.value" :value="type.value">
            {{ type.label }}
          </option>
        </select>
        <p v-if="errors.room_type" class="text-red-600 mt-1 text-sm">
          {{ Array.isArray(errors.room_type) ? errors.room_type[0] : errors.room_type }}
        </p>
      </div>

      <!-- Price -->
      <div>
        <label for="roomPrice" class="block font-medium mb-1">Price *</label>
        <input id="roomPrice" v-model.number="price" type="number" placeholder="Enter price"
          class="border p-2 w-full rounded" />
        <p v-if="errors.price" class="text-red-600 mt-1 text-sm">
          {{ Array.isArray(errors.price) ? errors.price[0] : errors.price }}
        </p>
      </div>

      <!-- Capacity -->
      <div>
        <label for="roomCapacity" class="block font-medium mb-1">Capacity *</label>
        <input id="roomCapacity" v-model.number="capacity" type="number" placeholder="Enter capacity"
          class="border p-2 w-full rounded" />
        <p v-if="errors.capacity" class="text-red-600 mt-1 text-sm">
          {{ Array.isArray(errors.capacity) ? errors.capacity[0] : errors.capacity }}
        </p>
      </div>

      <!-- Description (span 2 columns) -->
      <div class="md:col-span-2">
        <label for="roomDescription" class="block font-medium mb-1">Description</label>
        <textarea id="roomDescription" v-model="description" placeholder="Enter room description"
          class="border p-2 w-full rounded"></textarea>
        <p v-if="errors.description" class="text-red-600 mt-1 text-sm">
          {{ Array.isArray(errors.description) ? errors.description[0] : errors.description }}
        </p>
      </div>

      <!-- Amenities (span 2 columns) -->
      <div class="md:col-span-2">
        <label for="roomAmenities" class="block font-medium mb-1">Amenities</label>
        <input id="roomAmenities" v-model="amenities" type="text"
          placeholder="Comma-separated amenities (e.g., Wifi, AC)" class="border p-2 w-full rounded" />
        <p v-if="errors.amenities" class="text-red-600 mt-1 text-sm">
          {{ Array.isArray(errors.amenities) ? errors.amenities[0] : errors.amenities }}
        </p>
      </div>

      <!-- Submit Button (span 2 columns) -->
      <div class="md:col-span-2">
        <button type="submit" class="bg-blue-500 text-white p-2 rounded w-full hover:bg-blue-600 transition">
          {{ roomId ? 'Update Room' : 'Add Room' }}
        </button>
      </div>

    </form>

    <!-- Success Message -->
    <div v-if="successMessage" class="mt-4 p-2 bg-green-100 border border-green-400 text-green-700 rounded text-center">
      {{ successMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

export default {
  setup() {
    const route = useRoute()
    const router = useRouter()
    const roomId = route.params.roomId as string | undefined

    const room_type_options = ref([
      { value: 'single', label: 'Single' },
      { value: 'double', label: 'Double' }
    ])
    const roomType = ref('')

    const number = ref('')
    const name = ref('')
    const description = ref('')
    const price = ref<number | null>(null)
    const capacity = ref<number | null>(null)
    const amenities = ref('')
    const successMessage = ref('')
    const errors = ref<{ [key: string]: string | string[] }>({})

    onMounted(async () => {
      if (roomId) {
        try {
          const res = await api.get(`/rooms/${roomId}`)
          const room = res.data
          number.value = room.number
          name.value = room.name
          roomType.value = room.room_type
          description.value = room.description
          price.value = room.price
          capacity.value = room.capacity
          amenities.value = room.amenities.map((a: { name: string }) => a.name).join(', ')
        } catch (err: any) {
          errors.value.general = 'Failed to load room data'
        }
      }
    })

    const submitRoom = async () => {
      errors.value = {}

      const amenitiesArray = amenities.value
        .split(',')
        .map(a => a.trim())
        .filter(a => a)
        .map(a => ({ name: a }))

      const payload = {
        number: number.value,
        name: name.value,
        room_type: roomType.value,
        description: description.value,
        price: price.value,
        capacity: capacity.value,
        amenities: amenitiesArray
      }

      try {
        if (roomId) {
          await api.patch(`/rooms/${roomId}`, payload)
          successMessage.value = 'Room updated successfully!'
        } else {
          await api.post('/rooms', payload)
          successMessage.value = 'Room added successfully!'
        }

        setTimeout(() => router.push('/staff'), 2000)
      } catch (err: any) {
        if (err.response?.data) {
          const data = err.response.data
          Object.assign(errors.value, data)
        } else {
          errors.value.general = 'Failed to save room'
        }
      }
    }

    return {
      number,
      name,
      roomType,
      room_type_options,
      description,
      price,
      capacity,
      amenities,
      submitRoom,
      roomId,
      successMessage,
      errors
    }
  }
}
</script>
