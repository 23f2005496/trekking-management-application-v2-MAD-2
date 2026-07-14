<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            trek: null,
            error: ""
        }
    },

    mounted() {
        this.fetchTrek()
    },

    methods: {
        async fetchTrek() {
            try {
                const response = await api.get(`/admin/trek-details/${this.$route.params.id}`)
                this.trek = response.data.trek
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async deleteTrek() {
            if (!confirm(`Delete ${this.trek.name}?`)) {
                return
            }

            try {
                const response = await api.post(`/admin/delete-trek/${this.trek.id}`)
                setFlash(response.data.message, "error")
                this.$router.push({ name: "manage-treks" })
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
                        <RouterLink :to="{ name: trek.status !== 'Completed' ? 'manage-treks' : 'trekking-history' }">
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

                                <div class="detail-item">
                                    <span class="detail-key">Participants :</span>
                                    <span class="detail-value ml-6">{{ trek.participants }}</span>
                                </div>

                                <div class="d-flex justify-content-center gap-4 mt-6">
                                    <template v-if="trek.status !== 'Completed'">
                                        <RouterLink :to="{ name: 'edit-trek', params: { id: trek.id } }"
                                            class="btn btn-info btn-md">
                                            Edit
                                            <i class="fa-regular fa-pen-to-square"></i>
                                        </RouterLink>
                                        <button class="btn btn-danger btn-md" @click="deleteTrek">
                                            Delete
                                            <i class="fa-regular fa-trash-can"></i>
                                        </button>
                                        <RouterLink :to="{ name: 'assign-staff', params: { id: trek.id } }"
                                            class="btn btn-success btn-md">
                                            Assign Staff
                                            <i class="fa-regular fa-user"></i>
                                        </RouterLink>
                                    </template>

                                    <span v-else class="badge" :class="badgeClass(trek.status)">
                                        {{ trek.status }}
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
