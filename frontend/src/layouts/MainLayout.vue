<script>
import Navbar from "@/components/Navbar.vue"
import Sidebar from "@/components/Sidebar.vue"
import FlashMessage from "@/components/FlashMessage.vue"

export default {
    components: {
        Navbar,
        Sidebar,
        FlashMessage
    }
}
</script>

<template>

    <Navbar />

    <Sidebar />

    <main class="main-content">

        <FlashMessage />

        <div class="container">

            <router-view />

        </div>

    </main>

</template>