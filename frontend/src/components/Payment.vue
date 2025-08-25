<template>
  <div class="p-6 max-w-md mx-auto border rounded shadow">
    <h2 class="text-xl font-bold mb-4">Booking Detail</h2>

    <div v-if="booking">
      <p><strong>Guest:</strong> {{ booking.guest.first_name }} {{ booking.guest.last_name }}</p>
      <p><strong>Email:</strong> {{ booking.guest.email }}</p>
      <p><strong>Phone:</strong> {{ booking.guest.phone }}</p>

      <p><strong>Room:</strong> {{ booking.room.name || booking.room.number }}</p>
      <p><strong>Number:</strong> {{ booking.room.number }}</p>
      <p><strong>Type:</strong> {{ booking.room.room_type }}</p>
      <p><strong>Description:</strong> {{ booking.room.description }}</p>
      <p><strong>Capacity:</strong> {{ booking.room.capacity }}</p>
      <p><strong>Price per night:</strong> ${{ booking.room.price }}</p>
      <p><strong>Amenities:</strong> {{booking.room.amenities.map(a => a.name).join(', ')}}</p>

      <p><strong>Check-in:</strong> {{ booking.check_in }}</p>
      <p><strong>Check-out:</strong> {{ booking.check_out }}</p>
      <p><strong>Status:</strong> {{ booking.status }}</p>
      <p><strong>Total Price:</strong> ${{ booking.total_price }}</p>
      <p><strong>Payment Status:</strong> {{ booking.payment_status }}</p>

      <button v-if="booking.payment_status !== 'PAID'" @click="makePayment"
        class="bg-green-500 hover:bg-green-600 text-white p-2 rounded mt-4 w-full">
        Pay Now
      </button>

      <div v-if="message" :class="`mt-2 p-2 text-center rounded ${messageTypeClass}`">{{ message }}</div>

      <router-link to="/bookings" class="inline-block mt-4 text-blue-600 hover:underline">
        ← Back to My Bookings
      </router-link>
    </div>

    <div v-else class="text-center text-red-600">Booking not found.</div>
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
    const bookingId = route.params.bookingId as string

    const booking = ref<any>(null)
    const message = ref('')
    const messageTypeClass = ref('bg-green-100 text-green-700') // success by default

    const fetchBooking = async () => {
      try {
        const res = await api.get(`/bookings/${bookingId}`)
        booking.value = res.data
      } catch (err) {
        booking.value = null
      }
    }

    const makePayment = async () => {
      if (!booking.value) return
      try {
        await api.patch(`/bookings/${bookingId}`, { payment_status: 'PAID' })
        booking.value.payment_status = 'PAID'
        booking.value.status = 'CONFIRMED'
        message.value = 'Payment successful!'
        messageTypeClass.value = 'bg-green-100 text-green-700'
        setTimeout(() => router.push('/bookings'), 1000)
      } catch (err) {
        message.value = 'Payment failed.'
        messageTypeClass.value = 'bg-red-100 text-red-700'
      }
    }

    onMounted(() => fetchBooking())

    return { booking, makePayment, message, messageTypeClass }
  }
}
</script>
