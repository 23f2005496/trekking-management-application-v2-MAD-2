<script>
import { getUser } from "../services/auth"

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
        }
    }

}
</script>

<template>

    <aside class="drawer" v-if="user">

        <!-- ADMIN -->

        <template v-if="user.role === 'admin'">

            <router-link :to="{ name: 'admin-dashboard' }" class="nav-link">
                <i class="fa-solid fa-chart-simple"></i>
                Dashboard
            </router-link>

            <router-link :to="{ name: 'manage-treks' }" class="nav-link">
                <i class="fa-solid fa-mountain-sun"></i>
                Treks
            </router-link>

            <router-link :to="{ name: 'manage-staff' }" class="nav-link">
                <i class="fa-solid fa-user-group"></i>
                Staff
            </router-link>

            <router-link :to="{ name: 'all-bookings' }" class="nav-link">
                <i class="fa-regular fa-calendar"></i>
                Bookings
            </router-link>

            <router-link :to="{ name: 'trekking-history' }" class="nav-link">
                <i class="fa-solid fa-chart-column"></i>
                Trekking History
            </router-link>

            <router-link :to="{ name: 'manage-users' }" class="nav-link">
                <i class="fa-solid fa-users"></i>
                Users (Trekkers)
            </router-link>

        </template>

        <!-- STAFF -->

        <template v-else-if="user.role === 'staff'">

            <router-link :to="{ name: 'staff-dashboard' }" class="nav-link">
                <i class="fa-solid fa-chart-simple"></i>
                Dashboard
            </router-link>

            <router-link :to="{ name: 'assigned-treks' }" class="nav-link">
                <i class="fa-solid fa-mountain-sun"></i>
                Assigned Treks
            </router-link>

            <router-link :to="{ name: 'staff-history' }" class="nav-link">
                <i class="fa-solid fa-chart-column"></i>
                Trekking History
            </router-link>

            <router-link :to="{ name: 'staff-profile' }" class="nav-link">
                <i class="fa-solid fa-user-pen"></i>
                My Profile
            </router-link>

            <router-link :to="{ name: 'staff-update-password' }" class="nav-link">
                <i class="fa-solid fa-key"></i>
                Change Password
            </router-link>

        </template>

        <!-- TREKKER -->

        <template v-else>

            <router-link :to="{ name: 'trekker-dashboard' }" class="nav-link">
                <i class="fa-solid fa-chart-simple"></i>
                Dashboard
            </router-link>

            <router-link :to="{ name: 'view-treks' }" class="nav-link">
                <i class="fa-solid fa-mountain-sun"></i>
                View Treks
            </router-link>

            <router-link :to="{ name: 'my-bookings' }" class="nav-link">
                <i class="fa-regular fa-calendar"></i>
                My Bookings
            </router-link>

            <router-link :to="{ name: 'trekker-history' }" class="nav-link">
                <i class="fa-solid fa-chart-column"></i>
                Trekking History
            </router-link>

            <router-link :to="{ name: 'trekker-profile' }" class="nav-link">
                <i class="fa-solid fa-user-pen"></i>
                My Profile
            </router-link>

            <router-link :to="{ name: 'trekker-update-password' }" class="nav-link">
                <i class="fa-solid fa-key"></i>
                Change Password
            </router-link>

        </template>

    </aside>

</template>
