import SearchBook from './SearchBook'
/**
 * A book search result
 */
export default interface SearchResult {
  hits: SearchBook[]
  offset: number | undefined
  limit: number | undefined
  estimatedTotalHits: number | undefined
  totalHits: number | undefined
  totalPages: number | undefined
  hitsPerPage: number | undefined
  page: number | undefined
}
