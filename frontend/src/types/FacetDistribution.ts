/**
 * All facets distribution
 */
export default interface FacetDistribution {
  project: Record<string, number>
  language: Record<string, number>
  selection: Record<string, number>
  flavour: Record<string, number>
  category: Record<string, number>
  creator: Record<string, number>
  publisher: Record<string, number>
  tags: Record<string, number>
}
