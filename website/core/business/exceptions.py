from enum import Enum


class TypeException(Enum):
    """AWS type exception."""

    REDIRECTION = "PermanentRedirect"
    ILLEGAL_LOCATION = "IllegalLocationConstraintException"


class PermissionException(Enum):
    """AWS permission exception."""

    ACCESS_DENIED = "AccessDenied"
    NO_SUCH_BUCKET = "NoSuchBucket"
    LIST_BUCKET_RESULT = "ListBucketResult"
