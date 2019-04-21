<template>
    <b-navbar fixed ="top" toggleable="lg" type="dark" variant="info">
        <b-navbar-brand class="logo-font">Ticketr</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
                <b-nav-item v-bind:active="this.$route.path=='/charts'" :to="{path:'/charts'}">Charts</b-nav-item>
                <b-nav-item v-bind:active="this.$route.path=='/tickets'" :to="{path:'/tickets'}">Tickets</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
                <img src="@/assets/baseline-person-24px.svg"/>
                <b-nav-item-dropdown right>
                
                <!-- Using 'button-content' slot -->
                <template slot="button-content">{{this.logged_user.charAt(0).toUpperCase() + this.logged_user.slice(1)}}</template>
                <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>

<script>
import { store } from './store.js'
export default {
    data() {
        return {
            logged_user: store.state.logged_user,
        };
    },
  methods: {
      logout() {
          store.state.logged_in = false;
            store.state.logged_user = '';
          this.$router.push({path:'/'})
      }
  }
};
</script>
<style>
.logo-font {
    font-weight: 575;
}
.bg-info {
    background-color: #01479B !important;
}
</style>
