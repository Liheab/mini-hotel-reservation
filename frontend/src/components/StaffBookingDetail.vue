<template>
    <div class="p-6 max-w-3xl mx-auto bg-white shadow-md rounded-lg">
        <h2 class="text-2xl font-bold mb-6 text-center">Booking Detail</h2>

        <div v-if="booking" class="space-y-4">

            <!-- Guest Information -->
            <div class="p-4 border rounded-lg bg-gray-50">
                <h3 class="text-lg font-semibold mb-2">Guest Information</h3>
                <p><span class="font-medium">Name:</span> {{ booking.guest.first_name }} {{ booking.guest.last_name }}
                </p>
                <p><span class="font-medium">Email:</span> {{ booking.guest.email }}</p>
                <p><span class="font-medium">Phone:</span> {{ booking.guest.phone }}</p>
            </div>

            <!-- Room Information -->
            <div class="p-4 border rounded-lg bg-gray-50">
                <h3 class="text-lg font-semibold mb-2">Room Information</h3>
                <p><span class="font-medium">Room Number:</span> {{ booking.room.number }}</p>
                <p><span class="font-medium">Room Name:</span> {{ booking.room.name || 'N/A' }}</p>
                <p><span class="font-medium">Type:</span> {{ booking.room.room_type }}</p>
                <p><span class="font-medium">Description:</span> {{ booking.room.description }}</p>
                <p><span class="font-medium">Price per night:</span> ${{ booking.room.price }}</p>
                <p><span class="font-medium">Capacity:</span> {{ booking.room.capacity }}</p>
                <p><span class="font-medium">Amenities:</span>
                    <span class="text-gray-700">{{booking.room.amenities.map(a => a.name).join(', ')}}</span>
                </p>
            </div>

            <!-- Booking Details -->
            <div class="p-4 border rounded-lg bg-gray-50">
                <h3 class="text-lg font-semibold mb-2">Booking Details</h3>
                <p><span class="font-medium">Status:</span> {{ booking.status }}</p>
                <p><span class="font-medium">Payment Status:</span> {{ booking.payment_status }}</p>
                <p><span class="font-medium">Total Price:</span> ${{ booking.total_price }}</p>
                <p><span class="font-medium">Check-in:</span> {{ booking.check_in }}</p>
                <p><span class="font-medium">Check-out:</span> {{ booking.check_out }}</p>
                <p><span class="font-medium">Created At:</span> {{ new Date(booking.created_at).toLocaleString() }}</p>
            </div>

        </div>

        <router-link to="/staff"
            class="inline-block mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
            ← Back to Dashboard
        </router-link>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'

const route = useRoute()
const booking = ref<any>(null)

onMounted(async () => {
    try {
        const res = await api.get(`/bookings/${route.params.bookingId}`)
        booking.value = res.data
    } catch (err: any) {
        console.error('Failed to load booking:', err)
    }
})
</script>

<style scoped></style>
