
<template>
<div>
  <b-container >
    <b-row style="margin-top:20vh">
      <b-col>
        <div class="text-center">
          <img src="https://www.npinnovations.com/wp-content/uploads/2016/05/North-Park-sm.png" width="20%"/>
        </div>
      </b-col>
    </b-row>
    <b-row class="mt-4">
      <b-col sm="12" lg="6" offset-lg="3">
        <b-card class="p-3">
          <h4 class="mb-4">Login</h4>
          <b-form @submit.prevent="onLogin">
            <b-form-group>
              <b-form-input @click="clearFormError" v-model="id" type="text" placeholder="Username" required/>
            </b-form-group>

            <b-form-group>
              <b-form-input @click="clearFormError" v-model="password" type="password" placeholder="Password" required/>
            </b-form-group>
            <div class="text-center">
              <b-button type="submit" variant="primary" style="width:40%">Sign In</b-button>
            </div>
          </b-form>
          <p class="login-error text-center">{{error}}</p>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>
<script>
  import axios from 'axios'
  export default{
      data(){
        return {
          isFormError:false,
          error:'',
          id:'',
          password:''
        }
      },
      methods:{

        onLogin(data){
            let loginData = {
                id:this.id,
                password:this.password
            }
            axios.post(`http://localhost:5000/login`,loginData)
            .then(response => {
              if(response.status == 200){
                  this.$router.push({path:'data'});
                //   this.$store.commit('login',this.userId);
              }
            })
            .catch(e => {
              if(e.response.status == 500){
                  this.isFormError = true;
                  this.error = e.response.data.data;
              }
            })
        },
        clearFormError(){
          this.isFormError = false;
          this.error = '';
        }
      }
  }
</script>
<style scoped>
  .login-error{

      background-color:'red'
  }
</style>
