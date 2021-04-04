from enum import Enum


class SessionState(Enum):
    ENQUEUED = "ENQUEUED"
    ACCEPTED = "ACCEPTED"
    CLOSED = "CLOSED"
