import yara
import logging
import sys

logger = logging.getLogger(__name__)

def load_yara_rules(filepath):
    try:
        return yara.compile(filepath=filepath)
    except yara.YaraSyntaxError as e:
        logger.error(f"Failed to compile YARA rules. Error: {e}")
        sys.exit(1)
