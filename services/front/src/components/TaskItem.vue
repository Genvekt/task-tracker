<template>
  <q-item
    tag="label"
    v-ripple
    :class="{
      'line-through': isDone,
      'bg-grey-3': isDone,
    }"
  >
    <q-item-section side top>
      <q-checkbox
        v-model="isDone"
        :id="task.id"
        @click="taskStatusChange($event)"
      />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ task.title }}</q-item-label>
      <q-item-label caption> Description: {{ task.description }} </q-item-label>
      <q-item-label caption>
        {{ assigneeString }}
      </q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { db } from "@/main";

export default {
  name: "task-item",
  props: {
    task: {
      type: Object,
      default: null,
      required: true,
    },
  },
  computed: {
    isDone() {
      return this.task.status == "Done" ? true : false;
    },
    assigneeString() {
      if (this.task.assignee) {
        return `Assigned to: ${this.task.assignee.name}`;
      } else {
        return `Unassigned.`;
      }
    },
  },
  methods: {
    taskStatusChange: function () {
      if (!this.isDone) {
        this.$emit(
          "statusChange",
          db
            .updateOne("tasks", this.task.id, {
              id: this.task.id,
              title: this.task.title,
              description: this.task.description,
              user_id: this.task.assignee.id,
              status: "Done",
            })
            .then((task) => task.status)
        );
      } else {
        this.$emit(
          "statusChange",
          db
            .updateOne("tasks", this.task.id, {
              id: this.task.id,
              title: this.task.title,
              description: this.task.description,
              user_id: this.task.assignee.id,
              status: "In Progress",
            })
            .then((task) => task.status)
        );
      }
    },
  },
};
</script>
