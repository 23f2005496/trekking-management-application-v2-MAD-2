<script>
import api from "@/services/api"
import { saveUser } from "@/services/auth"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            form: {
                email: "",
                full_name: "",
                contact: ""
            },
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
                this.form = {
                    email: response.data.user.email,
                    full_name: response.data.user.full_name,
                    contact: response.data.user.contact || ""
                }
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async updateProfile() {
            try {
                const response = await api.post("/update-profile", this.form)
                saveUser(response.data.user)
                setFlash(response.data.message, "success")
                this.$router.push({ name: "staff-profile" })
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        }
    }
}
</script>

<template>
    <h1 class="page-title">Update Profile</h1>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <form @submit.prevent="updateProfile">

        <div class="form-group">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="form.email" required autofocus>
        </div>

        <div class="form-group">
            <label class="form-label">Full Name</label>
            <input class="form-control" v-model="form.full_name" required>
        </div>

        <div class="form-group">
            <label class="form-label">Contact</label>
            <input class="form-control" v-model="form.contact" minlength="10" maxlength="15">
        </div>

        <div class="action-buttons">
            <RouterLink :to="{ name: 'staff-profile' }" class="btn btn-outline-primary">
                Cancel
            </RouterLink>
            <button class="btn btn-primary">
                Submit
            </button>
        </div>

    </form>

</template>
