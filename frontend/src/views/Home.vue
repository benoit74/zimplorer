<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { watch } from 'vue'
import { useMainStore } from '../stores/main'
import { storeToRefs } from 'pinia'
import ProjectCard from '@/components/ProjectCard.vue'

const store = useMainStore()
const { query, projects } = storeToRefs(store)

watch(query, () => store.performSearch())
</script>

<template>
  <v-app id="home">
    <v-layout class="rounded rounded-md">
      <!--
      <v-app-bar title="Application bar"></v-app-bar>

      <v-navigation-drawer>
        <v-list>
          <v-list-item title="Navigation drawer"></v-list-item>
          <v-list-item title="Navigation drawer"></v-list-item>
          <v-list-item title="Navigation drawer"></v-list-item>
        </v-list>
      </v-navigation-drawer>
-->
      <v-main
        class="d-flex flex-column"
        :scrollable="true"
        style="min-height: 300px"
      >
        <div id="search" class="d-flex flex-column align-center">
          <v-text-field
            v-model="query"
            clearable
            placeholder="Search a ZIM (type at least 3 chars)"
            prepend-icon="fa-magnifying-glass"
          ></v-text-field>
          <div v-if="store.isLoading" id="progress">
            <v-progress-linear
              :model-value="store.progress"
            ></v-progress-linear>
            <v-progress-linear indeterminate></v-progress-linear>
          </div>
          <div v-if="store.hitsLimitReached">
            More than 1000 ZIMs found, please refine your search to see all
          </div>
        </div>

        <v-container v-if="projects">
          <v-row id="results">
            <v-col v-for="project in projects" :key="project.project" cols="4">
              <ProjectCard :project="project" />
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-layout>
  </v-app>
</template>

<style scoped>
.v-main {
  background-color: rgb(243, 239, 245);
}

#search {
  margin-top: 10em;
  margin-bottom: 4em;
}

#search .v-input {
  width: 800px;
}

#search div#progress {
  width: 797px;
  padding-left: 38px;
  margin-top: -32px;
  margin-bottom: 24px;
}

#results {
  margin: 1em 10em 5em 10em;
}
</style>
