import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";

import { DataProvider } from "@/services/DataProvider";
import store from "./store";
/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { Quasar } from "quasar";
import quasarUserOptions from "./quasar-user-options";
import "./assets/tailwind.css";
library.add(fas);
library.add(far);

const app = createApp(App).use(Quasar, quasarUserOptions);
app.use(router);
app.use(store);

//Make data provider instance

export const db = DataProvider(
  axios.create({
    baseURL: `http://127.0.0.1:8000/api/`,
    headers: {
      Authorization: "Bearer {token}",
    },
  })
);
app.component("font-awesome-icon", FontAwesomeIcon);

app.mount("#app");
