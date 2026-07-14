// const FLASH_KEY = "flash-message"

// export function setFlash(message, category = "success") {
//     sessionStorage.setItem(FLASH_KEY, JSON.stringify({ message, category }))
//     window.dispatchEvent(new Event("flash-updated"))
// }

// export function consumeFlash() {
//     const rawFlash = sessionStorage.getItem(FLASH_KEY)
//     if (!rawFlash) {
//         return null
//     }
//     sessionStorage.removeItem(FLASH_KEY)
//     return JSON.parse(rawFlash)
// }


import { reactive } from "vue"

const FLASH_KEY = "flash-message"

const state = reactive({
    flash: null
})

// Runs once when this module is first imported (i.e. on a real page load).
// If the app never hard-refreshes, this stays in memory across navigations.
function restoreFromStorage() {
    const raw = sessionStorage.getItem(FLASH_KEY)
    if (raw) {
        state.flash = JSON.parse(raw)
        sessionStorage.removeItem(FLASH_KEY)
    }
}
restoreFromStorage()

export function setFlash(message, category = "success") {
    state.flash = { message, category }
    // Backup only, for surviving a hard refresh mid-flow
    sessionStorage.setItem(FLASH_KEY, JSON.stringify(state.flash))
}

export function clearFlash() {
    state.flash = null
    sessionStorage.removeItem(FLASH_KEY)
}

export const flashState = state