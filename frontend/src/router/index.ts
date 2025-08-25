import { createRouter, createWebHistory } from 'vue-router'
import RoomSearch from '@/components/RoomSearch.vue'
import RoomDetail from '@/components/RoomDetail.vue'
import BookingForm from '@/components/BookingForm.vue'
import Payment from '@/components/Payment.vue'
import StaffDashboard from '@/components/StaffDashboard.vue'
import RoomForm from '@/components/RoomForm.vue'
import BookingDetail from '@/components/BookingDetail.vue'
import StaffBookingDetail from '@/components/StaffBookingDetail.vue'
import BookingList from '@/components/BookingList.vue'

const routes = [
  { path: '/', component: RoomSearch },
  { path: '/rooms/:roomId', component: RoomDetail },
  { path: '/book/:roomId', component: BookingForm },
  { path: '/bookings/:bookingId', component: BookingDetail },
  { path: '/payment/:bookingId', component: Payment },
  { path: '/bookings', component: BookingList },

  // Staff routes
  { path: '/staff', component: StaffDashboard },
  { path: '/staff/rooms/add', component: RoomForm },
  { path: '/staff/rooms/:roomId/edit', component: RoomForm },
  { path: '/staff/bookings/:bookingId', component: StaffBookingDetail },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
