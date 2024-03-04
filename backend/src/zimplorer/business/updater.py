import base64
import functools
import hashlib
import json
from http import HTTPStatus
from pathlib import Path
from urllib.parse import urljoin

import requests
from defusedxml import ElementTree

from zimplorer.constants import logger

CHUNCK_DOWNLOAD_SIZE = 8096


class Updater:

    def __init__(
        self,
        favicons_path: Path,
        json_library_path: Path,
        xml_library_path: Path,
        xml_library_url: str,
        http_timeout: int,
        ignored_books_path: Path,
        overriden_books_path: Path,
        meilisearch_url: str,
        meilisearch_prod_index: str,
        meilisearch_temp_index: str,
    ) -> None:
        self.favicons_path = favicons_path
        self.json_library_path = json_library_path
        self.xml_library_path = xml_library_path
        self.xml_library_url = xml_library_url
        self.library_changed = False
        self.library_last_digest: str | None = None
        self.http_timeout = http_timeout
        self.ignored_books_path = ignored_books_path
        self.overriden_books_path = overriden_books_path
        self.meilisearch_url = meilisearch_url
        self.meilisearch_prod_index = meilisearch_prod_index
        self.meilisearch_temp_index = meilisearch_temp_index

    def count_books(self):

        def count_fn(_, count):
            count[0] += 1

        count = [0]  # this is a hack to pass a mutable int
        self.iter_books(functools.partial(count_fn, count=count))
        logger.debug(f"{count[0]} books present in library")

    def extract_favicons(self):

        logger.debug("Extracting favicons")
        self.favicons_found = []
        self.nb_created = 0
        self.nb_total = 0
        self.nb_deleted = 0
        self.favicons_match = {}

        def extract_fn(book):
            favicon_bytes = base64.b64decode(book.attrib["favicon"])
            mime_type = book.attrib["faviconMimeType"]
            if mime_type != "image/png":
                raise ValueError(
                    f"Unexpected favicon mime type encountered: {mime_type}"
                )
            favicon_hash = hashlib.md5(favicon_bytes).hexdigest()  # noqa: S324
            self.favicons_match[book.attrib["id"]] = favicon_hash
            favicon_path = self.favicons_path / f"{favicon_hash}.png"
            if favicon_path not in self.favicons_found:
                self.favicons_found.append(favicon_path)
            if not favicon_path.exists():
                self.nb_created += 1
                favicon_path.write_bytes(favicon_bytes)

        self.favicons_path.mkdir(parents=True, exist_ok=True)
        self.iter_books(extract_fn)

        for file in self.favicons_path.glob("*.png"):
            self.nb_total += 1
            if file not in self.favicons_found:
                file.unlink()
                self.nb_deleted += 1

        logger.debug(f"{self.nb_created} favicons created")
        logger.debug(f"{self.nb_deleted} favicons deleted")
        logger.debug(f"{len(self.favicons_found)} favicons in memory")
        logger.debug(f"{self.nb_total} favicons on filesystem")

        del self.nb_created
        del self.nb_deleted
        del self.nb_total
        del self.favicons_found

    def process_books(self):

        logger.debug("Processing books to JSON/Search DB")
        self.books_processed = 0
        dictionary = {"items": {}}

        def create_fn(book):
            book_id = book.attrib["id"]

            name = book.attrib["name"]
            if name in self.books_to_ignore:
                self.books_really_ignored.add(name)
                return

            flavour = None
            if "flavour" in book.attrib:
                flavour = book.attrib["flavour"]

            category_tags = [
                tag
                for tag in book.attrib["tags"].split(";")
                if str(tag).startswith("_category:")
            ]
            if len(category_tags) > 1:
                logger.warning(
                    f"Book ignored - too many categories found for book {book_id}"
                )
                return
            if len(category_tags) == 0:
                category = "--"
            else:
                category = str(category_tags[0].split(":")[1])
            if category not in dictionary["items"].keys():
                dictionary["items"][category] = {"items": {}}

            if name in self.books_to_override:
                self.books_really_overriden.add(name)
                name = self.books_to_override[name]
            if category == "phet":
                parts = name.split("_")
                if parts[0] != "phets":
                    logger.warning(
                        "Book ignored - unexpected name - project - for phet book_id "
                        f"{book_id}: {name}"
                    )
                    return
                if len(parts) > 3:  # noqa: PLR2004
                    logger.warning(
                        "Book ignored - unexpected name length for phet book_id "
                        f"{book_id}: {name}"
                    )
                    return
                if len(parts) == 2:  # noqa: PLR2004
                    # Ignoring old stuff which has to be cleaned up
                    return
                project = parts[0]
                selection = parts[2]
                language = parts[1]
            elif category in (
                "other",
                "stack_exchange",
                "gutenberg",
                "ted",
                "wikihow",
                "wikibooks",
                "wikinews",
                "wikipedia",
                "wikiquote",
                "wikisource",
                "wikiversity",
                "wikivoyage",
                "wiktionary",
            ):
                parts = name.split("_")
                if len(parts) < 2 or len(parts) > 3:  # noqa: PLR2004
                    logger.warning(
                        "Book ignored - unexpected name length for book_id "
                        f"{book_id}: {name}"
                    )
                    return
                project = parts[0]
                language = parts[1]
                if len(language) > 3:  # noqa: PLR2004
                    logger.warning(
                        "Book ignored - unexpected name - lang - for book_id "
                        f"{book_id}: {name}"
                    )
                    return
                if len(parts) == 3:  # noqa: PLR2004
                    selection = parts[2]
                else:
                    selection = "all"
            elif category == "--":
                if name.startswith("avanti-"):
                    project = "avanti"
                    language = "hi"
                    selection = name[7:]
                elif name.startswith("maitre_lucas_"):
                    project = "maitre-lucas"
                    language = "fr"
                    selection = name[13:-3]
                elif name.startswith("canadian_prepper_"):
                    project = "canadian-prepper"
                    language = "en"
                    selection = name[17:-3]
                elif name.startswith("canadian_prepper_"):
                    project = "canadian-prepper"
                    language = "en"
                    selection = name[17:-3]
                else:
                    parts = name.split("_")
                    if len(parts) < 2 or len(parts) > 3:  # noqa: PLR2004
                        logger.warning(
                            "Book ignored - unexpected name length for book_id "
                            f"{book_id}: {name}"
                        )
                        return
                    project = parts[0]
                    language = parts[1]
                    if len(language) > 3:  # noqa: PLR2004
                        logger.warning(
                            "Book ignored - unexpected name - lang - for book_id "
                            f"{book_id}: {name}"
                        )
                        return
                    if len(parts) == 3:  # noqa: PLR2004
                        selection = parts[2]
                    else:
                        selection = "all"

            else:
                selection = "na"
                project = "na"
                language = "na"

            dictionary["items"][category]["items"][book_id] = {
                "selection": selection,
                "language": language,
                "project": project,
                "flavour": flavour,
            }

            def get_str_attrib_or_none(elem, key: str) -> str | None:
                return str(elem.attrib[key]) if key in elem.attrib else None

            def get_int_attrib_or_none(elem, key: str) -> int | None:
                return int(elem.attrib[key]) if key in elem.attrib else None

            # Create index which has been selected
            response = requests.post(
                urljoin(
                    self.meilisearch_url,
                    f"/indexes/{self.meilisearch_prepare_index}/documents",
                ),
                json={
                    "bookId": book_id,
                    "project": project,
                    "language": language,
                    "selection": selection,
                    "flavour": flavour,
                    "category": None if category == "--" else category,
                    "url": book.attrib["url"],
                    "size": get_int_attrib_or_none(book, "size"),
                    "mediaCount": get_int_attrib_or_none(book, "mediaCount"),
                    "articleCount": get_int_attrib_or_none(book, "articleCount"),
                    "title": get_str_attrib_or_none(book, "title"),
                    "description": get_str_attrib_or_none(book, "description"),
                    "creator": get_str_attrib_or_none(book, "creator"),
                    "publisher": get_str_attrib_or_none(book, "publisher"),
                    "tags": [
                        tag
                        for tag in (get_str_attrib_or_none(book, "tags") or "").split(
                            ";"
                        )
                        if not tag.startswith("_")
                    ],
                    "favicon": self.favicons_match[book_id],
                },
                timeout=self.http_timeout,
            )
            response.raise_for_status()

            self.books_processed += 1

        self.iter_books(create_fn)

        def count_items(a_dict):
            if "items" not in a_dict:
                return
            a_dict["count"] = len(a_dict["items"].keys())
            for value in a_dict["items"].values():
                count_items(value)

        count_items(dictionary)

        with open(self.json_library_path, "w") as fp:
            json.dump(dictionary, fp, indent=True)

        logger.debug(f"{self.books_processed} books processed")

    def iter_books(self, func):
        with open(self.xml_library_path, "rb") as f:
            context = ElementTree.iterparse(f, events=("start", "end"))
            for event, elem in context:
                if event == "start" and elem.tag == "book":
                    func(elem)
                    elem.clear()
        del context

    def download_library(self):
        logger.debug("Checking if XML library has changed")
        with requests.get(
            self.xml_library_url, stream=True, timeout=self.http_timeout
        ) as response:
            response.raise_for_status()
            etag = response.headers["ETag"]
            logger.debug(f"Library digest: {etag}")
            if self.library_last_digest and etag == self.library_last_digest:
                self.library_changed = False
                return
            self.library_last_digest = etag
            self.library_changed = True
            logger.debug("Downloading XML library")
            with open(self.xml_library_path, "wb") as fh:
                for chunk in response.iter_content(chunk_size=CHUNCK_DOWNLOAD_SIZE):
                    fh.write(chunk)

    def read_settings(self):

        self.books_to_override = {}
        self.books_really_overriden = set()

        with open(self.overriden_books_path) as fh:
            for line in fh:
                line_clean = line.strip()
                if line_clean.startswith("#") or len(line_clean) == 0:
                    continue
                items = line_clean.split("|")
                original = items[0].strip()
                override = items[1].strip()
                if original in self.books_to_override:
                    logger.warning(
                        f"{original} present twice in overriden books settings file"
                    )
                self.books_to_override[original] = override

        self.books_to_ignore = set()
        self.books_really_ignored = set()

        with open(self.ignored_books_path) as fh:
            for line in fh:
                line_clean = line.strip()
                if line_clean.startswith("#") or len(line_clean) == 0:
                    continue
                self.books_to_ignore.add(line_clean)

    def report_unused_settings(self):

        for book_not_ignored in self.books_to_ignore - self.books_really_ignored:
            logger.warning(
                f"Book {book_not_ignored} is set to be ignored but absent from the"
                "library"
            )

        for book_not_overiden in (
            set(self.books_to_override.keys()) - self.books_really_overriden
        ):
            logger.warning(
                f"Book {book_not_overiden} is set to be overriden but absent from the"
                "library"
            )

    def prepare_database(self):

        # Delete temp index if still here (could happen in case of previous failure)
        response = requests.get(
            urljoin(self.meilisearch_url, f"/indexes/{self.meilisearch_temp_index}"),
            timeout=self.http_timeout,
        )
        if response.status_code == HTTPStatus.OK:
            response = requests.delete(
                urljoin(
                    self.meilisearch_url, f"/indexes/{self.meilisearch_temp_index}"
                ),
                timeout=self.http_timeout,
            )
            response.raise_for_status()
        elif response.status_code != HTTPStatus.NOT_FOUND:
            response.raise_for_status()

        # Select which index to use: prod first time, temp every next ones
        response = requests.get(
            urljoin(self.meilisearch_url, f"/indexes/{self.meilisearch_prod_index}"),
            timeout=self.http_timeout,
        )
        if response.status_code == HTTPStatus.NOT_FOUND:
            self.meilisearch_prepare_index = self.meilisearch_prod_index
        else:
            response.raise_for_status()
            self.meilisearch_prepare_index = self.meilisearch_temp_index

        # Create index which has been selected
        response = requests.post(
            urljoin(self.meilisearch_url, "/indexes"),
            json={
                "uid": self.meilisearch_prepare_index,
                "primaryKey": "bookId",
            },
            timeout=self.http_timeout,
        )
        response.raise_for_status()

        # Configure index settings
        response = requests.put(
            urljoin(
                self.meilisearch_url,
                f"/indexes/{self.meilisearch_prepare_index}"
                "/settings/filterable-attributes",
            ),
            json=[
                "project",
                "language",
                "selection",
                "flavour",
                "category",
                "size",
                "mediaCount",
                "articleCount",
                "creator",
                "publisher",
                "tags",
            ],
            timeout=self.http_timeout,
        )
        response.raise_for_status()

    def finish_database(self):

        # If we worked directly on the prod index, nothing to do
        if self.meilisearch_prepare_index == self.meilisearch_prod_index:
            return

        # Let's swap prod and temp indexes
        response = requests.post(
            urljoin(self.meilisearch_url, "/swap-indexes"),
            json=[
                {
                    "indexes": [
                        self.meilisearch_prod_index,
                        self.meilisearch_temp_index,
                    ]
                }
            ],
            timeout=self.http_timeout,
        )
        response.raise_for_status()

        # Delete temp index (which was the prod few moments ago)
        response = requests.delete(
            urljoin(self.meilisearch_url, f"/indexes/{self.meilisearch_temp_index}"),
            timeout=self.http_timeout,
        )
        response.raise_for_status()

    def run(self):

        self.read_settings()

        self.prepare_database()

        self.download_library()

        if not self.library_changed:
            logger.debug("Library did not changed since last run, update finished")
            return

        self.count_books()

        self.extract_favicons()

        self.process_books()

        self.finish_database()

        self.report_unused_settings()

        logger.debug("Update DONE")
