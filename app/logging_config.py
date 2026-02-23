import logging
import logging.config
import sys

LOG_FILE_NAME = "logs/app.log"


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        record.method = getattr(record, "method", "-")
        record.path = getattr(record, "path", "-")
        record.status_code = getattr(record, "status_code", "-")
        record.duration = getattr(record, "duration", "-")
        return True


def setup_logging(level: str = "DEBUG"):
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": (
                    "%(asctime)s | %(levelname)s | %(name)s | "
                    "method=%(method)s path=%(path)s "
                    "status=%(status_code)s duration_ms=%(duration)s | "
                    "%(message)s"
                )
            }
        },
        "filters": {
            "request_context": {
                "()": RequestContextFilter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
                "filters": ["request_context"],
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": LOG_FILE_NAME,
                "maxBytes": 10_00_000,
                "backupCount": 5,
                "encoding": "utf-8",
                "filters": ["request_context"],
            },
        },
        "root": {"handlers": ["console", "file"], "level": level},
    }
    logging.config.dictConfig(config=logging_config)
