<template>
    <b-navbar fixed ="top" toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="#">Dashboard</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
                <b-nav-item class="nav-item" :to="{path:'/'}">Analytics</b-nav-item>
                <b-nav-item  :to="{path:'/data'}" >Data</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">

                <b-nav-item-dropdown right>
                <!-- Using 'button-content' slot -->
                <template slot="button-content"><em>User</em></template>
                <b-dropdown-item >Profile</b-dropdown-item>
                <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>

<script>
export default {
  methods: {
      logout() {
          this.$router.push({path:'/'})
          //state management
      }
  }
};
</script>
