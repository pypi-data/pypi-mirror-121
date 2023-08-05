# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AutoHealActionType',
    'AzureResourceType',
    'AzureStorageType',
    'BuiltInAuthenticationProvider',
    'ConnectionStringType',
    'CustomHostNameDnsRecordType',
    'DatabaseType',
    'FrequencyUnit',
    'FtpsState',
    'HostNameType',
    'HostType',
    'IpFilterTag',
    'LogLevel',
    'ManagedPipelineMode',
    'ManagedServiceIdentityType',
    'PublicCertificateLocation',
    'RedundancyMode',
    'ScmType',
    'SiteLoadBalancing',
    'SslState',
    'SupportedTlsVersions',
    'UnauthenticatedClientAction',
]


class AutoHealActionType(str, Enum):
    """
    Predefined action to be taken.
    """
    RECYCLE = "Recycle"
    LOG_EVENT = "LogEvent"
    CUSTOM_ACTION = "CustomAction"


class AzureResourceType(str, Enum):
    """
    Azure resource type.
    """
    WEBSITE = "Website"
    TRAFFIC_MANAGER = "TrafficManager"


class AzureStorageType(str, Enum):
    """
    Type of storage.
    """
    AZURE_FILES = "AzureFiles"
    AZURE_BLOB = "AzureBlob"


class BuiltInAuthenticationProvider(str, Enum):
    """
    The default authentication provider to use when multiple providers are configured.
    This setting is only needed if multiple providers are configured and the unauthenticated client
    action is set to "RedirectToLoginPage".
    """
    AZURE_ACTIVE_DIRECTORY = "AzureActiveDirectory"
    FACEBOOK = "Facebook"
    GOOGLE = "Google"
    MICROSOFT_ACCOUNT = "MicrosoftAccount"
    TWITTER = "Twitter"


class ConnectionStringType(str, Enum):
    """
    Type of database.
    """
    MY_SQL = "MySql"
    SQL_SERVER = "SQLServer"
    SQL_AZURE = "SQLAzure"
    CUSTOM = "Custom"
    NOTIFICATION_HUB = "NotificationHub"
    SERVICE_BUS = "ServiceBus"
    EVENT_HUB = "EventHub"
    API_HUB = "ApiHub"
    DOC_DB = "DocDb"
    REDIS_CACHE = "RedisCache"
    POSTGRE_SQL = "PostgreSQL"


class CustomHostNameDnsRecordType(str, Enum):
    """
    Custom DNS record type.
    """
    C_NAME = "CName"
    A = "A"


class DatabaseType(str, Enum):
    """
    Database type (e.g. SqlAzure / MySql).
    """
    SQL_AZURE = "SqlAzure"
    MY_SQL = "MySql"
    LOCAL_MY_SQL = "LocalMySql"
    POSTGRE_SQL = "PostgreSql"


class FrequencyUnit(str, Enum):
    """
    The unit of time for how often the backup should be executed (e.g. for weekly backup, this should be set to Day and FrequencyInterval should be set to 7)
    """
    DAY = "Day"
    HOUR = "Hour"


class FtpsState(str, Enum):
    """
    State of FTP / FTPS service
    """
    ALL_ALLOWED = "AllAllowed"
    FTPS_ONLY = "FtpsOnly"
    DISABLED = "Disabled"


class HostNameType(str, Enum):
    """
    Hostname type.
    """
    VERIFIED = "Verified"
    MANAGED = "Managed"


class HostType(str, Enum):
    """
    Indicates whether the hostname is a standard or repository hostname.
    """
    STANDARD = "Standard"
    REPOSITORY = "Repository"


class IpFilterTag(str, Enum):
    """
    Defines what this IP filter will be used for. This is to support IP filtering on proxies.
    """
    DEFAULT = "Default"
    XFF_PROXY = "XffProxy"


class LogLevel(str, Enum):
    """
    Log level.
    """
    OFF = "Off"
    VERBOSE = "Verbose"
    INFORMATION = "Information"
    WARNING = "Warning"
    ERROR = "Error"


class ManagedPipelineMode(str, Enum):
    """
    Managed pipeline mode.
    """
    INTEGRATED = "Integrated"
    CLASSIC = "Classic"


class ManagedServiceIdentityType(str, Enum):
    """
    Type of managed service identity.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"
    NONE = "None"


class PublicCertificateLocation(str, Enum):
    """
    Public Certificate Location
    """
    CURRENT_USER_MY = "CurrentUserMy"
    LOCAL_MACHINE_MY = "LocalMachineMy"
    UNKNOWN = "Unknown"


class RedundancyMode(str, Enum):
    """
    Site redundancy mode
    """
    NONE = "None"
    MANUAL = "Manual"
    FAILOVER = "Failover"
    ACTIVE_ACTIVE = "ActiveActive"
    GEO_REDUNDANT = "GeoRedundant"


class ScmType(str, Enum):
    """
    SCM type.
    """
    NONE = "None"
    DROPBOX = "Dropbox"
    TFS = "Tfs"
    LOCAL_GIT = "LocalGit"
    GIT_HUB = "GitHub"
    CODE_PLEX_GIT = "CodePlexGit"
    CODE_PLEX_HG = "CodePlexHg"
    BITBUCKET_GIT = "BitbucketGit"
    BITBUCKET_HG = "BitbucketHg"
    EXTERNAL_GIT = "ExternalGit"
    EXTERNAL_HG = "ExternalHg"
    ONE_DRIVE = "OneDrive"
    VSO = "VSO"


class SiteLoadBalancing(str, Enum):
    """
    Site load balancing.
    """
    WEIGHTED_ROUND_ROBIN = "WeightedRoundRobin"
    LEAST_REQUESTS = "LeastRequests"
    LEAST_RESPONSE_TIME = "LeastResponseTime"
    WEIGHTED_TOTAL_TRAFFIC = "WeightedTotalTraffic"
    REQUEST_HASH = "RequestHash"


class SslState(str, Enum):
    """
    SSL type.
    """
    DISABLED = "Disabled"
    SNI_ENABLED = "SniEnabled"
    IP_BASED_ENABLED = "IpBasedEnabled"


class SupportedTlsVersions(str, Enum):
    """
    MinTlsVersion: configures the minimum version of TLS required for SSL requests
    """
    SUPPORTED_TLS_VERSIONS_1_0 = "1.0"
    SUPPORTED_TLS_VERSIONS_1_1 = "1.1"
    SUPPORTED_TLS_VERSIONS_1_2 = "1.2"


class UnauthenticatedClientAction(str, Enum):
    """
    The action to take when an unauthenticated client attempts to access the app.
    """
    REDIRECT_TO_LOGIN_PAGE = "RedirectToLoginPage"
    ALLOW_ANONYMOUS = "AllowAnonymous"
