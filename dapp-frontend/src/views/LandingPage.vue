<template>
  <v-container fluid class="pa-0 fill-height">
    <v-carousel
      continuous
      cycle
      hide-delimiter-background
      hide-delimiters
      :show-arrows="false"
      style="position: absolute; height: 100%"
    >
      <v-overlay absolute>
        <div
          fill-height
          class="d-flex flex-column align-center justify-center"
          style="width: 100vw"
        >
          <div class="landing-title text-center mt-n16">
            <h1 class="mb-10 text-h1">Blockchain Dashboard</h1>
            <h4 class="text-h5 mt-10 mb-10">
              Track blockchain transactions in real-time with our dashboard. Get
              comprehensive views for crypto enthusiasts and businesses using
              blockchain tech.
            </h4>
          </div>
          <v-dialog v-model="popupOpen" width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                @click="
                  {
                    popupOpen = true;
                  }
                "
                x-large
                outlined
                color="white"
                class="px-10 py-5 mt-10"
                v-bind="attrs"
                v-on="on"
                >Log in</v-btn
              >
            </template>

            <v-card>
              <v-container class="d-flex flex-column pa-6 pr-7">
                <v-text-field
                  prepend-icon="fa-solid fa-user"
                  label="Username"
                ></v-text-field>
                <v-text-field
                  prepend-icon="fa-solid fa-key"
                  label="Password"
                ></v-text-field>
                <div class="d-flex justify-space-between mt-2">
                  <v-btn color="" outlined @click="popupOpen = false">
                    Cancel
                  </v-btn>
                  <v-btn color="primary" @click="popupOpen = false">
                    Log in
                  </v-btn>
                </div>
              </v-container>
            </v-card>
          </v-dialog>
        </div>
      </v-overlay>
      <v-carousel-item
        v-for="(item, index) in images"
        v-bind:key="index"
        class="fill-height"
        style="height: 100vh"
      >
        <v-img :src="require('@/assets/' + item)" height="100vh"></v-img>
      </v-carousel-item>
    </v-carousel>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      images: ["landing-1.jpg", "landing-2.jpg", "landing-3.jpg"],
      popupOpen: false,
    };
  },
  mounted: function () {
    let elHtml = document.getElementsByTagName("html")[0];
    elHtml.style.overflowY = "hidden";
  },
  destroyed: function () {
    let elHtml = document.getElementsByTagName("html")[0];
    elHtml.style.overflowY = null;
  },
};
</script>

<style>
.v-carousel__item {
  height: inherit !important;
}
.landing-title {
  /* margin-top: -350px; */
  max-width: 50%;
}
</style>
