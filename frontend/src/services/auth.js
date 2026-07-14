
export function getUser() {
    const rawUser = localStorage.getItem("user")
    return rawUser ? JSON.parse(rawUser) : null
}

export function saveUser(user) {
    localStorage.setItem("user", JSON.stringify(user))
    window.dispatchEvent(new Event("auth-changed"))
}

export function clearUser() {
    localStorage.removeItem("user")
    window.dispatchEvent(new Event("auth-changed"))
}

export function dashboardRouteFor(user) {
    if (!user) {
        return { name: "login" }
    }
    if (user.role === "admin") {
        return { name: "admin-dashboard" }
    }
    if (user.role === "staff") {
        return { name: "staff-dashboard" }
    }
    return { name: "trekker-dashboard" }
}
