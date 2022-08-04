<template>
  <div>
    <div id="memories">
      <h1>
        Memories
        <b-button pill variant="outline-dark" @click="get_memories_refresh">
          <b-icon icon="arrow-clockwise" aria-hidden="true" :animation="refreshing ? 'spin' : 'none'"/>
        </b-button>
      </h1>
      <p>Last Updated: {{lastUpdated}}</p>
      <b-overlay :show="refreshing">
      <b-table striped hover :items="allMemories" :fields="fields">
        <template #cell(Used(%))="row">
          <b-progress :value="cvtSize(row.item.used)" :max="cvtSize(row.item.total)" show-progress />
        </template>
      </b-table>
      </b-overlay>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MemoryTab",
  data() {
    return {
      fields: ['host', 'total', 'used', 'free', 'shared', 'buff/cache', 'available', 'Used(%)'],
      allMemories: [],
      refreshing: false,
      lastUpdated: "none",
    }
  },
  mounted() {
    this.get_memories()
  },
  inject: ["backend_url", "cvtSize"],
  methods: {
    get_memories() {
      axios
        .get(this.backend_url + "/memory")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allMemories = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        });
    },
    get_memories_refresh() {
      this.refreshing = true
      axios
        .get(this.backend_url + "/memory/refresh")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allMemories = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        })
        .finally(() => {
          this.refreshing = false
        });
    },
  }
}
</script>