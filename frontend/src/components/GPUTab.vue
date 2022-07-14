<template>
  <div>
    <div id="gpus">
      <h1>
        All GPUs
        <b-button pill variant="outline-dark" @click="get_GPUs_refresh">
          <b-icon icon="arrow-clockwise" aria-hidden="true" :animation="refreshing ? 'spin' : 'none'"/>
        </b-button>
      </h1>
      <p>Last Updated: {{lastUpdated}}</p>
      <b-overlay :show="refreshing">
        <b-table striped hover :items="allGPUs"></b-table>
      </b-overlay>
    </div>
    <div id="gpu_detailed">
      <h1>Detailed</h1>
      <b-form-select v-model="detailedSelectedHost" :options="hosts" @change="get_gpu_detailed"></b-form-select>
      <b-overlay :show="gettingDetailed">
        <b-table striped hover :items="detailed"></b-table>
      </b-overlay>
    </div>
    <div id="gpu_processes">
      <h1>Processes</h1>
      <b-form-select v-model="processesSelectedHost" :options="hosts" @change="get_gpu_processes"></b-form-select>
      <b-overlay :show="gettingProcesses">
        <b-table striped hover :items="processes"></b-table>
      </b-overlay>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SpaceTab",
  data() {
    return {
      allGPUs: [],
      refreshing: false,
      lastUpdated: "none",
      detailedSelectedHost: null,
      detailed: [],
      gettingDetailed: false,
      processesSelectedHost: null,
      processes: [],
      gettingProcesses: false,
    }
  },
  computed: {
    hosts() {
      let newDicts = [{ value: null, text: "Please select a host" }]

      this.allGPUs.forEach(function (item, index, array) {
        for (const [key, value] of Object.entries(item)) {
          if (key == "host") { 
            newDicts.push({"value": item[key], "text": item[key]})
          }
        }
      })
      return newDicts
    },
  },
  mounted() {
    this.get_GPUs()
  },
  inject: ["backend_url"],
  methods: {
    get_GPUs() {
      axios
        .get(this.backend_url + "/gpu")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allGPUs = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        });
    },
    get_GPUs_refresh() {
      this.refreshing = true
      axios
        .get(this.backend_url + "/gpu/refresh")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allGPUs = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        })
        .finally(() => {
          this.refreshing = false
        });
    },
    get_gpu_detailed() {
      if (this.detailedSelectedHost) {
        this.gettingDetailed = true
        axios
          .get(this.backend_url + "/gpu/detail?host=" + this.detailedSelectedHost)
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
    get_gpu_processes() {
      if (this.processesSelectedHost) {
        this.gettingProcesses = true
        axios
          .get(this.backend_url + "/gpu/processes?host=" + this.processesSelectedHost)
          .then((response) => {
            this.processes = response.data
          })
          .catch((error) => {
            console.log("Error:", error)
          })
          .finally(() => {
            this.gettingProcesses = false
          });
      }
      else {
        this.processes = []
      }
    },
  }
}
</script>