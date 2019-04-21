import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Data from '@/components/Data';
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
      path: '/data',
      name: 'Data',
      component: Data,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/charts',
      name: 'charts',
      component: Charts,
    },
    {
      path: '*',
      redirect: '/login',
    }
  ],
  mode: 'history',
});
