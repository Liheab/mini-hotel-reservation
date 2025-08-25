<template>
    <div class="p-6 max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold mb-4">My Bookings</h2>

        <!-- Filter section -->
        <div class="mb-4 flex flex-wrap gap-2 items-end">
            <div>
                <label class="block text-sm mb-1">Check-In</label>
                <input v-model="filterCheckIn" type="date" class="border p-1 rounded w-32" />
            </div>
            <div>
                <label class="block text-sm mb-1">Check-Out</label>
                <input v-model="filterCheckOut" type="date" class="border p-1 rounded w-32" />
            </div>
            <div>
                <label class="block text-sm mb-1">Status</label>
                <select v-model="filterStatus" class="border p-1 rounded w-32">
                    <option value="">All</option>
                    <option value="CONFIRMED">Confirmed</option>
                    <option value="CANCELLED">Cancelled</option>
                    <option value="COMPLETED">Completed</option>
                </select>
            </div>
            <button @click="applyFilters"
                class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition">Filter</button>
            <button @click="resetFilters"
                class="bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 transition">Reset</button>
        </div>

        <!-- Message -->
        <div v-if="message" class="mb-4 p-2 rounded text-center" :class="messageTypeClass">
            {{ message }}
        </div>

        <!-- Bookings table -->
        <div class="overflow-x-auto bg-white rounded shadow">
            <table class="min-w-full text-sm">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="p-2 border">ID</th>
                        <th class="p-2 border">Room</th>
                        <th class="p-2 border">Check-in</th>
                        <th class="p-2 border">Check-out</th>
                        <th class="p-2 border">Status</th>
                        <th class="p-2 border">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="booking in filteredBookings" :key="booking.id" class="hover:bg-gray-50">
                        <td class="p-2 border">{{ booking.id }}</td>
                        <td class="p-2 border">{{ booking.room.name || booking.room.number }}</td>
                        <td class="p-2 border">{{ booking.check_in }}</td>
                        <td class="p-2 border">{{ booking.check_out }}</td>
                        <td class="p-2 border">{{ booking.status }}</td>
                        <td class="p-2 border flex gap-2">
                            <router-link :to="`/bookings/${booking.id}`" class="text-blue-600 hover:underline">
                                View
                            </router-link>
                            <button v-if="['CONFIRMED', 'PENDING'].includes(booking.status)"
                                @click="cancelBooking(booking.id)" class="text-red-600 hover:underline">
                                Cancel
                            </button>

                        </td>
                    </tr>

                    <tr v-if="filteredBookings.length === 0">
                        <td colspan="6" class="p-4 text-center text-gray-500">No bookings found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/api'

export default {
    setup() {
        const bookings = ref<any[]>([])
        const message = ref('')
        const messageTypeClass = ref('bg-green-100 text-green-700')

        // Default check-in/out dates
        const today = new Date()
        const tomorrow = new Date()
        tomorrow.setDate(today.getDate() + 1)
        const formatDate = (date: Date) => date.toISOString().split('T')[0]

        // Filters
        const filterCheckIn = ref(formatDate(today))
        const filterCheckOut = ref(formatDate(tomorrow))
        const filterStatus = ref('')

        const loadBookings = async () => {
            try {
                const res = await api.get('/bookings') // fetch user's bookings
                bookings.value = res.data
            } catch (err: any) {
                console.error(err)
                message.value = 'Failed to load bookings'
                messageTypeClass.value = 'bg-red-100 text-red-700'
            }
        }

        const cancelBooking = async (id: number) => {
            if (!window.confirm('Are you sure you want to cancel this booking?')) return

            try {
                await api.patch(`/bookings/${id}`, { status: 'CANCELLED' })
                const booking = bookings.value.find(b => b.id === id)
                if (booking) booking.status = 'CANCELLED'
                message.value = 'Booking cancelled successfully'
                messageTypeClass.value = 'bg-green-100 text-green-700'
            } catch (err: any) {
                console.error(err)
                message.value = 'Failed to cancel booking'
                messageTypeClass.value = 'bg-red-100 text-red-700'
            }
        }

        const filteredBookings = computed(() => {
            return bookings.value.filter(b => {
                const checkInMatch = !filterCheckIn.value || b.check_in >= filterCheckIn.value
                const checkOutMatch = !filterCheckOut.value || b.check_out <= filterCheckOut.value
                const statusMatch = !filterStatus.value || b.status === filterStatus.value
                return checkInMatch && checkOutMatch && statusMatch
            })
        })

        const applyFilters = () => {
            // computed takes care of filtering, so no extra code needed
        }

        const resetFilters = () => {
            filterCheckIn.value = ''
            filterCheckOut.value = ''
            filterStatus.value = ''
        }

        onMounted(() => {
            loadBookings()
        })

        return {
            bookings,
            filteredBookings,
            cancelBooking,
            message,
            messageTypeClass,
            filterCheckIn,
            filterCheckOut,
            filterStatus,
            applyFilters,
            resetFilters
        }
    }
}
</script>
