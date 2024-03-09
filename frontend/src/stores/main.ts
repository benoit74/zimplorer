import { defineStore } from 'pinia'
import axios from 'axios'
import SearchRequest from '../types/SearchRequest'
import SearchResult from '../types/SearchResult'
import Project from '@/types/Project'
import Book from '@/types/Book'
import SearchBook from '@/types/SearchBook'

export type RootState = {
  isLoading: boolean
  progress: number
  errorMessage: string | null
  dummyValue: string | null
  query: string
  searchResult: SearchResult | null
  hitsLimitReached: boolean | null
  selectedProject: Project | null
}

const getBookFromSearchBook = function (searchBook: SearchBook): Book {
  return {
    bookId: searchBook.bookId,
    language: searchBook.language,
    selection: searchBook.selection,
    flavor: searchBook.flavor,
    category: searchBook.category,
    url: searchBook.url,
    size: searchBook.size,
    mediaCount: searchBook.mediaCount,
    articleCount: searchBook.articleCount,
    title: searchBook.title,
    description: searchBook.description,
    creator: searchBook.creator,
    publisher: searchBook.publisher,
    tags: searchBook.tags,
    favicon: searchBook.favicon,
  } as Book
}

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      isLoading: false,
      errorMessage: null,
      dummyValue: null,
      query: '',
      searchResult: null,
      hitsLimitReached: null,
      progress: 0,
      selectedProject: null,
    }) as RootState,
  getters: {
    projects: (state) =>
      state.searchResult?.hits.reduce((accumulator, currentValue) => {
        const project = accumulator.find(
          (element) => element.project === currentValue.project,
        )
        if (project) {
          project.books.push(getBookFromSearchBook(currentValue))
        } else {
          accumulator.push({
            project: currentValue.project,
            books: [getBookFromSearchBook(currentValue)],
          })
        }
        return accumulator
      }, [] as Project[]),
  },
  actions: {
    selectProject(project: Project | null) {
      this.selectedProject = project
    },
    async performSearch() {
      if (this.query.length < 3) {
        return
      }
      this.selectedProject = null
      this.isLoading = true
      this.progress = 0
      this.errorMessage = null
      try {
        let page = 1
        // eslint-disable-next-line no-constant-condition
        while (true) {
          const searchRequest: SearchRequest = {
            q: this.query,
            hitsPerPage: 100,
            page: page,
          }
          const data = await axios.post(
            import.meta.env.VITE_BACKEND_ROOT_API + '/books_search',
            searchRequest,
          )
          const searchPage: SearchResult = data.data
          this.progress =
            ((searchPage.page || 0) * 100) /
            (searchPage.totalPages === undefined ? 1 : searchPage.totalPages)
          if (page === 1) {
            this.searchResult = searchPage
            this.hitsLimitReached = this.searchResult?.totalHits === 1000
          } else {
            this.searchResult?.hits.push(...searchPage.hits)
          }
          if (
            !searchPage.page ||
            !searchPage.totalPages ||
            searchPage.page >= searchPage.totalPages
          ) {
            break
          }
          page += 1
        }
      } catch (error) {
        this.errorMessage = 'Failed to load search result'
        this.searchResult = null
        // this is temporary until we have implemented proper error display
        // in the UI.
        // eslint-disable-next-line no-console
        console.log(error)
      }
      this.isLoading = false
    },
  },
})
