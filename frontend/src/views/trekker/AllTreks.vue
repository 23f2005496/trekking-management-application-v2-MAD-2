<script>
import api from "@/services/api"

export default {
    data() {
        return {
            location: "",
            difficulty: "",
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
                const response = await api.get("/trekker/treks", {
                    params: {
                        location: this.location,
                        difficulty: this.difficulty
                    }
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
    <h1 class="page-title">All Treks</h1>

    <div class="card">
        <div class="card-body">
            <form @submit.prevent="fetchTreks">

                <div class="form-group">
                    <label for="location" class="form-label">Search Location</label>
                    <input class="form-control" type="text" v-model="location" placeholder="Search by Location">
                </div>

                <div class="form-group">
                    <label for="difficulty" class="form-label">Select Difficulty</label>
                    <select v-model="difficulty" class="form-control">
                        <option value="">All</option>
                        <option value="Easy">Easy</option>
                        <option value="Moderate">Moderate</option>
                        <option value="Hard">Hard</option>
                    </select>
                </div>

                <button type="submit" class="btn btn-primary">Filter Treks</button>
            </form>
        </div>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <section class="mb-6">
        <div class="card">
            <div class="card-body">
                <div class="trek-container">

                    <div v-for="trek in treks" :key="trek.id" class="trek-card">
                        <div>
                            <img :src="trek.image_url" alt="Trek image" class="trek-image">
                        </div>

                        <div class="trek-body">
                            <h2>{{ trek.name }}</h2>
                            <p class="text-gray mt-2 mb-2">{{ trek.location }}</p>

                            <div class="d-flex gap-16 align-items-center">
                                <p><strong>{{ trek.difficulty }}</strong> • {{ trek.duration }}</p>
                                <p>
                                    <span class="badge" :class="badgeClass(trek.status)">
                                        {{ trek.status }}
                                    </span>
                                </p>
                            </div>

                            <p>Available Slots: <strong>{{ trek.slots }}</strong></p>

                            <RouterLink :to="{ name: 'trekker-trek-details', params: { id: trek.id } }"
                                class="btn btn-outline-info d-block btn-md">
                                View Details
                            </RouterLink>
                        </div>

                    </div>

                    <p v-if="treks.length === 0" class="text-gray">No available treks</p>
                </div>
            </div>
        </div>
    </section>
</template>
