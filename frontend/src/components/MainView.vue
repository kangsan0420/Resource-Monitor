<template>
  <div>
    <b-tabs content-class="mt-3">
      <b-tab title="Space" active><SpaceTab /></b-tab>
      <b-tab title="GPU"><GPUTab /></b-tab>
      <b-tab title="Memory"><MemoryTab /></b-tab>
      <b-tab title="Users" disabled><p>I"m a disabled tab!</p></b-tab>
    </b-tabs>
  </div>
</template>

<script>
import SpaceTab from "./SpaceTab.vue"
import MemoryTab from "./MemoryTab.vue"
import GPUTab from "./GPUTab.vue"

export default {
  name: "MainView",
  components: {
    SpaceTab,
    MemoryTab,
    GPUTab,
  },
}
</script>
