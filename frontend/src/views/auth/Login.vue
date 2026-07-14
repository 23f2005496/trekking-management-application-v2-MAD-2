<script>
import api from "@/services/api"
import Navbar from "@/components/Navbar.vue"
import FlashMessage from "@/components/FlashMessage.vue"
import { dashboardRouteFor, saveUser } from "@/services/auth"
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
            error: ""

        }

    },

    methods: {

        async login() {

            try {
                this.error = ""

                const response = await api.post("/login", {

                    email: this.email,
                    password: this.password

                })

                if (response.data.success) {

                    saveUser(response.data.user)
                    setFlash(response.data.message, "success")
                    this.$router.push(dashboardRouteFor(response.data.user))

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

            <h1 class="page-title">Login</h1>

            <div v-if="error" class="alert alert-error">
                {{ error }}
            </div>

            <form @submit.prevent="login">

                <div class="form-group mb-3">

                    <label class="form-label">
                        Email
                    </label>

                    <input type="email" class="form-control" v-model="email" required autofocus>

                </div>

                <div class="form-group mb-3">

                    <label class="form-label">
                        Password
                    </label>

                    <input type="password" class="form-control" v-model="password" required minlength="8">

                </div>

                <div>
                    <button class="btn btn-primary">
                        Login
                    </button>
                </div>

            </form>

        </div>
    </main>

</template>
