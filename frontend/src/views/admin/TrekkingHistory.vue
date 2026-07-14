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
        this.fetchHistory()
    },

    methods: {
        async fetchHistory() {
            try {
                const response = await api.get("/admin/trekking-history", {
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
    <h1 class="page-title">Trekking History</h1>

    <form @submit.prevent="fetchHistory">
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
                                <th>Trek Name</th>
                                <th>Location</th>
                                <th>Difficulty</th>
                                <th>Duration</th>
                                <th>Status</th>
                                <th>Completed On</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="trek in treks" :key="trek.id">
                                <td>{{ trek.name }}</td>
                                <td>{{ trek.location }}</td>
                                <td>{{ trek.difficulty }}</td>
                                <td>{{ trek.duration }}</td>
                                <td>
                                    <span class="badge" :class="badgeClass(trek.status)">
                                        {{ trek.status }}
                                    </span>
                                </td>
                                <td>{{ trek.end_date_label }}</td>
                                <td class="action-buttons">
                                    <RouterLink :to="{ name: 'admin-trek-details', params: { id: trek.id } }"
                                        class="btn btn-outline-info btn-md">
                                        View Details
                                    </RouterLink>
                                </td>
                            </tr>
                            <tr v-if="treks.length === 0">
                                <td colspan="7" class="text-center text-gray">No completed treks found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>
