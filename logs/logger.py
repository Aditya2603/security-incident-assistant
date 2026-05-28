import logging

logging.basicConfig(
    filename="logs/incidents.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)