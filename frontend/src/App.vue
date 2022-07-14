<template>
  <div id="app">
    <Navbar />
    <MainView />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import MainView from './components/MainView.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    MainView
  },
  mounted() {
    console.log('envs:', process.env);
  },
  data() {
    return {
      backend_url: `${process.env.VUE_APP_HOST_ADDR}:${process.env.VUE_APP_PORT_BACK}`,
    };
  },
  provide() {
    return {
      backend_url: this.backend_url,
    };
  }
}
</script>

<style lang="scss">
</style>
