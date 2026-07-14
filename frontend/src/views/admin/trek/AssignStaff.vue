<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            query: "",
            trek: null,
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
                const response = await api.get(`/admin/trek/${this.$route.params.id}/staff`, {
                    params: { query: this.query }
                })
                this.trek = response.data.trek
                this.staff = response.data.staff
                this.error = ""
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async assignStaff(member) {
            // if (!confirm(`Assign ${member.full_name} to ${this.trek.name}?`)) {
            //     return
            // }

            try {
                const response = await api.post(`/admin/trek/${this.trek.id}/assign-staff/${member.id}`)
                this.trek = response.data.trek
                setFlash(response.data.message, "success")

            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        },

        async removeStaff(member) {
            if (!confirm(`Remove ${member.full_name} from ${this.trek.name}?`)) {
                return
            }

            try {
                const response = await api.post(`/admin/trek/${this.trek.id}/remove-staff/${member.id}`)
                this.trek = response.data.trek
                setFlash(response.data.message, "error")
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        }
    }
}
</script>

<template>
    <h1 class="page-title">Assign Staff for {{ trek?.name }}</h1>

    <RouterLink v-if="trek" :to="{ name: 'admin-trek-details', params: { id: trek.id } }"
        class="btn btn-outline-primary mb-4">
        Back
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

    <section v-if="trek" class="mb-6">
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
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="member in staff" :key="member.id">
                                <td>S00{{ member.id }}</td>
                                <td>{{ member.full_name }}</td>
                                <td>{{ member.email }}</td>
                                <td>{{ member.contact || "No Contact" }}</td>
                                <td class="action-buttons">
                                    <button v-if="trek.assigned_staff_id === member.id" class="btn btn-danger btn-sm"
                                        @click="removeStaff(member)">
                                        Remove
                                    </button>
                                    <button v-else class="btn btn-info btn-sm" @click="assignStaff(member)">
                                        Assign
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="staff.length === 0">
                                <td colspan="5" class="text-center text-gray">No active staff</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</template>
