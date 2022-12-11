import { createRouter, createWebHistory } from "vue-router";
import TaskList from "../views/TaskList.vue";

const routes = [
  {
    path: "/",
    name: "taskList",
    component: TaskList,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
