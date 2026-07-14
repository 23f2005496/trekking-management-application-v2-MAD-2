<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {

    data() {
        return {
            query: "",
            staff: [],
            error: ""
        }
    },

    mounted() {
        this.fetchStaff()
    },

    methods: {

        async fetchStaff() {
            try {
                const response = await api.get("/admin/staff", {
                    params: {
                        query: this.query
                    }
                })
                this.staff = response.data.staff
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async changeStaffStatus(staff, status) {
            if (!confirm(`Change ${staff.full_name}'s status to ${status}?`)) {
                return
            }

            try {
                const response = await api.post(`/admin/staff/${staff.id}/status`, { status })
                setFlash(response.data.message, "success")
                await this.fetchStaff()
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

    <h1 class="page-title">Manage Trekking Staff</h1>

    <RouterLink :to="{ name: 'create-staff' }" class="btn btn-primary mb-4">
        <i class="fa-regular fa-user"></i>
        Create New Staff
    </RouterLink>

    <form @submit.prevent="fetchStaff">
        <table class="table">
            <tbody>
                <tr>
                    <td>Search Staff:</td>
                    <td>
                        <input class="form-control" type="text" v-model="query" placeholder="Search by Name">
                    </td>
                    <td>
                        <button class="btn btn-primary" type="submit">Search</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </form>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <section class="mb-6">
        <div class="card">
            <div class="card-body">

                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Staff ID</th>
                                <th>Full Name</th>
                                <th>Email</th>
                                <th>Contact</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="member in staff" :key="member.id">
                                <td>TS00{{ member.id }}</td>
                                <td>{{ member.full_name }}</td>
                                <td>{{ member.email }}</td>
                                <td>{{ member.contact || "No Contact" }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(member.status)">
                                        {{ member.status }}
                                    </span>
                                </td>
                                <td class="action-buttons">
                                    <button v-if="member.status !== 'Active'" class="btn btn-outline-success btn-md"
                                        @click="changeStaffStatus(member, 'Active')">
                                        Activate
                                    </button>
                                    <button v-if="member.status !== 'Blacklisted'" class="btn btn-outline-danger btn-md"
                                        @click="changeStaffStatus(member, 'Blacklisted')">
                                        Blacklist
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="staff.length === 0">
                                <td colspan="6" class="text-center text-gray">No staff found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>