import { defineStore } from 'pinia'
import axios from 'axios'

export type RootState = {
  isLoading: boolean
  errorMessage: string | null
  dummyValue: string | null
}
export const useMainStore = defineStore('main', {
  state: () =>
    ({
      isLoading: false,
      errorMessage: null,
      dummyValue: null,
    }) as RootState,
  getters: {
  },
  actions: {
    async fetchDummy() {
      this.isLoading = true
      this.errorMessage = null
      try {
        const data = await axios.get(
          import.meta.env.VITE_BACKEND_ROOT_API +
            '/dummy',
        )
        this.dummyValue = data.data.value
      } catch (error) {
        this.errorMessage = 'Failed to load dummy'
        this.dummyValue = null
        // this is temporary until we have implemented proper error display
        // in the UI.
        // eslint-disable-next-line no-console
        console.log(error)
      }
      this.isLoading = false
    },
  },
})
