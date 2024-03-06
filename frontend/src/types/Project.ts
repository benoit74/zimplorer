import Book from './Book'

/**
 * A project with all existing books
 */
export default interface Project {
  project: string
  books: Book[]
}
