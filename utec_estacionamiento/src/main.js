// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import BootstrapVue from 'bootstrap-vue/dist/bootstrap-vue.esm';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

import listaCarros from './components/listaCarros'
import listaPagos from './components/listaPagos'
import loginUsuario from './components/loginUsuario'
import registrarCarro from './components/registrarCarro'

Vue.use(VueResource)
Vue.use(BootstrapVue);
Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    { path: '/', component: loginUsuario },
    { path: '/listaCarros', component: listaCarros },
    { path: '/registrarCarro', component: registrarCarro },
    { path: '/listaPagos', component: listaPagos }
  ]
})

Vue.config.productionTip = false
new Vue({
  router,
  components: { App },
  template: '<App/>'
}).$mount('#app')

