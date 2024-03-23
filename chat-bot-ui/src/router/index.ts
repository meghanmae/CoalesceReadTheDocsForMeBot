import { createRouter, createWebHistory } from "vue-router";
import ChatBotView from "../views/ChatBotView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: ChatBotView,
    },
  ],
});

export default router;
