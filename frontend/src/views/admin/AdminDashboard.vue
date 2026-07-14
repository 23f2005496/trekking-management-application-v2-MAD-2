<script>
import api from "@/services/api"

export default {

    data() {

        return {

            total_treks: 0,
            total_staff: 0,
            total_trekkers: 0,
            total_bookings: 0,

            trek_status_data: {},
            error: "",
            chart: null

        }

    },

    mounted() {

        this.fetchDashboard()

    },

    beforeUnmount() {

        if (this.chart) {
            this.chart.destroy()
        }

    },

    methods: {

        async fetchDashboard() {

            try {

                const response = await api.get("/admin/dashboard")
                this.total_treks = response.data.total_treks
                this.total_staff = response.data.total_staff
                this.total_trekkers = response.data.total_trekkers
                this.total_bookings = response.data.total_bookings
                this.trek_status_data = response.data.trek_status_data
                this.$nextTick(this.loadChart)

            }

            catch (error) {

                this.error = error.response?.data?.message || error.message

            }

        },

        loadChart() {

            const ctx = document.getElementById("trekStatusChart")
            if (!ctx || !window.Chart) {
                return
            }

            if (this.chart) {
                this.chart.destroy()
            }

            this.chart = new window.Chart(ctx, {

                type: "pie",

                data: {

                    labels: this.trek_status_data.map(item => item.status),

                    datasets: [
                        {

                            label: "Trek Count",

                            data: this.trek_status_data.map(item => item.count),

                            backgroundColor: [
                                "#1d4ed8",  //Open          //Light Blue
                                "#ff0000",  //Closed        //Red
                                "#f97316",  //Ongoing       //Accent
                                "#008000"   //Completed     //Green
                            ],

                            hoverOffset: 5

                        }
                    ]

                },

                options: {

                    plugins: {

                        legend: {

                            position: "top",

                            labels: {

                                usePointStyle: true,
                                pointStyle: "circle",
                                padding: 20

                            }

                        }

                    }

                }

            })

        }

    }

}
</script>

<template>

    <h1 class="page-title">Welcome, Admin!</h1>

    <div v-if="error" class="alert alert-error">
        {{ error }}
    </div>

    <section class="mb-6">

        <div class="row gap-6">

            <div class="col">

                <div class="card">

                    <div class="card-body">

                        <h2 class="mb-3">Statistics & Insights</h2>

                        <div class="row gap-6">

                            <div class="col">

                                <div class="card bg-gray">

                                    <div class="card-body">

                                        <h3 class="mb-3">Total Treks</h3>

                                        <div class="detail-item gap-12">

                                            <h1 class="detail-key">
                                                {{ total_treks }}
                                            </h1>

                                            <h1 class="detail-value">
                                                <i class="fa-solid fa-mountain-sun"></i>
                                            </h1>

                                        </div>

                                    </div>

                                </div>

                            </div>

                            <div class="col">

                                <div class="card bg-gray">

                                    <div class="card-body">

                                        <h3 class="mb-3">Total Staff</h3>

                                        <div class="detail-item gap-12">

                                            <h1 class="detail-key">
                                                {{ total_staff }}
                                            </h1>

                                            <h1 class="detail-value">
                                                <i class="fa-solid fa-user-group"></i>
                                            </h1>

                                        </div>

                                    </div>

                                </div>

                            </div>

                            <div class="col">

                                <div class="card bg-gray">

                                    <div class="card-body">

                                        <h3 class="mb-3">Total Trekkers</h3>

                                        <div class="detail-item gap-12">

                                            <h1 class="detail-key">
                                                {{ total_trekkers }}
                                            </h1>

                                            <h1 class="detail-value">
                                                <i class="fa-solid fa-users"></i>
                                            </h1>

                                        </div>

                                    </div>

                                </div>

                            </div>

                            <div class="col">

                                <div class="card bg-gray">

                                    <div class="card-body">

                                        <h3 class="mb-3">Total Bookings</h3>

                                        <div class="detail-item gap-12">

                                            <h1 class="detail-key">
                                                {{ total_bookings }}
                                            </h1>

                                            <h1 class="detail-value">
                                                <i class="fa-regular fa-calendar"></i>
                                            </h1>

                                        </div>

                                    </div>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

            <div class="col">

                <div class="card">

                    <div class="card-body">

                        <h2 class="mb-3">Treks Status</h2>

                        <canvas id="trekStatusChart" class="trek-status-chart"></canvas>

                    </div>

                </div>

            </div>

        </div>

    </section>

</template>
