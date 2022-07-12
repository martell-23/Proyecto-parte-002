<template>
  <div id="app">
    <li>
      <router-link to="/">Login</router-link>
      <router-link to="/listaCarros">listaCarros</router-link>
      <router-link to="/registrarCarro">registrarCarro</router-link>
      <router-link to="/listaPagos">listaPagos</router-link>
    </li>
    <router-view></router-view>
  </div>
</template>

<script>
import listaCarros from './components/listaCarros.vue'
import loginUsuario from './components/loginUsuario.vue'
import registrarCarro from './components/registrarCarro.vue'
import listaPagos from './components/listaPagos.vue'

export default {
  name: 'App',
  components: {
    loginUsuario,
    listaCarros,
    registrarCarro,
    listaPagos
  }
}
</script>
