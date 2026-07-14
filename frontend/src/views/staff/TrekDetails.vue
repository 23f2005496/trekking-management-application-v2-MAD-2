<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            trek: null,
            bookings: [],
            slotValue: 0,
            statusValue: "Open",
            error: ""
        }
    },

    mounted() {
        this.fetchTrek()
    },

    methods: {
        async fetchTrek() {
            try {
                const response = await api.get(`/staff/trek-details/${this.$route.params.id}`)
                this.trek = response.data.trek
                this.bookings = response.data.bookings
                this.slotValue = this.trek.slots
                this.statusValue = this.trek.status
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async updateSlots() {
            if (!confirm("Update the available slots?")) {
                return
            }

            try {
                const response = await api.post(`/staff/trek/${this.trek.id}/update-slots`, {
                    slots: this.slotValue
                })
                this.trek = response.data.trek
                setFlash(response.data.message, "success")
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async changeStatus() {
            if (!confirm("Change this trek status?")) {
                return
            }

            try {
                const response = await api.post(`/staff/trek/${this.trek.id}/change-status`, {
                    status: this.statusValue
                })
                setFlash(response.data.message, "success")
                await this.fetchTrek()
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
    <h1 class="page-title">Trek Details</h1>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <section v-if="trek" class="mb-6">
        <div class="row gap-6">
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <RouterLink :to="{ name: trek.status !== 'Completed' ? 'assigned-treks' : 'staff-history' }">
                            <i class="fa-solid fa-arrow-left"></i>
                            Back to {{ trek.status !== 'Completed' ? 'Treks' : 'History' }}
                        </RouterLink>

                        <h1 class="mb-1 text-center">{{ trek.name }}</h1>

                        <div class="row gap-16 mt-6">
                            <div>
                                <img :src="trek.image_url" class="image" alt="Trek image">
                            </div>

                            <div>
                                <div class="detail-item">
                                    <span class="detail-key">Location :</span>
                                    <span class="detail-value ml-6">{{ trek.location }}</span>
                                </div>

                                <div class="detail-item">
                                    <span class="detail-key">Difficulty :</span>
                                    <span class="detail-value ml-6">{{ trek.difficulty }}</span>
                                </div>

                                <div class="detail-item">
                                    <span class="detail-key">Duration :</span>
                                    <span class="detail-value ml-6">{{ trek.duration }}</span>
                                </div>

                                <div class="detail-item" v-if="trek.status !== 'Completed'">
                                    <span class="detail-key">Available Slots :</span>
                                    <span class="detail-value ml-6">
                                        <form class="detail-form" @submit.prevent="updateSlots">
                                            <div class="d-flex gap-8">
                                                <input type="number" v-model="slotValue" min="0"
                                                    class="detail-input form-control">
                                                <button class="btn btn-success btn-md">
                                                    Update
                                                </button>
                                            </div>
                                        </form>
                                    </span>
                                </div>

                                <div class="detail-item" v-else>
                                    <span class="detail-key">Available Slots :</span>
                                    <span class="detail-value ml-6">{{ trek.slots }}</span>
                                </div>

                                <div class="detail-item" v-if="trek.status !== 'Completed'">
                                    <span class="detail-key">Status :</span>
                                    <span class="detail-value ml-6">
                                        <form class="detail-form" @submit.prevent="changeStatus">
                                            <div class="d-flex gap-8">
                                                <select v-model="statusValue" class="form-control detail-select">
                                                    <option>Open</option>
                                                    <option>Closed</option>
                                                    <option>Ongoing</option>
                                                    <option>Completed</option>
                                                </select>
                                                <button class="btn btn-info btn-md">
                                                    Change
                                                </button>
                                            </div>
                                        </form>
                                    </span>
                                </div>

                                <div class="detail-item" v-else>
                                    <span class="detail-key">Status :</span>
                                    <span class="detail-value ml-6">
                                        <span class="badge" :class="badgeClass(trek.status)">
                                            {{ trek.status }}
                                        </span>
                                    </span>
                                </div>

                                <div class="detail-item">
                                    <span class="detail-key">Start Date :</span>
                                    <span class="detail-value ml-6">{{ trek.start_date_label }}</span>
                                </div>

                                <div class="detail-item">
                                    <span class="detail-key">End Date :</span>
                                    <span class="detail-value ml-6">{{ trek.end_date_label }}</span>
                                </div>

                                <div class="detail-item">
                                    <span class="detail-key">Bookings :</span>
                                    <span class="detail-value ml-6">{{ bookings.length }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section v-if="trek" class="mb-6">
        <div class="card">
            <div class="card-body">
                <h2 class="mb-3">Participants ({{ bookings.length }})</h2>
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Full Name</th>
                                <th>Email</th>
                                <th>Contact</th>
                                <th>Booking Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="booking in bookings" :key="booking.id">
                                <td>{{ booking.user.full_name }}</td>
                                <td>{{ booking.user.email }}</td>
                                <td>{{ booking.user.contact || "No Contact" }}</td>
                                <td>{{ booking.booking_date_label }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(booking.status)">
                                        {{ booking.status }}
                                    </span>
                                </td>
                            </tr>
                            <tr v-if="bookings.length === 0">
                                <td colspan="5" class="text-center text-gray">No participants</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>
