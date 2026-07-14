<script>
import { flashState, clearFlash } from "@/services/flash"

export default {
    data() {
        return {
            flashState,
        }
    },

    methods: {
        close() {
            clearFlash()
        }
    }
}
</script>

<template>

    <div v-if="flashState.flash" class="alert d-flex justify-content-between"
        :class="`alert-${flashState.flash.category}`">
        {{ flashState.flash.message }}
        <button type="button" @click="close" class="bg-none text-base">
            <i class="fa-solid fa-xmark"></i>
        </button>

    </div>

</template>
