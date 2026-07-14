<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            trek: null,
            booking: null,
            error: ""
        }
    },

    computed: {
        canBook() {
            return this.trek?.status === "Open" && this.booking?.status !== "Booked"
        },

        canCancel() {
            return (this.trek?.status === "Open" || this.trek?.status === "Closed") && this.booking?.status === "Booked"
        }
    },

    mounted() {
        this.fetchTrek()
    },

    methods: {
        async fetchTrek() {
            try {
                const response = await api.get(`/trekker/trek-details/${this.$route.params.id}`)
                this.trek = response.data.trek
                this.booking = response.data.booking
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async bookTrek() {
            if (!confirm("Book this trek?")) {
                return
            }

            try {
                const response = await api.post(`/trekker/trek/${this.trek.id}/book`)
                this.trek = response.data.trek
                this.booking = response.data.booking
                setFlash(response.data.message, "success")
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async cancelBooking() {
            if (!confirm("Cancel this booking?")) {
                return
            }

            try {
                const response = await api.post(`/trekker/booking/${this.booking.id}/cancel`)
                this.trek = response.data.trek
                this.booking = response.data.booking
                setFlash(response.data.message, "success")
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
                        <RouterLink
                            :to="{ name: booking?.status === 'Booked' || booking?.status === 'Completed' ? 'my-bookings' : 'view-treks' }">
                            <i class="fa-solid fa-arrow-left"></i>
                            Back to {{ booking?.status === 'Booked' || booking?.status === 'Completed' ? 'Bookings' :
                            'Treks' }}
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

                                <div class="detail-item">
                                    <span class="detail-key">Available Slots :</span>
                                    <span class="detail-value ml-6">{{ trek.slots }}</span>
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
                                    <span class="detail-key">Assigned Staff :</span>
                                    <span class="detail-value ml-6">{{ trek.staff?.full_name || "Not Assigned" }}</span>
                                </div>

                                <div class="d-flex justify-content-end gap-4 mt-10">
                                    <button v-if="canCancel" class="btn btn-outline-danger btn-md"
                                        @click="cancelBooking">
                                        Cancel Booking
                                    </button>
                                    <button v-else-if="canBook" class="btn btn-info-light btn-md" @click="bookTrek">
                                        Book Now
                                    </button>
                                    <span v-else class="badge" :class="badgeClass(trek.status)">
                                        {{ booking?.status === "Completed" ? "Completed" : trek.status }}
                                    </span>
                                </div>

                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
