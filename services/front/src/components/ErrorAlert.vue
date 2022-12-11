<template>
  <q-banner rounded class="bg-red text-white" :class="{ hidden: !show }">
    {{ message }}
  </q-banner>
</template>

<script>
export default {
  name: "ErrorAlert",
  props: {
    show: {
      type: Boolean,
      default: false,
      required: true,
    },
    message: {
      type: String,
      default: "",
      required: true,
    },
  },
};
</script>
