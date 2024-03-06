<script setup lang="ts">
import { PropType } from 'vue'
import Project from '@/types/Project'

defineProps({
  project: {
    type: Object as PropType<Project>,
    required: true,
  },
})
</script>

<template>
  <v-card class="full-height" height="150">
    <v-card-text class="full-height pa-2 d-flex flex-column justify-center">
      <div class="pb-3 text-h5">{{ project.project }}</div>
      <div class="text-h6">{{ project.books.length }} ZIM</div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
div {
  text-align: center;
}
.full-height {
  height: 100%;
}
</style>
