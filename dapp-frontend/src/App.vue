<template>
  <v-app>
    <v-app-bar app color="white" dark v-if="currentRouteName != '/'">
      <v-spacer></v-spacer>

      <v-btn color="primary"> Login </v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "App",

  data: () => ({
    //
  }),
  computed: {
    currentRouteName() {
      return this.$route.path;
    },
  },
});
</script>
