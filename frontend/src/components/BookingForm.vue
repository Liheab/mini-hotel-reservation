<template>
  <div class="p-4 max-w-md mx-auto">
    <h2 class="text-xl font-bold mb-4">Book Room</h2>

    <form @submit.prevent="submitBooking" class="space-y-4">
      <!-- Guest First Name -->
      <div>
        <label class="block mb-1">First Name *</label>
        <input v-model="firstName" type="text" class="border p-2 w-full rounded" placeholder="First Name" />
        <p v-if="errors.first_name" class="text-red-600 text-sm mt-1">
          {{ Array.isArray(errors.first_name) ? errors.first_name[0] : errors.first_name }}
        </p>
      </div>

      <!-- Guest Last Name -->
      <div>
        <label class="block mb-1">Last Name *</label>
        <input v-model="lastName" type="text" class="border p-2 w-full rounded" placeholder="Last Name" />
        <p v-if="errors.last_name" class="text-red-600 text-sm mt-1">
          {{ Array.isArray(errors.last_name) ? errors.last_name[0] : errors.last_name }}
        </p>
      </div>

      <!-- Guest Email -->
      <div>
        <label class="block mb-1">Email *</label>
        <input v-model="email" type="email" class="border p-2 w-full rounded" placeholder="Email" />
        <p v-if="errors.email" class="text-red-600 text-sm mt-1">
          {{ Array.isArray(errors.email) ? errors.email[0] : errors.email }}
        </p>
      </div>

      <!-- Guest Phone -->
      <div>
        <label class="block mb-1">Phone</label>
        <input v-model="phone" type="text" class="border p-2 w-full rounded" placeholder="Phone" />
        <p v-if="errors.phone" class="text-red-600 text-sm mt-1">
          {{ Array.isArray(errors.phone) ? errors.phone[0] : errors.phone }}
        </p>
      </div>

      <!-- Check-in Date -->
      <div>
        <label class="block mb-1">Check-In *</label>
        <input v-model="checkIn" type="date" class="border p-2 w-full rounded" />
        <p v-if="errors.check_in" class="text-red-600 text-sm mt-1">
          {{ Array.isArray(errors.check_in) ? errors.check_in[0] : errors.check_in }}
        </p>
      </div>

      <!-- Check-out Date -->
      <div>
        <label class="block mb-1">Check-Out *</label>
        <input v-model="checkOut" type="date" class="border p-2 w-full rounded" />
        <p v-if="errors.check_out" class="text-red-600 text-sm mt-1">
          {{ Array.isArray(errors.check_out) ? errors.check_out[0] : errors.check_out }}
        </p>
      </div>

      <!-- Submit -->
      <div>
        <button type="submit" class="bg-green-500 hover:bg-green-600 text-white p-2 w-full rounded">
          Book Now
        </button>
      </div>
    </form>

    <!-- Message -->
    <div v-if="message || successMessage" :class="`mt-2 p-2 rounded text-center ${messageTypeClass}`">
      {{ message || successMessage }}
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
    const roomId = route.params.roomId as string

    const firstName = ref('')
    const lastName = ref('')
    const email = ref('')
    const phone = ref('')
    const checkIn = ref('')
    const checkOut = ref('')
    const message = ref('')
    const successMessage = ref('')
    const messageTypeClass = ref('bg-green-100 text-green-700')
    const errors = ref<{ [key: string]: string | string[] }>({})

    onMounted(() => {
      const today = new Date()
      const tomorrow = new Date()
      tomorrow.setDate(today.getDate() + 1)
      const formatDate = (date: Date) => date.toISOString().split('T')[0]
      checkIn.value = formatDate(today)
      checkOut.value = formatDate(tomorrow)
    })

    const submitBooking = async () => {
      errors.value = {}
      message.value = ''
      successMessage.value = ''

      if (!firstName.value || !lastName.value || !email.value || !checkIn.value || !checkOut.value) {
        message.value = 'Please fill all required fields'
        messageTypeClass.value = 'bg-red-100 text-red-700'
        return
      }

      const payload = {
        room: Number(roomId),
        guest: {
          first_name: firstName.value,
          last_name: lastName.value,
          email: email.value,
          phone: phone.value
        },
        check_in: checkIn.value,
        check_out: checkOut.value,
        status: 'PENDING',
        total_price: '0.00',
        payment_status: 'PENDING'
      }

      try {
        const res = await api.post('/bookings', payload)
        successMessage.value = 'Booking successful!'
        messageTypeClass.value = 'bg-green-100 text-green-700'
        setTimeout(() => router.push(`/payment/${res.data.id}`), 1000)
      } catch (err: any) {
        if (err.response?.data) {
          const data = err.response.data

          if (data.guest) Object.assign(errors.value, data.guest)

          Object.assign(errors.value, data)

          if (data.non_field_errors) {
            message.value = data.non_field_errors.join(', ')
          }
        } else {
          message.value = 'Booking failed'
        }
        messageTypeClass.value = 'bg-red-100 text-red-700'
      }
    }

    return {
      firstName, lastName, email, phone,
      checkIn, checkOut,
      submitBooking, message, successMessage, errors,
      messageTypeClass
    }
  }
}
</script>
