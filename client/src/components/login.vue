
<template>
<div>
  <b-container >
    <b-row style="margin-top:25vh">
      <b-col>
        <div class="text-center">
          <h3>Login</h3>
        </div>
      </b-col>
    </b-row>
    <b-row class="mt-4">
      <b-col sm="12" lg="4" offset-lg="4">
        <b-card class="p-3">
          <b-form @submit.prevent="onLogin">
            <b-form-group>
              <b-form-input @click="clearFormError" v-model="username" type="text" placeholder="Username" required/>
            </b-form-group>

            <b-form-group>
              <b-form-input @click="clearFormError" v-model="password" type="password" placeholder="Password" required/>
            </b-form-group>
            <div class="text-center">
              <b-button class="btn-nptheme" type="submit" variant="primary" style="width:40%">Sign In</b-button>
            </div>
          </b-form>
          <b-row style="margin-top:2vh">
            <b-col>
                <p style="color:#d32f2f;" class="text-center" v-if="loginError" >Invalid credentials</p>
            </b-col>
          </b-row>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script>
  import axios from 'axios'
  import { store } from "./store.js";
  
  export default{
      data(){
        return {
          loginError:false,
          username:'',
          password:''
        }
      },
      methods:{
        onLogin(data){
            var loginData = {
                username:this.username,
                password:this.password
            }
            axios.post(`http://localhost:5000/login`,loginData)
            .then(response => {
              if(response.status == 200){
                  this.loginError = false;
                  store.state.logged_in = true;
                  store.state.logged_user = loginData.username;
                  this.$router.push({path:'data'});
                //   this.$store.commit('login',this.userId);
              }
              else {
                  this.loginError = true;
              }
            })
            .catch(e => {
              if(e.response.status == 401){
                  this.loginError = true;
                //   this.error = e.response.data.data;
              }
            })
        },
        clearFormError(){
          this.isFormError = false;
          this.error = '';
        }
      },
      created() {
        if(store.state.logged_in) {
            this.$router.push('data')
        }
    },
  }
</script>

<style scoped>
  .login-error{
      background-color:'red'
  }
  .btn-nptheme { 
  color: #ffffff; 
  background-color: #4F91CD; 
  border-color: #4683BD; 
} 
 
.btn-nptheme:hover, 
.btn-nptheme:focus, 
.btn-nptheme:active, 
.btn-nptheme.active, 
.open .dropdown-toggle.btn-nptheme { 
  color: #ffffff; 
  background-color: #34618C; 
  border-color: #4683BD; 
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
  background-color: #4F91CD; 
  border-color: #4683BD; 
} 
 
.btn-nptheme .badge { 
  color: #4F91CD; 
  background-color: #ffffff; 
}
</style>
