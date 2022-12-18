import { createRouter, createWebHistory } from "vue-router";
import TaskList from "../views/TaskList.vue";
import LoginPage from "../views/Login.vue";

const routes = [
  {
    path: "/",
    name: "taskList",
    component: TaskList,
  },
  {
    path: "/login",
    name: "loginPage",
    component: LoginPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
