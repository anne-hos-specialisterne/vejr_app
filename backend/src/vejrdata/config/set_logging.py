import logging
import sys

def setup_logger(name=None, level=logging.INFO):
    """
    Configure logger for Docker-friendly output.
    Logs go to stdout and optionally can be extended to files.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # prevent duplicate logs

    # Check if handlers already exist (avoid duplicate logs)
    if not logger.handlers:
        # Stream handler (stdout)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level)

        # Optional: file handler
        file_handler = logging.FileHandler("backend/logs/app.log")
        file_handler.setLevel(level)

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger