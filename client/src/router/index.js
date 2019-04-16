import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Books from '@/components/Books';
import Order from '@/components/Order';
import OrderComplete from '@/components/OrderComplete';
import Data from '@/components/Data';
import login from '@/components/login';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
    {
      path: '/order/:id',
      name: 'Order',
      component: Order,
    },
    {
      path: '/complete/:id',
      name: 'OrderComplete',
      component: OrderComplete,
    },
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
  ],
  mode: 'history',
});
