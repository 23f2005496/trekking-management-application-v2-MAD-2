<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            password: "",
            confirm_password: "",
            error: ""
        }
    },

    methods: {
        async changePassword() {
            if (this.password !== this.confirm_password) {
                this.error = "Confirm password do not match."
                return
            }

            try {
                const response = await api.post("/change-password", {
                    password: this.password,
                    confirm_password: this.confirm_password
                })
                setFlash(response.data.message, "success")
                this.$router.push({ name: "trekker-profile" })
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        }
    }
}
</script>

<template>
    <h1 class="page-title">Change Password</h1>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <form @submit.prevent="changePassword">

        <div class="form-group">
            <label class="form-label">New Password</label>
            <input type="password" class="form-control" v-model="password" required minlength="8" autofocus>
        </div>

        <div class="form-group">
            <label class="form-label">Confirm Password</label>
            <input type="password" class="form-control" v-model="confirm_password" required minlength="8">
        </div>

        <div>
            <button class="btn btn-primary">
                Submit
            </button>
        </div>

    </form>

</template>
