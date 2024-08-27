import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import LandingPage from "../views/LandingPage.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "landing",
    component: LandingPage,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
