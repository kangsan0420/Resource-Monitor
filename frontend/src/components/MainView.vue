<template>
  <div>
    <b-tabs content-class="mt-3">
      <b-tab title="Space" active><SpaceTab /></b-tab>
      <b-tab title="GPU"><GPUTab /></b-tab>
      <b-tab title="Memory"><MemoryTab /></b-tab>
      <b-tab title="Containers"><p><ContainerTab /></p></b-tab>
    </b-tabs>
  </div>
</template>

<script>
import SpaceTab from "./SpaceTab.vue"
import MemoryTab from "./MemoryTab.vue"
import GPUTab from "./GPUTab.vue"
import ContainerTab from "./ContainerTab.vue"

export default {
  name: "MainView",
  components: {
    SpaceTab,
    MemoryTab,
    GPUTab,
    ContainerTab,
  },
}
</script>
