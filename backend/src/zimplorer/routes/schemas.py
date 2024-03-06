from pydantic import Field

from zimplorer.business.schemas import CamelModel


class DummyData(CamelModel):
    """Dummy data for demo"""

    value: str


class SearchRequest(CamelModel):
    """A search request"""

    q: str | None = Field(default=None)
    offset: int | None = Field(default=None)
    limit: int | None = Field(default=None)
    hits_per_page: int | None = Field(default=None)
    page: int | None = Field(default=None)
    filter: str | None = Field(default=None)
    attributes_to_retrieve: list[str] | None = Field(default=None)
    attribute_to_crop: list[str] | None = Field(default=None)
    crop_length: int | None = Field(default=None)
    crop_marker: str | None = Field(default=None)
    attributes_to_highlight: list[str] | None = Field(default=None)
    highlight_pre_tag: str | None = Field(default=None)
    highlight_post_tag: str | None = Field(default=None)
    show_matched_position: bool | None = Field(default=None)
    sort: list[str] | None = Field(default=None)
    matching_strategy: str | None = Field(default=None)
    show_ranking_score: bool | None = Field(default=None)
    attributes_to_search_on: list[str] | None = Field(default=None)


class BookModel(CamelModel):
    """A book"""

    book_id: str
    project: str
    language: str
    selection: str
    flavor: str | None = Field(default=None)
    category: str | None = Field(default=None)
    url: str
    size: int
    media_count: int
    article_count: int
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    creator: str | None = Field(default=None)
    publisher: str | None = Field(default=None)
    tags: list[str]
    favicon: str


class BookSearchHit(BookModel):
    """A hit for a book search"""

    formatted: BookModel = Field(alias="_formatted", default=None)


class BookFacetDistibution(CamelModel):
    project: dict[str, int]
    language: dict[str, int]
    selection: dict[str, int]
    flavour: dict[str, int]
    category: dict[str, int]
    creator: dict[str, int]
    publisher: dict[str, int]
    tags: dict[str, int]


class BookFacetStat(CamelModel):
    min: int
    max: int


class BookFacetStats(CamelModel):
    size: BookFacetStat | None = Field(default=None)
    media_count: BookFacetStat | None = Field(default=None)
    article_count: BookFacetStat | None = Field(default=None)


class BookSearchResult(CamelModel):
    """A book search result"""

    hits: list[BookSearchHit]
    offset: int | None = Field(default=None)
    limit: int | None = Field(default=None)
    estimated_total_hits: int | None = Field(default=None)
    total_hits: int | None = Field(default=None)
    total_pages: int | None = Field(default=None)
    hits_per_page: int | None = Field(default=None)
    page: int | None = Field(default=None)
    facet_distribution: BookFacetDistibution | None = Field(default=None)
    facet_stats: BookFacetStats | None = Field(default=None)
    processing_time_ms: int
    query: str
