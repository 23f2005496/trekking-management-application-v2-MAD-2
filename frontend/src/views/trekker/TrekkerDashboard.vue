<script>
import api from "@/services/api"
import { getUser } from "@/services/auth"

export default {
    data() {
        return {
            total_bookings: 0,
            cancelled_bookings: 0,
            completed_treks: 0,
            upcoming_treks: [],
            error: ""
        }
    },

    computed: {
        user() {
            return getUser()
        }
    },

    mounted() {
        this.fetchDashboard()
    },

    methods: {
        async fetchDashboard() {
            try {
                const response = await api.get("/trekker/dashboard")
                this.total_bookings = response.data.total_bookings
                this.cancelled_bookings = response.data.cancelled_bookings
                this.completed_treks = response.data.completed_treks
                this.upcoming_treks = response.data.upcoming_treks
                this.error = ""
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

    <h1 class="page-title">Welcome, {{ user?.full_name }}!</h1>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <section class="mb-6">
        <div class="card">
            <div class="card-body">
                <h2 class="mb-3">Your Journey</h2>

                <div class="row gap-6">
                    <div class="col">
                        <div class="card bg-gray">
                            <div class="card-body">
                                <h3 class="mb-3">Total Bookings</h3>
                                <div class="detail-item gap-12">
                                    <h1 class="detail-key">{{ total_bookings }}</h1>
                                    <h1 class="detail-value"><i class="fa-solid fa-mountain-sun"></i></h1>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col">
                        <div class="card bg-gray">
                            <div class="card-body">
                                <h3 class="mb-3">Cancelled Bookings</h3>
                                <div class="detail-item gap-12">
                                    <h1 class="detail-key">{{ cancelled_bookings }}</h1>
                                    <h1 class="detail-value"><i class="fa-solid fa-xmark"></i></h1>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col">
                        <div class="card bg-gray">
                            <div class="card-body">
                                <h3 class="mb-3">Completed Treks</h3>
                                <div class="detail-item gap-12">
                                    <h1 class="detail-key">{{ completed_treks }}</h1>
                                    <h1 class="detail-value"><i class="fa-solid fa-calendar-check"></i></h1>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col">
                        <div class="card bg-gray">
                            <div class="card-body">
                                <h3 class="mb-3">Upcoming Treks</h3>
                                <div class="detail-item gap-12">
                                    <h1 class="detail-key">{{ upcoming_treks.length }}</h1>
                                    <h1 class="detail-value"><i class="fa-solid fa-arrow-up-right-dots"></i></h1>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </section>

    <section class="mb-6">
        <div class="card">
            <div class="card-body">
                <h2 class="mb-3">Upcoming Treks</h2>
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Trek Name</th>
                                <th>Location</th>
                                <th>Difficulty</th>
                                <th>Duration</th>
                                <th>Start Date</th>
                                <th>End Date</th>
                                <th>Status</th>
                                <th>Assigned Staff</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="trek in upcoming_treks" :key="trek.id">
                                <td>{{ trek.name }}</td>
                                <td>{{ trek.location }}</td>
                                <td>{{ trek.difficulty }}</td>
                                <td>{{ trek.duration }}</td>
                                <td>{{ trek.start_date_label }}</td>
                                <td>{{ trek.end_date_label }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(trek.status)">
                                        {{ trek.status }}
                                    </span>
                                </td>
                                <td>{{ trek.staff?.full_name || "Not Assigned" }}</td>
                            </tr>
                            <tr v-if="upcoming_treks.length === 0">
                                <td colspan="8" class="text-center text-gray">No upcoming treks</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>

</template>
