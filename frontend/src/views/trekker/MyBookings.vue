<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            my_bookings: [],
            taskId: null,
            error: ""
        }
    },

    mounted() {
        this.fetchBookings()
    },

    methods: {
        async fetchBookings() {
            try {
                const response = await api.get("/trekker/bookings")
                this.my_bookings = response.data.bookings
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async exportCSV() {

            const response = await api.post("/trekker/export-bookings")

            this.taskId = response.data.task_id

            setFlash(response.data.message, "success")

            this.checkStatus()

        },

        async checkStatus() {

            const response = await api.get(`/trekker/export-status/${this.taskId}`)

            setFlash(response.data.message, "success")

            if (response.data.status === "SUCCESS") {

                window.location.href =
                `http://localhost:5000/api/trekker/download/${response.data.filename}`

                clearInterval(this.interval)
            }

        },


        badgeClass(status) {
            return (status || "").toLowerCase()
        }
    }
}
</script>

<template>
    <h1 class="page-title">My Bookings</h1>

    <button @click="exportCSV" class="btn btn-primary btn-md mb-4" v-if="my_bookings.length !== 0">
        <i class="fa-solid fa-download"></i> Download CSV File
    </button>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <section class="mb-6">
        <div class="card">
            <div class="card-body">
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Trek Name</th>
                                <th>Location</th>
                                <th>Duration</th>
                                <th>Trek Dates</th>
                                <th>Booking Status</th>
                                <th>Booking Date</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="booking in my_bookings" :key="booking.id">
                                <td>{{ booking.trek.name }}</td>
                                <td>{{ booking.trek.location }}</td>
                                <td>{{ booking.trek.duration }}</td>
                                <td>{{ booking.trek.start_date_label }} - {{ booking.trek.end_date_label }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(booking.status)">
                                        {{ booking.status }}
                                    </span>
                                </td>
                                <td>{{ booking.booking_date_label }}</td>
                                <td class="action-buttons">
                                    <RouterLink :to="{ name: 'trekker-trek-details', params: { id: booking.trek.id } }"
                                        class="btn btn-outline-info btn-md">
                                        View Details
                                    </RouterLink>
                                </td>
                            </tr>
                            <tr v-if="my_bookings.length === 0">
                                <td colspan="7" class="text-center text-gray">No bookings</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>
