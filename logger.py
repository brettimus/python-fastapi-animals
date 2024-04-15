import asyncio
from datetime import datetime, timezone
import logging
from opensearchpy import AsyncOpenSearch
import os

opensearch_host = os.environ.get("OPENSEARCH_HOST", "http://localhost:9200")
enable_opensearch_logging = os.environ.get("OPENSEARCH_LOGGING_ENABLED", "false") == "true"

# NOTE - This is not production code. We shouldn't spawn tasks like this from a log handler
class OpenSearchHandler(logging.Handler):
    def __init__(self, hosts, index):
        super().__init__()
        self.client = AsyncOpenSearch(hosts=hosts)
        self.index = index

    def emit(self, record):
        print("Emitting log")
        log_entry = self.format(record)
        timestamp_iso = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()

        document = {
            "message": log_entry,
            "logger": record.name,
            "level": record.levelname,
            "@timestamp": timestamp_iso,  # Use the ISO 8601 formatted timestamp, otherwise the timestamp is indexed as a float
        }
        # Schedule the coroutine to run on the event loop
        # This is somewhat straightforward for us because we assume
        # that we're running in an event loop (async web server)
        asyncio.ensure_future(self.async_emit(document))

    async def async_emit(self, document):
        try:
            await self.client.index(index=self.index, body=document)
        except Exception as e:
            print(f"Failed to send log to OpenSearch: {e}")


def get_logger(name="animalbuttons", log_file="animalbuttons.log", level=logging.INFO):
    file_handler = logging.FileHandler(log_file)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(file_handler)

    if enable_opensearch_logging:
        opensearch_handler = OpenSearchHandler([opensearch_host], "animalbuttons-logs-v3")
        opensearch_handler.setFormatter(formatter)
        logger.addHandler(opensearch_handler)

    return logger
