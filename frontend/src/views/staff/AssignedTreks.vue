<script>
import api from "@/services/api"

export default {
    data() {
        return {
            query: "",
            assigned_treks: [],
            error: ""
        }
    },

    mounted() {
        this.fetchTreks()
    },

    methods: {
        async fetchTreks() {
            try {
                const response = await api.get("/staff/assigned-treks", {
                    params: { query: this.query }
                })
                this.assigned_treks = response.data.treks
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
    <h1 class="page-title">Assigned Treks</h1>

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
                                <th>S. No</th>
                                <th>Name</th>
                                <th>Location</th>
                                <th>Difficulty</th>
                                <th>Duration</th>
                                <th>Status</th>
                                <th>Available Slots</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(trek, index) in assigned_treks" :key="trek.id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ trek.name }}</td>
                                <td>{{ trek.location }}</td>
                                <td>{{ trek.difficulty }}</td>
                                <td>{{ trek.duration }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(trek.status)">
                                        {{ trek.status }}
                                    </span>
                                </td>
                                <td>{{ trek.slots }}</td>
                                <td class="action-buttons">
                                    <RouterLink :to="{ name: 'staff-trek-details', params: { id: trek.id } }"
                                        class="btn btn-outline-info btn-md">
                                        Manage
                                    </RouterLink>
                                </td>
                            </tr>
                            <tr v-if="assigned_treks.length === 0">
                                <td colspan="8" class="text-center text-gray">No assigned treks</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>
