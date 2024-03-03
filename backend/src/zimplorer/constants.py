import os
import pathlib

from zimplorer.logging import get_logger

src_dir = pathlib.Path(__file__).parent.resolve()

logger = get_logger(
    "zimplorer",
    level=os.getenv(
        "LOG_LEVEL",
        "INFO",
    ),
)


class BackendConf:
    """Shared backend configuration"""

    allowed_origins: list[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost|http://localhost:8000|http://localhost:8080",  # dev fallback
    ).split("|")

    # Boolean stoping background processing of new library content
    # Useful mostly for local development purpose when we do not want to refresh the
    # indexes regularly to work on stable datasets
    # The environment variable must hence be explicitely set to True (case-insensitive)
    # all other values will enable the processing.
    processing_enabled = os.getenv("PROCESSING_DISABLED", "False").lower() != "true"

    ui_location = pathlib.Path(os.getenv("UI_LOCATION", "/src/ui"))

    updater_period_seconds = int(os.getenv("UPDATER_PERIOD_SECONDS", "60"))

    favicons_path = pathlib.Path(os.getenv("FAVICONS_LOCATION", "/data/favicons"))

    json_library_path = pathlib.Path(
        os.getenv("JSON_LIBRARY_LOCATION", "/data/library.json")
    )

    xml_library_path = pathlib.Path(
        os.getenv("XML_LIBRARY_LOCATION", "/data/library.xml")
    )

    xml_library_url = os.getenv(
        "XML_LIBRARY_URL", "https://download.kiwix.org/library/library_zim.xml"
    )

    http_timeout = int(os.getenv("HTTP_TIMEOUT", "60"))

    ignored_books_path = pathlib.Path(
        os.getenv("IGNORED_BOOKS_LOCATION", "/data/settings/books_ignored.txt")
    )

    overriden_books_path = pathlib.Path(
        os.getenv("OVERRIDEN_BOOKS_LOCATION", "/data/settings/books_name_overrides.txt")
    )
