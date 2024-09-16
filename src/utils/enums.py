from enum import Enum

class ScheduleStatus(Enum):
    PENDING = "Pending"
    SENT = "Sent"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

    @classmethod
    def list(cls):
        return [status.value for status in cls]
        # return list(map(lambda c: c.value, cls))
