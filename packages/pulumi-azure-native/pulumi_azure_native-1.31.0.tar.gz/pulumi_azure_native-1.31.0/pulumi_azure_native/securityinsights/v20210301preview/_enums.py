# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AlertDetail',
    'AlertRuleKind',
    'AlertSeverity',
    'AttackTactic',
    'ConnectivityType',
    'ContentType',
    'CustomEntityQueryKind',
    'DataConnectorKind',
    'DataTypeState',
    'EntityMappingType',
    'EntityType',
    'EventGroupingAggregationKind',
    'IncidentClassification',
    'IncidentClassificationReason',
    'IncidentSeverity',
    'IncidentStatus',
    'Kind',
    'MatchingMethod',
    'MicrosoftSecurityProductName',
    'Operator',
    'PermissionProviderScope',
    'PollingFrequency',
    'ProviderName',
    'RepoType',
    'SettingKind',
    'SettingType',
    'Source',
    'SourceKind',
    'SupportTier',
    'TriggerOperator',
    'UebaDataSources',
]


class AlertDetail(str, Enum):
    """
    Alert detail
    """
    DISPLAY_NAME = "DisplayName"
    """Alert display name"""
    SEVERITY = "Severity"
    """Alert severity"""


class AlertRuleKind(str, Enum):
    """
    The kind of the alert rule
    """
    SCHEDULED = "Scheduled"
    MICROSOFT_SECURITY_INCIDENT_CREATION = "MicrosoftSecurityIncidentCreation"
    FUSION = "Fusion"
    ML_BEHAVIOR_ANALYTICS = "MLBehaviorAnalytics"
    THREAT_INTELLIGENCE = "ThreatIntelligence"


class AlertSeverity(str, Enum):
    """
    The severity for alerts created by this alert rule.
    """
    HIGH = "High"
    """High severity"""
    MEDIUM = "Medium"
    """Medium severity"""
    LOW = "Low"
    """Low severity"""
    INFORMATIONAL = "Informational"
    """Informational severity"""


class AttackTactic(str, Enum):
    """
    The severity for alerts created by this alert rule.
    """
    INITIAL_ACCESS = "InitialAccess"
    EXECUTION = "Execution"
    PERSISTENCE = "Persistence"
    PRIVILEGE_ESCALATION = "PrivilegeEscalation"
    DEFENSE_EVASION = "DefenseEvasion"
    CREDENTIAL_ACCESS = "CredentialAccess"
    DISCOVERY = "Discovery"
    LATERAL_MOVEMENT = "LateralMovement"
    COLLECTION = "Collection"
    EXFILTRATION = "Exfiltration"
    COMMAND_AND_CONTROL = "CommandAndControl"
    IMPACT = "Impact"
    PRE_ATTACK = "PreAttack"


class ConnectivityType(str, Enum):
    """
    type of connectivity
    """
    IS_CONNECTED_QUERY = "IsConnectedQuery"


class ContentType(str, Enum):
    """
    Content type.
    """
    ANALYTIC_RULE = "AnalyticRule"
    WORKBOOK = "Workbook"


class CustomEntityQueryKind(str, Enum):
    """
    the entity query kind
    """
    ACTIVITY = "Activity"


class DataConnectorKind(str, Enum):
    """
    The data connector kind
    """
    AZURE_ACTIVE_DIRECTORY = "AzureActiveDirectory"
    AZURE_SECURITY_CENTER = "AzureSecurityCenter"
    MICROSOFT_CLOUD_APP_SECURITY = "MicrosoftCloudAppSecurity"
    THREAT_INTELLIGENCE = "ThreatIntelligence"
    THREAT_INTELLIGENCE_TAXII = "ThreatIntelligenceTaxii"
    OFFICE365 = "Office365"
    OFFICE_ATP = "OfficeATP"
    AMAZON_WEB_SERVICES_CLOUD_TRAIL = "AmazonWebServicesCloudTrail"
    AZURE_ADVANCED_THREAT_PROTECTION = "AzureAdvancedThreatProtection"
    MICROSOFT_DEFENDER_ADVANCED_THREAT_PROTECTION = "MicrosoftDefenderAdvancedThreatProtection"
    DYNAMICS365 = "Dynamics365"
    MICROSOFT_THREAT_PROTECTION = "MicrosoftThreatProtection"
    MICROSOFT_THREAT_INTELLIGENCE = "MicrosoftThreatIntelligence"
    GENERIC_UI = "GenericUI"


class DataTypeState(str, Enum):
    """
    Describe whether this data type connection is enabled or not.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class EntityMappingType(str, Enum):
    """
    The V3 type of the mapped entity
    """
    ACCOUNT = "Account"
    """User account entity type"""
    HOST = "Host"
    """Host entity type"""
    IP = "IP"
    """IP address entity type"""
    MALWARE = "Malware"
    """Malware entity type"""
    FILE = "File"
    """System file entity type"""
    PROCESS = "Process"
    """Process entity type"""
    CLOUD_APPLICATION = "CloudApplication"
    """Cloud app entity type"""
    DNS = "DNS"
    """DNS entity type"""
    AZURE_RESOURCE = "AzureResource"
    """Azure resource entity type"""
    FILE_HASH = "FileHash"
    """File-hash entity type"""
    REGISTRY_KEY = "RegistryKey"
    """Registry key entity type"""
    REGISTRY_VALUE = "RegistryValue"
    """Registry value entity type"""
    SECURITY_GROUP = "SecurityGroup"
    """Security group entity type"""
    URL = "URL"
    """URL entity type"""
    MAILBOX = "Mailbox"
    """Mailbox entity type"""
    MAIL_CLUSTER = "MailCluster"
    """Mail cluster entity type"""
    MAIL_MESSAGE = "MailMessage"
    """Mail message entity type"""
    SUBMISSION_MAIL = "SubmissionMail"
    """Submission mail entity type"""


class EntityType(str, Enum):
    """
    The type of the query's source entity
    """
    ACCOUNT = "Account"
    """Entity represents account in the system."""
    HOST = "Host"
    """Entity represents host in the system."""
    FILE = "File"
    """Entity represents file in the system."""
    AZURE_RESOURCE = "AzureResource"
    """Entity represents azure resource in the system."""
    CLOUD_APPLICATION = "CloudApplication"
    """Entity represents cloud application in the system."""
    DNS = "DNS"
    """Entity represents dns in the system."""
    FILE_HASH = "FileHash"
    """Entity represents file hash in the system."""
    IP = "IP"
    """Entity represents ip in the system."""
    MALWARE = "Malware"
    """Entity represents malware in the system."""
    PROCESS = "Process"
    """Entity represents process in the system."""
    REGISTRY_KEY = "RegistryKey"
    """Entity represents registry key in the system."""
    REGISTRY_VALUE = "RegistryValue"
    """Entity represents registry value in the system."""
    SECURITY_GROUP = "SecurityGroup"
    """Entity represents security group in the system."""
    URL = "URL"
    """Entity represents url in the system."""
    IO_T_DEVICE = "IoTDevice"
    """Entity represents IoT device in the system."""
    SECURITY_ALERT = "SecurityAlert"
    """Entity represents security alert in the system."""
    HUNTING_BOOKMARK = "HuntingBookmark"
    """Entity represents HuntingBookmark in the system."""
    MAIL_CLUSTER = "MailCluster"
    """Entity represents mail cluster in the system."""
    MAIL_MESSAGE = "MailMessage"
    """Entity represents mail message in the system."""
    MAILBOX = "Mailbox"
    """Entity represents mailbox in the system."""
    SUBMISSION_MAIL = "SubmissionMail"
    """Entity represents submission mail in the system."""


class EventGroupingAggregationKind(str, Enum):
    """
    The event grouping aggregation kinds
    """
    SINGLE_ALERT = "SingleAlert"
    ALERT_PER_RESULT = "AlertPerResult"


class IncidentClassification(str, Enum):
    """
    The reason the incident was closed
    """
    UNDETERMINED = "Undetermined"
    """Incident classification was undetermined"""
    TRUE_POSITIVE = "TruePositive"
    """Incident was true positive"""
    BENIGN_POSITIVE = "BenignPositive"
    """Incident was benign positive"""
    FALSE_POSITIVE = "FalsePositive"
    """Incident was false positive"""


class IncidentClassificationReason(str, Enum):
    """
    The classification reason the incident was closed with
    """
    SUSPICIOUS_ACTIVITY = "SuspiciousActivity"
    """Classification reason was suspicious activity"""
    SUSPICIOUS_BUT_EXPECTED = "SuspiciousButExpected"
    """Classification reason was suspicious but expected"""
    INCORRECT_ALERT_LOGIC = "IncorrectAlertLogic"
    """Classification reason was incorrect alert logic"""
    INACCURATE_DATA = "InaccurateData"
    """Classification reason was inaccurate data"""


class IncidentSeverity(str, Enum):
    """
    The severity of the incident
    """
    HIGH = "High"
    """High severity"""
    MEDIUM = "Medium"
    """Medium severity"""
    LOW = "Low"
    """Low severity"""
    INFORMATIONAL = "Informational"
    """Informational severity"""


class IncidentStatus(str, Enum):
    """
    The status of the incident
    """
    NEW = "New"
    """An active incident which isn't being handled currently"""
    ACTIVE = "Active"
    """An active incident which is being handled"""
    CLOSED = "Closed"
    """A non-active incident"""


class Kind(str, Enum):
    """
    The kind of content the metadata is for.
    """
    DATA_CONNECTOR = "DataConnector"
    DATA_TYPE = "DataType"
    WORKBOOK = "Workbook"
    WORKBOOK_TEMPLATE = "WorkbookTemplate"
    PLAYBOOK = "Playbook"
    PLAYBOOK_TEMPLATE = "PlaybookTemplate"
    ANALYTICS_RULE_TEMPLATE = "AnalyticsRuleTemplate"
    ANALYTICS_RULE = "AnalyticsRule"
    HUNTING_QUERY = "HuntingQuery"
    INVESTIGATION_QUERY = "InvestigationQuery"
    PARSER = "Parser"
    WATCHLIST = "Watchlist"
    WATCHLIST_TEMPLATE = "WatchlistTemplate"
    SOLUTION = "Solution"


class MatchingMethod(str, Enum):
    """
    Grouping matching method. When method is Selected at least one of groupByEntities, groupByAlertDetails, groupByCustomDetails must be provided and not empty.
    """
    ALL_ENTITIES = "AllEntities"
    """Grouping alerts into a single incident if all the entities match"""
    ANY_ALERT = "AnyAlert"
    """Grouping any alerts triggered by this rule into a single incident"""
    SELECTED = "Selected"
    """Grouping alerts into a single incident if the selected entities, custom details and alert details match"""


class MicrosoftSecurityProductName(str, Enum):
    """
    The alerts' productName on which the cases will be generated
    """
    MICROSOFT_CLOUD_APP_SECURITY = "Microsoft Cloud App Security"
    AZURE_SECURITY_CENTER = "Azure Security Center"
    AZURE_ADVANCED_THREAT_PROTECTION = "Azure Advanced Threat Protection"
    AZURE_ACTIVE_DIRECTORY_IDENTITY_PROTECTION = "Azure Active Directory Identity Protection"
    AZURE_SECURITY_CENTER_FOR_IO_T = "Azure Security Center for IoT"
    OFFICE_365_ADVANCED_THREAT_PROTECTION = "Office 365 Advanced Threat Protection"
    MICROSOFT_DEFENDER_ADVANCED_THREAT_PROTECTION = "Microsoft Defender Advanced Threat Protection"


class Operator(str, Enum):
    """
    Operator used for list of dependencies in criteria array.
    """
    AND_ = "AND"
    OR_ = "OR"


class PermissionProviderScope(str, Enum):
    """
    Permission provider scope
    """
    RESOURCE_GROUP = "ResourceGroup"
    SUBSCRIPTION = "Subscription"
    WORKSPACE = "Workspace"


class PollingFrequency(str, Enum):
    """
    The polling frequency for the TAXII server.
    """
    ONCE_A_MINUTE = "OnceAMinute"
    """Once a minute"""
    ONCE_AN_HOUR = "OnceAnHour"
    """Once an hour"""
    ONCE_A_DAY = "OnceADay"
    """Once a day"""


class ProviderName(str, Enum):
    """
    Provider name
    """
    MICROSOFT_OPERATIONAL_INSIGHTS_SOLUTIONS = "Microsoft.OperationalInsights/solutions"
    MICROSOFT_OPERATIONAL_INSIGHTS_WORKSPACES = "Microsoft.OperationalInsights/workspaces"
    MICROSOFT_OPERATIONAL_INSIGHTS_WORKSPACES_DATASOURCES = "Microsoft.OperationalInsights/workspaces/datasources"
    MICROSOFT_AADIAM_DIAGNOSTIC_SETTINGS = "microsoft.aadiam/diagnosticSettings"
    MICROSOFT_OPERATIONAL_INSIGHTS_WORKSPACES_SHARED_KEYS = "Microsoft.OperationalInsights/workspaces/sharedKeys"
    MICROSOFT_AUTHORIZATION_POLICY_ASSIGNMENTS = "Microsoft.Authorization/policyAssignments"


class RepoType(str, Enum):
    """
    The repository type of the source control
    """
    GITHUB = "Github"
    DEV_OPS = "DevOps"


class SettingKind(str, Enum):
    """
    The kind of the setting
    """
    ANOMALIES = "Anomalies"
    EYES_ON = "EyesOn"
    ENTITY_ANALYTICS = "EntityAnalytics"
    UEBA = "Ueba"


class SettingType(str, Enum):
    """
    The kind of the setting
    """
    COPYABLE_LABEL = "CopyableLabel"
    INSTRUCTION_STEPS_GROUP = "InstructionStepsGroup"
    INFO_MESSAGE = "InfoMessage"


class Source(str, Enum):
    """
    The source of the watchlist
    """
    LOCAL_FILE = "Local file"
    REMOTE_STORAGE = "Remote storage"


class SourceKind(str, Enum):
    """
    Source type of the content
    """
    LOCAL_WORKSPACE = "LocalWorkspace"
    COMMUNITY = "Community"
    SOLUTION = "Solution"
    SOURCE_REPOSITORY = "SourceRepository"


class SupportTier(str, Enum):
    """
    Type of support for content item
    """
    MICROSOFT = "Microsoft"
    PARTNER = "Partner"
    COMMUNITY = "Community"


class TriggerOperator(str, Enum):
    """
    The operation against the threshold that triggers alert rule.
    """
    GREATER_THAN = "GreaterThan"
    LESS_THAN = "LessThan"
    EQUAL = "Equal"
    NOT_EQUAL = "NotEqual"


class UebaDataSources(str, Enum):
    """
    The data source that enriched by ueba.
    """
    AUDIT_LOGS = "AuditLogs"
    AZURE_ACTIVITY = "AzureActivity"
    SECURITY_EVENT = "SecurityEvent"
    SIGNIN_LOGS = "SigninLogs"
