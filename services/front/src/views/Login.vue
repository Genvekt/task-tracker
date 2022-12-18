<template>
  <q-page
    class="bg-light-green window-height window-width row justify-center items-center"
  >
    <div class="column">
      <div class="row">
        <h5 class="text-h5 text-white q-my-md">Task Manager</h5>
      </div>
      <div class="row">
        <q-card class="q-pa-lg shadow-2" style="max-width: 500px">
          <q-form class="q-gutter-md" @submit="handleLogin">
            <q-card-section>
              <q-input
                filled
                v-model="user.username"
                type="email"
                class="q-pb-sm"
                label="Email"
              />
              <q-input
                filled
                v-model="user.password"
                type="password"
                class="q-pb-sm"
                label="Password"
              />
            </q-card-section>
            <q-card-actions class="q-px-md">
              <q-btn
                unelevated
                color="light-green"
                type="submit"
                label="Login"
              />
            </q-card-actions>
            <q-card-section class="text-center q-pa-none">
              <p class="text-grey-6">Not reigistered? Created an Account</p>
            </q-card-section>
          </q-form>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      user: {},
      loading: false,
      message: "",
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.push("/profile");
    }
  },
  methods: {
    handleLogin() {
      this.loading = true;
      if (this.user.username && this.user.password) {
        this.$store.dispatch("auth/login", this.user).then(
          () => {
            this.$router.push("/profile");
          },
          (error) => {
            this.loading = false;
            this.message =
              (error.response && error.response.data) ||
              error.message ||
              error.toString();
          }
        );
      }
    },
  },
};
</script>
