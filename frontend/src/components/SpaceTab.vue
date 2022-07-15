<template>
  <div>
    <div id="spaces">
      <h1>
        All Spaces
        <b-button pill variant="outline-dark" @click="get_space_refresh">
          <b-icon icon="arrow-clockwise" aria-hidden="true" :animation="refreshing ? 'spin' : 'none'"/>
        </b-button>
      </h1>
      <p>Last Updated: {{lastUpdated}}</p>
      <b-overlay :show="refreshing">
      <b-table striped hover :items="allSpaces" :fields="fields">
        <template #cell(Used(%))="row">
          <b-progress :value="cvtSize(row.item.Used)" :max="cvtSize(row.item.Size)" show-progress />
        </template>
      </b-table>
      </b-overlay>
    </div>
    <div id="space_detailed">
      <h1>Detailed</h1>
      <b-form-select v-model="selectedHost" :options="hosts" @change="get_space_detail"></b-form-select>
      <b-overlay :show="gettingDetailed">
        <b-table striped hover :items="detailed"></b-table>
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
      fields: ['host', 'Size', 'Used', 'Used(%)'],
      allSpaces: [],
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

      this.allSpaces.forEach(function (item, index, array) {
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
    this.get_spaces()
  },
  inject: ["backend_url", "cvtSize"],
  methods: {
    get_spaces() {
      axios
        .get(this.backend_url + "/space")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allSpaces = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        });
    },
    get_space_refresh() {
      this.refreshing = true
      axios
        .get(this.backend_url + "/space/refresh")
        .then((response) => {
          this.lastUpdated = response.data["time"]
          this.allSpaces = response.data["data"]
        })
        .catch((error) => {
          console.log("Error:", error)
        })
        .finally(() => {
          this.refreshing = false
        });
    },
    get_space_detail() {
      if (this.selectedHost) {
        this.gettingDetailed = true
        axios
          .get(this.backend_url + "/space/detail?host=" + this.selectedHost)
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