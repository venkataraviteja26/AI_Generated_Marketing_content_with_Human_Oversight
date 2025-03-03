import logging

def setup_logging(log_level="INFO"):
    """
    Configures the logging module with the provided log level.
    Logs will include the timestamp, logger name, level, and message.
    log levels could be DEBUG, INFO, ERROR, CRITICAL, WARNING
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.getLogger().info(f"Logging is set to {log_level}")
