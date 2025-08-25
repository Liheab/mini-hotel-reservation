<template>
    <div class="p-6 max-w-xl mx-auto border rounded shadow">
        <h2 class="text-xl font-bold mb-4">{{ room.name || room.number }}</h2>
        <p class="mb-2"><strong>Number:</strong> {{ room.number }}</p>
        <p class="mb-2"><strong>Type:</strong> {{ room.room_type }}</p>
        <p class="mb-2"><strong>Price:</strong> ${{ room.price }}</p>
        <p class="mb-2"><strong>Capacity:</strong> {{ room.capacity }}</p>
        <p class="mb-2"><strong>Description:</strong> {{ room.description }}</p>
        <p class="mb-2"><strong>Amenities:</strong> {{(room.amenities?.map(a => a.name) || []).join(', ')}}</p>

        <div class="mt-4 flex gap-2">
            <router-link :to="`/book/${room.id}`"
                class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition">
                Book This Room
            </router-link>

            <!-- Use router.back() if you want to go to the previous page -->
            <button @click="goBack" class="text-blue-600 hover:underline px-4 py-2">
                ← Back to Search
            </button>
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
        const room = ref<any>({})

        const goBack = () => {
            router.back() // This goes to the previous page (works even if not exactly /rooms)
        }

        onMounted(async () => {
            try {
                const res = await api.get(`/rooms/${route.params.roomId}`)
                room.value = res.data
            } catch (err: any) {
                console.error('Failed to load room detail', err)
            }
        })

        return { room, goBack }
    }
}
</script>
