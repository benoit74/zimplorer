/**
 * A book
 */
export default interface Book {
  bookId: string
  language: string
  selection: string
  flavor: string | null
  category: string | null
  url: string
  size: number
  mediaCount: number
  articleCount: number
  title: string | null
  description: string | null
  creator: string | null
  publisher: string | null
  tags: string[] | null
  favicon: string | null
}
