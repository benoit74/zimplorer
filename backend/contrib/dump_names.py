import logging
from pathlib import Path

import requests
from defusedxml import ElementTree

logger = logging.Logger("dump_names", logging.DEBUG)
HTTP_TIMEOUT = 10
LIBRARY_URL = "https://download.kiwix.org/library/library_zim.xml"
LIBRARY_PATH = Path("library_zim.xml")
CHUNCK_DOWNLOAD_SIZE = 8192


def download_library():
    logger.debug("Downloading XML library")
    with requests.get(
        LIBRARY_URL,
        stream=True,
        timeout=HTTP_TIMEOUT,
    ) as response:
        response.raise_for_status()
        with open(LIBRARY_PATH, "wb") as fh:
            for chunk in response.iter_content(chunk_size=CHUNCK_DOWNLOAD_SIZE):
                fh.write(chunk)


def iter_books(func):
    with open(LIBRARY_PATH, "rb") as f:
        context = ElementTree.iterparse(f, events=("start", "end"))
        for event, elem in context:
            if event == "start" and elem.tag == "book":
                func(elem)
                elem.clear()
    del context


def dump_names():
    def create_fn(book):
        name = book.attrib["name"]
        url = book.attrib["url"]
        flavour = book.attrib["flavour"] if "flavour" in book.attrib else ""
        title = book.attrib["title"]
        description = book.attrib["description"] if "description" in book.attrib else ""
        filename = url.split("/")[-1][:-6]
        print(f"{name}##{filename}##{flavour}##{title}##{description}")  # noqa: T201

    iter_books(create_fn)


# download_library()
dump_names()
