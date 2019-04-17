import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Data from '@/components/Data';
import login from '@/components/login';

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
      name: 'login',
      component: login,
    },
    {
      path: '*',
      redirect: '/login',
    }
  ],
  mode: 'history',
});
