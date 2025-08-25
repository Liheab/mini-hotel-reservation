<template>
    <div class="p-6 max-w-xl mx-auto border rounded shadow">
        <h2 class="text-xl font-bold mb-4">Booking Detail</h2>

        <div v-if="booking">
            <p><strong>Guest:</strong> {{ booking.guest.first_name }} {{ booking.guest.last_name }}</p>
            <p><strong>Email:</strong> {{ booking.guest.email }}</p>
            <p><strong>Phone:</strong> {{ booking.guest.phone || '-' }}</p>
            <p><strong>Room:</strong> {{ booking.room.name || booking.room.number }}</p>
            <p><strong>Check-in:</strong> {{ booking.check_in }}</p>
            <p><strong>Check-out:</strong> {{ booking.check_out }}</p>
            <p><strong>Status:</strong> {{ booking.status }}</p>
            <p><strong>Total Price:</strong> ${{ booking.total_price }}</p>

            <div class="flex gap-2 mt-4">
                <button v-if="booking.status !== 'CANCELLED'" @click="cancelBooking"
                    class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
                    Cancel Booking
                </button>
                <router-link to="/bookings" class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400">
                    ← Back to My Bookings
                </router-link>
            </div>
        </div>
        <div v-else class="text-center text-gray-500 py-10">Loading booking...</div>
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
        const booking = ref<any>(null)

        const loadBooking = async () => {
            try {
                const res = await api.get(`/bookings/${route.params.bookingId}`)
                booking.value = res.data
            } catch (err: any) {
                console.error('Failed to load booking', err)
            }
        }

        const cancelBooking = async () => {
            if (!window.confirm('Are you sure you want to cancel this booking?')) return
            try {
                await api.patch(`/bookings/${booking.value.id}`, { status: 'CANCELLED' })
                booking.value.status = 'CANCELLED'
                alert('Booking cancelled')
            } catch (err: any) {
                console.error('Cancel failed', err)
                alert('Failed to cancel booking')
            }
        }

        onMounted(loadBooking)

        return { booking, cancelBooking }
    }
}
</script>
