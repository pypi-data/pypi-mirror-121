import uuid

from logger.src.common.enums.platform import Platform

class Payload:
    def __init__(self, package, eventTime, message, tags, detail):
        self.eventId = str(uuid.uuid4())
        self.package = package
        self.platform = Platform.python
        self.eventTime = eventTime
        self.message = message
        self.tag = tags
        self.detail = detail
