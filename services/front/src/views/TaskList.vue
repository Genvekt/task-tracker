<template>
  <q-page class="">
    <div class="q-pt-md">
      <task-create
        @taskCreated="addCreatedTask($event)"
        @errorResponce="showErrorAlert($event)"
      />
    </div>
    <div class="q-mx-auto q-px-md q-pt-sm">
      <q-list bordered class="rounded-borders shadow-3 justify-center">
        <div v-for="task in this.tasks" :key="task.id">
          <task-item
            :task="task"
            @statusChange="
              $event.then((status) => {
                task.status = status;
              })
            "
          />
          <q-separator />
        </div>
      </q-list>
    </div>
    <div class="column q-mt-md items-center">
      <q-btn
        class="col-2"
        color="primary"
        label="Reassign tasks"
        @click="reassignTrigger"
      />
    </div>
    <q-footer elevated>
      <error-alert :message="this.alertMessage" :show="this.alertShow" />
    </q-footer>
  </q-page>
</template>

<script>
import { db } from "@/main";
import { ref } from "vue";
import TaskItem from "@/components/TaskItem";
import TaskCreate from "@/components/TaskCreate";
import ErrorAlert from "@/components/ErrorAlert";
export default {
  name: "TaskList",
  components: { ErrorAlert, TaskCreate, TaskItem },
  data() {
    return {
      tasks: [],
      dialog: ref(),
      alertShow: false,
      alertMessage: "",
      newTask: {
        title: null,
        description: null,
        user_id: null,
      },
    };
  },
  created() {
    this.reloadTaskList();
  },
  methods: {
    addCreatedTask: function (task) {
      this.tasks.push(task);
    },
    showErrorAlert: function (message) {
      this.alertShow = true;
      this.alertMessage = message;
      setTimeout(() => {
        this.alertShow = false;
      }, 2000);
    },
    reassignTrigger: function () {
      db.reassignTasks().then(() => this.reloadTaskList());
    },
    reloadTaskList: function () {
      db.getList("tasks").then((data) => {
        this.tasks = data;
      });
    },
  },
};
</script>
