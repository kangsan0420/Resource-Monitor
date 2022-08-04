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
      cvtSize: this.cvtSize,
    };
  },
  methods: {
    cvtSize(str) {
      const map = {'0': 1, 'K': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}
      var str = str.replace("B", "");
      let unit = str.slice(-1);
      return (unit === '0') ? 0 : parseFloat(str.slice(0,-1)) * map[unit]
    }
  }
}
</script>

<style lang="scss">
</style>
