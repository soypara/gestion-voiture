import { createRouter, createWebHistory } from "vue-router";
import Register from "../components/Register.vue";
import Login from "../components/Login.vue";
import Dashboard from "../components/Dashboard.vue";
import Directions from "../components/Directions.vue"

const routes = [
  { path: "/", redirect: "/login" }, // page par défaut
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/dashboard", component: Dashboard },
  { path: "/directions", component: Directions},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
