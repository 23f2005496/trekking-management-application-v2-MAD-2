import { createRouter, createWebHistory } from "vue-router"
import { getUser, dashboardRouteFor } from "@/services/auth"

import Home from "@/views/Home.vue"

import Login from "@/views/auth/Login.vue"
import Register from "@/views/auth/Register.vue"

import MainLayout from "@/layouts/MainLayout.vue"

import AdminDashboard from "@/views/admin/AdminDashboard.vue"
import AddTrek from "@/views/admin/trek/AddTrek.vue"
import AdminTrekDetails from "@/views/admin/trek/TrekDetails.vue"
import EditTrek from "@/views/admin/trek/EditTrek.vue"
import AssignStaff from "@/views/admin/trek/AssignStaff.vue"
import ManageStaff from "@/views/admin/ManageStaff.vue"
import CreateStaff from "@/views/admin/CreateStaff.vue"
import AllBookings from "@/views/admin/AllBookings.vue"
import AdminTrekkingHistory from "@/views/admin/TrekkingHistory.vue"
import ManageTreks from "@/views/admin/trek/ManageTreks.vue"
import ManageUsers from "@/views/admin/ManageUsers.vue"

import StaffDashboard from "@/views/staff/StaffDashboard.vue"
import AssignedTreks from "@/views/staff/AssignedTreks.vue"
import StaffTrekDetails from "@/views/staff/TrekDetails.vue"
import StaffTrekkingHistory from "@/views/staff/TrekkingHistory.vue"
import StaffProfile from "@/views/staff/MyProfile.vue"
import StaffUpdateProfile from "@/views/staff/UpdateProfile.vue"
import StaffChangePassword from "@/views/staff/ChangePassword.vue"

import TrekkerDashboard from "@/views/trekker/TrekkerDashboard.vue"
import AllTreks from "@/views/trekker/AllTreks.vue"
import TrekkerTrekDetails from "@/views/trekker/TrekDetails.vue"
import MyBookings from "@/views/trekker/MyBookings.vue"
import TrekkerTrekkingHistory from "@/views/trekker/TrekkingHistory.vue"
import TrekkerProfile from "@/views/trekker/MyProfile.vue"
import TrekkerUpdateProfile from "@/views/trekker/UpdateProfile.vue"
import TrekkerChangePassword from "@/views/trekker/ChangePassword.vue"

const routes = [

  {
    path: "/",
    name: "home",
    component: Home
  },


  {
    path: "/login",
    name: "login",
    component: Login
  },

  {
    path: "/register",
    name: "register",
    component: Register
  },

  {
    path: "/admin",
    component: MainLayout,
    children: [
      {
        path: "dashboard",
        name: "admin-dashboard",
        component: AdminDashboard,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "treks",
        name: "manage-treks",
        component: ManageTreks,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "treks/add",
        name: "add-trek",
        component: AddTrek,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "treks/:id",
        name: "admin-trek-details",
        component: AdminTrekDetails,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "treks/:id/edit",
        name: "edit-trek",
        component: EditTrek,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "treks/:id/assign-staff",
        name: "assign-staff",
        component: AssignStaff,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "staff",
        name: "manage-staff",
        component: ManageStaff,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "create-staff",
        name: "create-staff",
        component: CreateStaff,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "bookings",
        name: "all-bookings",
        component: AllBookings,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "history",
        name: "trekking-history",
        component: AdminTrekkingHistory,
        meta: { requiresAuth: true, role: "admin" }
      },
      {
        path: "users",
        name: "manage-users",
        component: ManageUsers,
        meta: { requiresAuth: true, role: "admin" }
      }
    ]
  },

  {
    path: "/staff",
    component: MainLayout,
    children: [
      {
        path: "dashboard",
        name: "staff-dashboard",
        component: StaffDashboard,
        meta: { requiresAuth: true, role: "staff" }
      },
      {
        path: "treks",
        name: "assigned-treks",
        component: AssignedTreks,
        meta: { requiresAuth: true, role: "staff" }
      },
      {
        path: "treks/:id",
        name: "staff-trek-details",
        component: StaffTrekDetails,
        meta: { requiresAuth: true, role: "staff" }
      },
      {
        path: "history",
        name: "staff-history",
        component: StaffTrekkingHistory,
        meta: { requiresAuth: true, role: "staff" }
      },
      {
        path: "profile",
        name: "staff-profile",
        component: StaffProfile,
        meta: { requiresAuth: true, role: "staff" }
      },
      {
        path: "profile/update",
        name: "staff-update-profile",
        component: StaffUpdateProfile,
        meta: { requiresAuth: true, role: "staff" }
      },
      {
        path: "password/update",
        name: "staff-update-password",
        component: StaffChangePassword,
        meta: { requiresAuth: true, role: "staff" }
      },
    ]
  },

  {
    path: "/trekker",
    component: MainLayout,
    children: [
      {
        path: "dashboard",
        name: "trekker-dashboard",
        component: TrekkerDashboard,
        meta: { requiresAuth: true, role: "trekker" }
      },
      {
        path: "treks",
        name: "view-treks",
        component: AllTreks,
        meta: { requiresAuth: true, role: "trekker" }
      },
      {
        path: "treks/:id",
        name: "trekker-trek-details",
        component: TrekkerTrekDetails,
        meta: { requiresAuth: true, role: "trekker" }
      },
      {
        path: "bookings",
        name: "my-bookings",
        component: MyBookings,
        meta: { requiresAuth: true, role: "trekker" }
      },
      {
        path: "history",
        name: "trekker-history",
        component: TrekkerTrekkingHistory,
        meta: { requiresAuth: true, role: "trekker" }
      },
      {
        path: "profile",
        name: "trekker-profile",
        component: TrekkerProfile,
        meta: { requiresAuth: true, role: "trekker" }
      },
      {
        path: "profile/update",
        name: "trekker-update-profile",
        component: TrekkerUpdateProfile,
        meta: { requiresAuth: true, role: "trekker" }
      },
      {
        path: "password/update",
        name: "trekker-update-password",
        component: TrekkerChangePassword,
        meta: { requiresAuth: true, role: "trekker" }
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const user = getUser()

  if ((to.name === "login" || to.name === "register") && user) {
    return dashboardRouteFor(user)
  }

  if (to.meta.requiresAuth && !user) {
    return { name: "login" }
  }

  if (to.meta.role && user?.role !== to.meta.role) {
    return dashboardRouteFor(user)
  }

  return true
})

export default router
