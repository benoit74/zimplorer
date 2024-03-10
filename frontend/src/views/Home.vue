<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { watch } from 'vue'
import { useMainStore } from '../stores/main'
import { storeToRefs } from 'pinia'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectDetailsCard from '@/components/ProjectDetailsCard.vue'
import FacetFilter from '@/components/FacetFilter.vue'

const store = useMainStore()
const { query, projects, searchResult, selectedProject } = storeToRefs(store)

watch(query, () => store.performSearch())
</script>

<template>
  <v-app id="home">
    <v-layout class="rounded rounded-md">
      <!--
      <v-app-bar title="Application bar"></v-app-bar>
-->

      <v-navigation-drawer>
        <v-list>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Project"
              :facet-data="searchResult?.facetDistribution?.project"
            />
          </v-list-item>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Language"
              :facet-data="searchResult?.facetDistribution?.language"
            />
          </v-list-item>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Selection"
              :facet-data="searchResult?.facetDistribution?.selection"
            />
          </v-list-item>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Flavour"
              :facet-data="searchResult?.facetDistribution?.flavour"
            />
          </v-list-item>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Category"
              :facet-data="searchResult?.facetDistribution?.category"
            />
          </v-list-item>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Creator"
              :facet-data="searchResult?.facetDistribution?.creator"
            />
          </v-list-item>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Publisher"
              :facet-data="searchResult?.facetDistribution?.publisher"
            />
          </v-list-item>
          <v-list-item v-if="searchResult?.facetDistribution">
            <FacetFilter
              title="Tags"
              :facet-data="searchResult?.facetDistribution?.tags"
            />
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
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

        <v-expand-transition>
          <ProjectDetailsCard
            v-if="selectedProject"
            v-show="selectedProject"
            id="project"
            :project="selectedProject"
          />
        </v-expand-transition>

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
  margin-top: 2em;
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

#project {
  margin: 1em 10em 5em 10em;
}
</style>
