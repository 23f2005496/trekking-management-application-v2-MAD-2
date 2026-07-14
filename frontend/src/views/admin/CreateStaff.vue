<script>
import api from "@/services/api"
import Navbar from "@/components/Navbar.vue"
import FlashMessage from "@/components/FlashMessage.vue"
import { setFlash } from "@/services/flash"
import { createApp } from "vue";


export default {

    components: {
        Navbar,
        FlashMessage
    },

    data() {
        return {
            email: "",
            password: "",
            confirm_password: "",
            full_name: "",
            contact: "",
            role: "staff",
            error: ""
        }
    },

    methods: {


        async createStaff() {

            if (this.password !== this.confirm_password) {

                this.error = "Passwords do not match!"
                return

            }

            try {
                this.error = ""

                const response = await api.post("/admin/create-staff", {

                    full_name: this.full_name,
                    email: this.email,
                    password: this.password,
                    contact: this.contact,
                    role: this.role

                })

                if (response.data.success) {

                    setFlash(response.data.message, "success")
                    this.$router.push({ name: "manage-staff" })
                }

            }

            catch (error) {

                if (error.response) {
                    this.error = error.response.data.message
                }
                else {
                    this.error = error.message
                }

            }

        }

    }

}

</script>



<template>

    <h1 class="page-title">Create New Trekking Staff</h1>

    <div v-if="error" class="alert alert-error">
        {{ error }}
    </div>

    <form @submit.prevent="createStaff">

        <div class="form-group">

            <label class="form-label">
                Full Name
            </label>

            <input type="text" class="form-control" v-model="full_name" required autofocus>

        </div>

        <div class="form-group">
            <label class="form-label">
                Email
            </label>

            <input type="email" class="form-control" v-model="email" required>

        </div>

        <div class="form-group">

            <label class="form-label">
                Password
            </label>

            <input type="password" class="form-control" v-model="password" required minlength="8">

        </div>

        <div class="form-group">

            <label class="form-label">
                Confirm Password
            </label>

            <input type="password" class="form-control" v-model="confirm_password" required minlength="8">

        </div>

        <div class="form-group">

            <label class="form-label">
                Contact
            </label>

            <input type="text" class="form-control" v-model="contact" minlength="10" maxlength="15">

        </div>

        <div class="action-buttons">

            <RouterLink :to="{ name: 'manage-staff' }" class="btn btn-outline-primary">
                Cancel
            </RouterLink>

            <button class="btn btn-primary">
                Create Staff
            </button>
        </div>
    </form>

</template>
