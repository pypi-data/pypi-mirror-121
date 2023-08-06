import json


class PayloadDetail:
    def __init__(
            self,
            logLevel,
            location,
            logger,
            nodestoreInsert,
            received,
            timestamp,
            title,
            type,
            version,
            metadata,
            sdk,
            user):
        self.level = logLevel
        self.location = location
        self.logger = logger
        self.nodestoreInsert = nodestoreInsert
        self.received = received
        self.timestamp = timestamp
        self.title = title
        self.type = type
        self.version = version
        self.metadata = metadata
        self.sdk = sdk
        self.user = user

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
