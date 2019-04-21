export const store = {
    state: {
      logged_in: false,
      logged_user: '',
    },
    server_url: `http://localhost:5000`,
    logIn(username) {
      this.state.logged_in = true;
      this.state.logged_user = username;
    },
    logOut() {
        this.state.logged_in = false;
        this.state.logged_user = '';
      }
  };