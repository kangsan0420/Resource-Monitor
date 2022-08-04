<template>
  <div>
    <div id="containers">
      <h1>
        Containers
        <b-button pill variant="outline-dark" @click="get_container_refresh">
          <b-icon icon="arrow-clockwise" aria-hidden="true" :animation="refreshing ? 'spin' : 'none'"/>
        </b-button>
      </h1>
      <p>Last Updated: {{lastUpdated}}</p>
      <b-overlay :show="refreshing">
      <b-table striped hover :items="allContainers" :fields="fields">
        <template #cell(Used(%))="row">
          <b-progress :value="cvtSize(row.item.Used)" :max="cvtSize(row.item.Size)" show-progress />
        </template>
      </b-table>
      </b-overlay>
    </div>
    <div id="container_detailed">
      <h1>Detailed</h1>
      <b-form-select v-model="selectedHost" :options="hosts" @change="get_container_detail"></b-form-select>
      <b-overlay :show="gettingDetailed">
        <b-table striped hover :items="detailed"></b-table>
      </b-overlay>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ContainerTab",
  data() {
    return {
      fields: ['Host', 'Active', 'Exited'],
      allContainers: [],
      refreshing: false,
      lastUpdated: "none",
      selectedHost: null,
      detailed: [],
      gettingDetailed: false,
    }
  },
  computed: {
    hosts() {
      let newDicts = [{ value: null, text: "Please select a host" }]

      this.allContainers.forEach(function (item, index, array) {
        for (const [key, value] of Object.entries(item)) {
          if (key == "Host") { 
            newDicts.push({"value": item[key], "text": item[key]})
          }
        }
      })
      return newDicts
    },
  },
  mounted() {
    this.get_containers()
  },
  inject: ["backend_url", "cvtSize"],
  methods: {
    get_containers() {
      axios
        .get(this.backend_url + "/container")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allContainers = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        });
    },
    get_container_refresh() {
      this.refreshing = true
      axios
        .get(this.backend_url + "/container/refresh")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allContainers = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        })
        .finally(() => {
          this.refreshing = false
        });
    },
    get_container_detail() {
      if (this.selectedHost) {
        this.gettingDetailed = true
        axios
          .get(this.backend_url + "/container/detail?host=" + this.selectedHost)
          .then((response) => {
            this.detailed = response.data
          })
          .catch((error) => {
            console.log("Error:", error)
          })
          .finally(() => {
            this.gettingDetailed = false
          });
      }
      else {
        this.detailed = []
      }
    },
  }
}
</script>