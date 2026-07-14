<script>
import api from "@/services/api"
import Navbar from "@/components/Navbar.vue"
import FlashMessage from "@/components/FlashMessage.vue"
import { setFlash } from "@/services/flash"


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
            role: "trekker",
            error: ""
        }
    },

    methods: {


        async register() {

            if (this.password !== this.confirm_password) {

                this.error = "Passwords do not match!"
                return

            }

            try {
                this.error = ""

                const response = await api.post("/register", {

                    email: this.email,
                    password: this.password,
                    full_name: this.full_name,
                    contact: this.contact,
                    role: this.role

                })

                if (response.data.success) {

                    setFlash(response.data.message, "success")
                    this.$router.push({ name: "login" })
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

    <Navbar />

    <main class="main-content">

        <FlashMessage />

        <div class="container">

            <h1 class="page-title">Register As Trekker</h1>

            <div v-if="error" class="alert alert-error">
                {{ error }}
            </div>

            <form @submit.prevent="register">

                <div class="form-group">
                    <label class="form-label">
                        Email
                    </label>

                    <input type="email" class="form-control" v-model="email" required autofocus>

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
                        Full Name
                    </label>

                    <input type="text" class="form-control" v-model="full_name" required>

                </div>

                <div class="form-group">

                    <label class="form-label">
                        Contact
                    </label>

                    <input type="text" class="form-control" v-model="contact" minlength="10" maxlength="15">

                </div>

                <div>
                    <button class="btn btn-primary">
                        Register
                    </button>
                </div>
            </form>
        </div>
    </main>

</template>
