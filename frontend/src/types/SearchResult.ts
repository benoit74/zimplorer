import FacetDistribution from './FacetDistribution'
import SearchBook from './SearchBook'
/**
 * A book search result
 */
export default interface SearchResult {
  hits: SearchBook[]
  offset: number | null
  limit: number | null
  estimatedTotalHits: number | null
  totalHits: number | null
  totalPages: number | null
  hitsPerPage: number | null
  page: number | null
  facetDistribution: FacetDistribution | null
}
