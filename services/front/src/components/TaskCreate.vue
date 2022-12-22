<template>
  <q-form
    @submit="onSubmit"
    @reset="onReset"
    class="q-gutter-md row self-center q-px-md"
  >
    <q-input
      class="col-2"
      filled
      v-model="newTask.title"
      label="Title"
      lazy-rules
    />
    <q-input
      class="col-5"
      filled
      v-model="newTask.description"
      label="Description"
      lazy-rules
    />
    <q-btn
      class="col-1"
      icon="far fa-plus"
      label="Submit"
      type="submit"
      color="primary"
      :loading="this.loading"
    />
    <q-btn
      outline
      class="col-1"
      icon="far fa-redo"
      label="Reset"
      type="reset"
      color="primary"
    />
  </q-form>
</template>

<script>
import { db } from "@/main";

export default {
  name: "TaskCreate",
  data() {
    return {
      options: [],
      loading: false,
      newTask: {
        title: "",
        description: "",
      },
    };
  },
  methods: {
    onSubmit: function () {
      this.loading = true;
      db.createOne("tasks", {
        title: this.newTask.title,
        description: this.newTask.description,
      })
        .then((task) => {
          this.loading = false;
          this.newTask = {
            title: "",
            description: "",
          };
          return this.$emit("taskCreated", task);
        })
        .catch((error) => {
          this.loading = false;
          if (error && error.response) {
            let message = "";
            if (typeof error.response.data.detail == "string") {
              message = error.response.data.detail;
            } else {
              message = error.response.statusText;
            }
            this.$emit("errorResponce", message);
          }
        });
    },
    onReset: function () {
      this.newTask = {
        title: "",
        description: "",
      };
    },
  },
};
</script>

<style scoped></style>
