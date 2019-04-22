
<template>
  <div>
    <b-container>
      <b-row style="margin-top:25vh">
        <b-col>
          <div class="text-center">
            <h3 class="logo-font">Ticketr</h3>
          </div>
        </b-col>
      </b-row>
      <b-row class="mt-4">
        <b-col sm="6" lg="4" offset-lg="4" offset-sm="3">
          <b-card class="p-3">
            <b-form @submit.prevent="onLogin">
              <b-form-group>
                <b-form-input
                  @click="clearFormError"
                  v-model="username"
                  type="text"
                  placeholder="Username"
                  required
                />
              </b-form-group>

              <b-form-group>
                <b-form-input
                  @click="clearFormError"
                  v-model="password"
                  type="password"
                  placeholder="Password"
                  required
                />
              </b-form-group>
              <div class="text-center">
                <b-button
                  class="btn-nptheme"
                  type="submit"
                  variant="primary"
                  style="width:40%"
                >Sign In</b-button>
              </div>
            </b-form>
            <b-row style="margin-top:2vh">
              <b-col>
                <p
                  style="color:#d32f2f;"
                  class="text-center"
                  v-if="logout_init"
                >You have been logged out.</p>
                <p
                  style="color:#d32f2f;"
                  class="text-center"
                  v-else-if="loginError"
                >Invalid credentials</p>
                <p
                  style="color:#d32f2f;"
                  class="text-center"
                  v-else-if="unauth"
                >Log in to access page</p>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import { store } from "./store.js";

export default {
  data() {
    return {
      loginError: false,
      username: "",
      password: "",
      unauth: store.state.unauth_attempt,
      logout_init: store.state.logout_init
    };
  },
  methods: {
    onLogin(data) {
      this.logout_init = false;
      store.state.logout_init = false;
      this.unauth = false;
      store.state.unauth_attempt = false;
      var loginData = {
        username: this.username,
        password: this.password
      };
      axios
        .post(store.server_url + `/login`, loginData)
        .then(response => {
          if (response.status == 200) {
            this.loginError = false;
            store.state.unauth_attempt = false;
            store.state.logged_in = true;
            store.state.logged_user = loginData.username;
            this.$router.push(store.state.attempt_path);
          } else {
            this.loginError = true;
          }
        })
        .catch(e => {
          if (e.response.status == 401) {
            this.loginError = true;
          }
        });
    },
    clearFormError() {
      this.isFormError = false;
      this.error = "";
    }
  },
  created() {
    this.logout_init = store.state.logout_init;
    if (store.state.logged_in) {
      store.state.unauth_attempt = false;
      this.unauth = false;
      this.$router.push("charts");
    } else if (store.state.unauth_attempt) {
      this.unauth = true;
    }
  }
};
</script>

<style scoped>
.logo-font {
  font-weight: 575;
}

.btn-nptheme {
  color: #ffffff;
  background-color: #4f91cd;
  border-color: #4683bd;
}

.btn-nptheme:hover,
.btn-nptheme:focus,
.btn-nptheme:active,
.btn-nptheme.active,
.open .dropdown-toggle.btn-nptheme {
  color: #ffffff;
  background-color: #34618c;
  border-color: #4683bd;
}

.btn-nptheme:active,
.btn-nptheme.active,
.open .dropdown-toggle.btn-nptheme {
  background-image: none;
}

.btn-nptheme.disabled,
.btn-nptheme[disabled],
fieldset[disabled] .btn-nptheme,
.btn-nptheme.disabled:hover,
.btn-nptheme[disabled]:hover,
fieldset[disabled] .btn-nptheme:hover,
.btn-nptheme.disabled:focus,
.btn-nptheme[disabled]:focus,
fieldset[disabled] .btn-nptheme:focus,
.btn-nptheme.disabled:active,
.btn-nptheme[disabled]:active,
fieldset[disabled] .btn-nptheme:active,
.btn-nptheme.disabled.active,
.btn-nptheme[disabled].active,
fieldset[disabled] .btn-nptheme.active {
  background-color: #4f91cd;
  border-color: #4683bd;
}

.btn-nptheme .badge {
  color: #4f91cd;
  background-color: #ffffff;
}
</style>
