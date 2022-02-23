import logging

logger = logging.getLogger()
logger.setLevel("INFO")


def handler(event: dict, context):
    """
    The handler for enrichment process.

    Args:
        event (dict): contains the data received from its data source.
        context: contains the lambda invocation context.
    """
    logger.info(f"event - {event}")
    raise ValueError("Invalid message sent")
