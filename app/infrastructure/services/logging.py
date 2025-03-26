import logging

from app.config import settings

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(filename)s | %(message)s",
    level=settings.LOG_LEVEL,
)

logger = logging.getLogger(__name__)
