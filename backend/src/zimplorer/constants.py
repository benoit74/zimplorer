import os
import pathlib

from zimplorer.logging import get_logger

src_dir = pathlib.Path(__file__).parent.resolve()

logger = get_logger(
    "offspot_metrics",
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
