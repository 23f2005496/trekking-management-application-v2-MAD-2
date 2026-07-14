<script>
import api from "@/services/api"

export default {

    data() {

        return {

            all_bookings: [],
            error: ""

        }

    },

    mounted() {

        this.fetchBookings()

    },

    methods: {

        async fetchBookings() {

            try {

                const response = await api.get("/admin/bookings")
                this.all_bookings = response.data.bookings

            }

            catch (error) {

                this.error = error.response?.data?.message || error.message

            }

        },

        badgeClass(status) {
            return (status || "").toLowerCase()
        }

    }

}
</script>

<template>

    <h1 class="page-title">All Bookings</h1>

    <div v-if="error" class="alert alert-error">
        {{ error }}
    </div>

    <section class="mb-6">

        <div class="card">

            <div class="card-body">

                <div class="table-container">

                    <table class="table">

                        <thead>

                            <tr>
                                <th>Booking ID</th>
                                <th>Trekker</th>
                                <th>Trek</th>
                                <th>Booking Date</th>
                                <th>Status</th>
                            </tr>

                        </thead>

                        <tbody>

                            <tr v-for="(booking, index) in all_bookings" :key="booking.id">

                                <td>B00{{ index + 1 }}</td>

                                <td>{{ booking.user.full_name }}</td>

                                <td>{{ booking.trek.name }}</td>

                                <td>{{ booking.booking_date_label }}</td>

                                <td>

                                    <span class="badge" :class="badgeClass(booking.status)">
                                        {{ booking.status }}
                                    </span>

                                </td>

                            </tr>
                            <tr v-if="all_bookings.length === 0">
                                <td colspan="5" class="text-center text-gray">No bookings</td>
                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

        </div>

    </section>

</template>
