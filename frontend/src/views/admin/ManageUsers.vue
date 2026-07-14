<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {

    data() {
        return {
            query: "",
            users: [],
            error: ""
        }
    },

    mounted() {
        this.fetchUsers()
    },

    methods: {

        async fetchUsers() {
            try {
                const response = await api.get("/admin/users", {
                    params: {
                        query: this.query
                    }
                })
                this.users = response.data.users
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async changeUserStatus(user, status) {
            if (!confirm(`Change ${user.full_name}'s status to ${status}?`)) {
                return
            }

            try {
                const response = await api.post(`/admin/user/${user.id}/change-status`, { status })
                setFlash(response.data.message, "success")
                await this.fetchUsers()
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
    <h1 class="page-title">Manage Users (Trekkers)</h1>

    <form @submit.prevent="fetchUsers">
        <table class="table">
            <tbody>
                <tr>
                    <td>Search Users:</td>
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
                                <th>User ID</th>
                                <th>Full Name</th>
                                <th>Email</th>
                                <th>Contact</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(user, index) in users" :key="user.id">
                                <td>U00{{ index + 1 }}</td>
                                <td>{{ user.full_name }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ user.contact || "No Contact" }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(user.status)">
                                        {{ user.status }}
                                    </span>
                                </td>
                                <td class="action-buttons">
                                    <template v-if="user.role !== 'admin'">
                                        <button v-if="user.status === 'Blacklisted'" class="btn btn-outline-success btn-md"
                                            @click="changeUserStatus(user, 'Active')">
                                            Activate
                                        </button>
                                        <button v-else class="btn btn-outline-danger btn-md"
                                            @click="changeUserStatus(user, 'Blacklisted')">
                                            Blacklist
                                        </button>
                                    </template>
                                    <span v-else>None</span>
                                </td>
                            </tr>
                            <tr v-if="users.length === 0">
                                <td colspan="7" class="text-center text-gray">No users found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>
