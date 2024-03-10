<script setup lang="ts">
import { PropType } from 'vue'

defineProps({
  title: {
    type: String,
    required: true,
  },
  facetData: {
    type: Object as PropType<Record<string, number>>,
    required: true,
  },
})
</script>

<template>
  <b>{{ title }}:</b>
  <ul>
    <li v-for="facet in Object.keys(facetData)" :key="facet">
      {{ facet }}: {{ facetData[facet] }}
    </li>
  </ul>
</template>

<style scoped></style>
