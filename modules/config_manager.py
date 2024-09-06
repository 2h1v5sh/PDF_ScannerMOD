import configparser
import logging
import os
import sys

logger = logging.getLogger(__name__)

def load_config(config_file=None):
    config = configparser.ConfigParser()
    config_path = config_file or os.getenv('PDF_SCANNER_CONFIG', 'config.ini')

    try:
        config.read(config_path)
        logger.info(f"Configuration loaded from {config_path}")
    except Exception as e:
        logger.error(f"Failed to read config file {config_path}. Error: {e}")
        sys.exit(1)
    
    return config
