import logging
from elasticsearch import AsyncElasticsearch
import os

# Get the environment variable 'MY_VAR'. If it's not set, default to 'default_value'.
opensearch_host = os.environ.get("OPENSEARCH_HOST", "http://localhost:9200")

class OpenSearchHandler(logging.Handler):
    def __init__(self, es_hosts, index):
        super().__init__()
        self.es = AsyncElasticsearch(hosts=es_hosts)
        self.index = index

    async def emit(self, record):
        log_entry = self.format(record)
        # Transform log_entry into the structure OpenSearch expects
        # Remember to catch exceptions and handle retries/failed sends
        await self.es.index(
            index=self.index,
            document={
                "message": log_entry,
                "logger": record.name,
                "level": record.levelname,
                "timestamp": record.created,
            },
        )


def get_logger(name="animalbuttons", log_file="animalbuttons.log", level=logging.INFO):
    file_handler = logging.FileHandler(log_file)
    opensearch_handler = OpenSearchHandler([opensearch_host], "animalbuttons-logs")

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    opensearch_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(opensearch_handler)

    return logger
