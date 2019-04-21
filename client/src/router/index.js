import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Tickets from '@/components/Tickets';
import Login from '@/components/Login';
import Charts from '@/components/Charts';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/tickets',
      name: 'Tickets',
      component: Tickets,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/charts',
      name: 'Charts',
      component: Charts,
    },
    {
      path: '*',
      redirect: '/login',
    }
  ],
  mode: 'history',
});
