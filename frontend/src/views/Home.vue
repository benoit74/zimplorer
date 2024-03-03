<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">

import { onMounted } from 'vue'
import { useMainStore } from '../stores/main'

const store = useMainStore()
onMounted(() => {
  store.fetchDummy()
})
</script>

<template>
  <v-app v-if="store.dummyValue" id="home">
    <v-main>
      Hello! Value is "{{ store.dummyValue }}".
    </v-main>
  </v-app>
</template>

<style scoped>
.v-main {
  background-color: rgb(243, 239, 245);
}
</style>
