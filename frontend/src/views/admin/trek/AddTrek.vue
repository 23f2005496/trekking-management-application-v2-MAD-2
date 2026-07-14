<script>
import api from "@/services/api"
import { setFlash } from "@/services/flash"

export default {
    data() {
        return {
            form: {
                name: "",
                location: "",
                difficulty: "Easy",
                duration: "",
                slots: 0,
                start_date: "",
                end_date: ""
            },
            image: null,
            error: ""
        }
    },

    methods: {
        onFileChange(event) {
            this.image = event.target.files[0] || null
        },

        buildFormData() {
            const formData = new FormData()
            Object.entries(this.form).forEach(([key, value]) => {
                formData.append(key, value)
            })
            if (this.image) {
                formData.append("image", this.image)
            }
            return formData
        },

        async saveTrek() {
            try {
                const response = await api.post("/admin/add-trek", this.buildFormData())
                setFlash(response.data.message, "success")
                this.$router.push({ name: "manage-treks" })
            }
            catch (error) {
                this.error = error.response?.data?.message || error.message
            }
        }
    }
}
</script>

<template>
    <h1 class="page-title">Add New Trek</h1>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <form @submit.prevent="saveTrek" enctype="multipart/form-data">

        <div class="form-group">
            <label class="form-label">Trek Name</label>
            <input class="form-control" v-model="form.name" required autofocus>
        </div>

        <div class="form-group">
            <label class="form-label">Location</label>
            <input class="form-control" v-model="form.location" required>
        </div>

        <div class="form-group">
            <label class="form-label">Trek Image</label>
            <input class="form-control" type="file" accept=".jpg,.jpeg,.png" @change="onFileChange">
        </div>

        <div class="form-group">
            <label class="form-label">Difficulty</label>
            <select class="form-control" v-model="form.difficulty">
                <option>Easy</option>
                <option>Moderate</option>
                <option>Hard</option>
            </select>
        </div>

        <div class="form-group">
            <label class="form-label">Duration (Days)</label>
            <input class="form-control" v-model="form.duration" required>
        </div>

        <div class="form-group">
            <label class="form-label">Available Slots</label>
            <input class="form-control" type="number" min="0" v-model="form.slots" required>
        </div>

        <div class="form-group">
            <label class="form-label">Start Date</label>
            <input class="form-control" type="date" v-model="form.start_date" required>
        </div>

        <div class="form-group">
            <label class="form-label">End Date</label>
            <input class="form-control" type="date" v-model="form.end_date" required>
        </div>

        <div class="action-buttons">
            <RouterLink :to="{ name: 'manage-treks' }" class="btn btn-outline-primary">
                Cancel
            </RouterLink>
            <button class="btn btn-primary">
                Save
            </button>
        </div>

    </form>

</template>
