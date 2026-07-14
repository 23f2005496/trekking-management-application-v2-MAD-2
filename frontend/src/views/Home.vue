<script>
import Navbar from "@/components/Navbar.vue"

export default {
    components: {
        Navbar,
    }
}
</script>

<template>

    <Navbar />


    <div class="container mt-16">

        <!-- Hero Section -->
        <section class="text-center p-6">

            <h1 class="font-bold" style="font-size: 2.75rem; margin-bottom: 1.5rem;">
                Welcome to Trekking World
            </h1>

            <p class="text-lg text-gray mb-6" style="max-width: 940px; margin-left: auto; margin-right: auto;">
                Explore Beyond Boundaries, breathtaking destinations, plan your next adventure,
                and connect with fellow trekkers. Join our community of outdoor enthusiasts today.
            </p>

            <div class="d-flex justify-content-center gap-4 mb-6">
                <RouterLink :to="{ name: 'register' }" class="btn btn-primary btn-lg">
                    Get Started
                </RouterLink>

                <RouterLink :to="{ name: 'login' }" class="btn btn-outline-primary btn-lg">
                    Sign In
                </RouterLink>
            </div>

        </section>

        <!-- Features Section -->
        <section class="mb-6">

            <div class="dashboard-cards row gap-6">

                <div class="col">

                    <div class="card h-100">

                        <div class="card-body text-center">

                            <h3 class="mb-3">🏔️ Explore</h3>
                            <h3 class="mb-3">Find Your Next Adventure</h3>

                            <p>
                                Explore handpicked trekking experiences designed
                                for beginners and seasoned adventurers alike.
                            </p>

                        </div>

                    </div>

                </div>

                <div class="col">

                    <div class="card h-100">

                        <div class="card-body text-center">

                            <h3 class="mb-3">🎒 Book</h3>
                            <h3 class="mb-3">Seamless Trek Booking</h3>

                            <p>
                                Reserve your place on upcoming treks and manage
                                all your bookings in one convenient platform.
                            </p>

                        </div>

                    </div>

                </div>

                <div class="col">

                    <div class="card h-100">

                        <div class="card-body text-center">

                            <h3 class="mb-3">🌍 Connect</h3>
                            <h3 class="mb-3">Adventure Together</h3>

                            <p>
                                Join a community of trekkers and experienced guides
                                who share your passion for exploration.
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </section>

        <!-- Call To Action -->
        <section class="text-center p-6 mb-6 bg-primary rounded-lg text-white">

            <h2 class="mb-3 text-white">
                Your Gateway to Adventure
            </h2>

            <p class="mb-4">
                Join treks led by experienced guides and stay updated with trek
                schedules, participant information, and real-time trek status.
            </p>

            <RouterLink :to="{ name: 'register' }" class="btn btn-lg text-primary bg-white">
                Create Your Account
            </RouterLink>

        </section>

    </div>


</template>