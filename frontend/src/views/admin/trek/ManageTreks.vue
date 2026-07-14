<script>
import api from "@/services/api"

export default {
    data() {
        return {
            query: "",
            treks: [],
            error: ""
        }
    },

    mounted() {
        this.fetchTreks()
    },

    methods: {
        async fetchTreks() {
            try {
                const response = await api.get("/admin/treks", {
                    params: { query: this.query }
                })
                this.treks = response.data.treks
                this.error = ""
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
    <h1 class="page-title">Manage Treks</h1>

    <RouterLink :to="{ name: 'add-trek' }" class="btn btn-primary mb-4">
        <i class="fa-solid fa-plus"></i>
        Add New Trek
    </RouterLink>

    <form @submit.prevent="fetchTreks">
        <table class="table">
            <tbody>
                <tr>
                    <td>Search Treks:</td>
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
                                <th>ID</th>
                                <th>Trek Name</th>
                                <th>Location</th>
                                <th>Difficulty</th>
                                <th>Available Slots</th>
                                <th>Status</th>
                                <th>Assigned Staff</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(trek, index) in treks" :key="trek.id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ trek.name }}</td>
                                <td>{{ trek.location }}</td>
                                <td>{{ trek.difficulty }}</td>
                                <td>{{ trek.slots }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(trek.status)">
                                        {{ trek.status }}
                                    </span>
                                </td>
                                <td>{{ trek.staff?.full_name || "Not Assigned" }}</td>
                                <td class="action-buttons">
                                    <RouterLink :to="{ name: 'admin-trek-details', params: { id: trek.id } }"
                                        class="btn btn-outline-info btn-md">
                                        Manage
                                    </RouterLink>
                                </td>
                            </tr>
                            <tr v-if="treks.length === 0">
                                <td colspan="8" class="text-center text-gray">No treks found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>
