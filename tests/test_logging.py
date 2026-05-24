import logging

from openapi_parser.logging import log_ctx


def test_log_context_prefix() -> None:
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    records: list[logging.LogRecord] = []

    class RecordHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            record.msg = self.format(record)
            records.append(record)

    record_handler = RecordHandler()
    logger.addHandler(record_handler)
    logger.setLevel(logging.DEBUG)

    with log_ctx("test", "path"):
        logger.debug("hello")

    logger.removeHandler(record_handler)

    assert len(records) == 1
    assert records[0].msg == "[test.path] hello"
