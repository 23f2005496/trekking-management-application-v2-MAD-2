<script>
import api from "@/services/api"
import { clearUser, getUser } from "@/services/auth"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            authVersion: 0
        }
    },

    computed: {

        user() {
            this.authVersion
            return getUser()
        }

    },

    mounted() {
        window.addEventListener("auth-changed", this.refreshAuth)
    },

    beforeUnmount() {
        window.removeEventListener("auth-changed", this.refreshAuth)
    },

    methods: {
        refreshAuth() {
            this.authVersion += 1
        },

        async logout() {

            try {

                await api.post("/logout")

                clearUser()
                setFlash("Logout successful!", "success")

                this.$router.push({
                    name: "login"
                })

            }

            catch (error) {

                setFlash(error.response?.data?.message || error.message, "error")

            }

        }

    }

}
</script>

<template>

    <nav class="navbar">

        <router-link :to="{ name: 'home' }" class="navbar-brand">
            <i class="fa-solid fa-person-hiking"></i>
            Trekking Management Application
        </router-link>

        <ul class="navbar-nav">

            <template v-if="user">

                <li class="nav-item">
                    <i class="fa-regular fa-user"></i>
                    {{ user.full_name }}
                </li>

                <li class="nav-item">

                    <a href="#" class="nav-link" @click.prevent="logout">
                        <i class="fa-solid fa-arrow-right-from-bracket"></i>
                        Logout
                    </a>

                </li>

            </template>

            <template v-else>

                <li class="nav-item">

                    <router-link :to="{ name: 'login' }" class="nav-link">
                        Login
                    </router-link>

                </li>

                <li class="nav-item">

                    <router-link :to="{ name: 'register' }" class="nav-link">
                        Register
                    </router-link>

                </li>

            </template>

        </ul>

    </nav>

</template>
