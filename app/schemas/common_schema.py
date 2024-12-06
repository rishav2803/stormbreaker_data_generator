from enum import Enum


class DataSourceType(str, Enum):
    POSTGRES = "postgres"
    SNOWFLAKE = "snowflake"
    FILE = "file"
    TRINO = "trino"
    DATABRICKS = "databricks"
    MSSQL = "mssql"
    ORACLE = "oracle"
    MYSQL = "mysql"


class IOrderEnum(str, Enum):
    ascendent = "asc"
    descendent = "desc"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class SourceType(str, Enum):
    WEB = "web"
    SDK = "sdk"
    CLI = "cli"
    CI = "ci"
    API = "api"


class ProviderType(str, Enum):
    GOOGLE = "google"
    EMAIL = "email"
    MICROSOFT = "microsoft"


class UserRole(str, Enum):
    ADMIN = "admin"
    DEVELOPER = "developer"


class UserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class InvitationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"


class UserActivityType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"


class ProviderType(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    AZURE = "azure"


class TokenType(str, Enum):
    ACCESS = "access"
    INVITE = "invite"
    CHANGE_PASSWORD = "change_password"


class AutoStatus(str, Enum):
    IN_REVIEW = "in_review"
    REJECTED = "rejected"
    ENABLED = "enabled"


class ValidationCategory(str, Enum):
    RELIABILITY = "reliability"
    UNIQUENESS = "uniqueness"
    COMPLETENESS = "completeness"
    DISTRIBUTIONS = "distributions"
    CUSTOM = "custom"
    VALIDITY = "validity"


class AlertStatus(str, Enum):
    NO_STATUS = "no_status"
    FIXED = "fixed"
    INVESTIGATING = "investigating"
    EXPECTED = "expected"
    NO_ACTION_NEEDED = "no_action_needed"
    FALSE_POSITIVE = "false_positive"


class Severity(str, Enum):
    CRITICAL = "critical"
    MEDIUM = "medium"
    MINOR = "minor"
