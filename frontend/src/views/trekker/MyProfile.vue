<script>
import api from "@/services/api"

export default {
    data() {
        return {
            user: null,
            error: ""
        }
    },

    mounted() {
        this.fetchProfile()
    },

    methods: {
        async fetchProfile() {
            try {
                const response = await api.get("/user-profile")
                this.user = response.data.user
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        }
    }
}
</script>

<template>
    <h1 class="page-title">My Profile</h1>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <section v-if="user" class="mb-6">
        <div class="row gap-6">
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <h2 class="mb-3">Your Details</h2>
                        <div class="detail-item">
                            <span class="detail-key">Email :</span>
                            <span class="detail-value">{{ user.email }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-key">Full Name :</span>
                            <span class="detail-value">{{ user.full_name }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-key">Contact :</span>
                            <span class="detail-value">{{ user.contact || "-" }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-key">Role :</span>
                            <span class="detail-value">{{ user.role }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <RouterLink :to="{ name: 'trekker-update-profile' }" class="btn btn-primary">
        Update Profile
    </RouterLink>
</template>
