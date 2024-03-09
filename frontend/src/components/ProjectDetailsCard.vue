<script setup lang="ts">
import { PropType } from 'vue'
import Project from '@/types/Project'
import { useMainStore } from '@/stores/main'
import Book from '@/types/Book'

const store = useMainStore()

const getTwelveBooks = function (project: Project): Book[] {
  if (project.books.length <= 12) {
    return project.books
  }
  return project.books.slice(0, 11)
}

defineProps({
  project: {
    type: Object as PropType<Project | null>,
    required: true,
  },
})
</script>

<template>
  <v-card v-if="project" class="full-height" @click="store.selectProject(null)">
    <v-card-text class="pt-6 pa-2 d-flex flex-column justify-center">
      <div class="pb-3 text-h5">{{ project.project }}</div>
      <v-container id="books">
        <v-row>
          <v-col
            v-for="book in getTwelveBooks(project)"
            :key="book.bookId"
            cols="4"
          >
            <v-card>
              <v-card-text>{{ book.title }} </v-card-text>
              <v-card-text>{{ book.description }}</v-card-text>
              <v-card-text>{{ book.language }}</v-card-text>
              <v-card-text>{{ book.creator }}</v-card-text>
              <v-card-text>{{ book.publisher }}</v-card-text>
              <v-card-text>{{ book.flavor }}</v-card-text>
              <v-card-text>{{ book.category }}</v-card-text>
              <v-card-text>{{ book.tags }}</v-card-text>
            </v-card>
          </v-col>
          <v-col v-if="project.books.length > 12" cols="4"> More ... </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<style scoped>
div {
  text-align: center;
}

#books .v-card {
  height: 100%;
}
</style>
