const AUTH_API_URL = "http://localhost:8001/";
import axios from "axios";

class AuthService {
  login(user) {
    let loginFormData = new FormData();
    loginFormData.append("username", user.username);
    loginFormData.append("password", user.password);
    return axios
      .post(AUTH_API_URL + "login", loginFormData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((response) => {
        if (response.data.access_token) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem("user");
  }
}

export default new AuthService();
