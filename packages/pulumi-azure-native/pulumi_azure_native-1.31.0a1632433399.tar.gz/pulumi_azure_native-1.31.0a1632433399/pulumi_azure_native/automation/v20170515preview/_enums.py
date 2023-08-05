# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'LinuxUpdateClasses',
    'OperatingSystemType',
    'ScheduleDay',
    'ScheduleFrequency',
    'SourceType',
    'TagOperators',
    'TokenType',
    'WindowsUpdateClasses',
]


class LinuxUpdateClasses(str, Enum):
    """
    Update classifications included in the software update configuration.
    """
    UNCLASSIFIED = "Unclassified"
    CRITICAL = "Critical"
    SECURITY = "Security"
    OTHER = "Other"


class OperatingSystemType(str, Enum):
    """
    operating system of target machines
    """
    WINDOWS = "Windows"
    LINUX = "Linux"


class ScheduleDay(str, Enum):
    """
    Day of the occurrence. Must be one of monday, tuesday, wednesday, thursday, friday, saturday, sunday.
    """
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class ScheduleFrequency(str, Enum):
    """
    Gets or sets the frequency of the schedule.
    """
    ONE_TIME = "OneTime"
    DAY = "Day"
    HOUR = "Hour"
    WEEK = "Week"
    MONTH = "Month"
    MINUTE = "Minute"
    """The minimum allowed interval for Minute schedules is 15 minutes."""


class SourceType(str, Enum):
    """
    The source type. Must be one of VsoGit, VsoTfvc, GitHub, case sensitive.
    """
    VSO_GIT = "VsoGit"
    VSO_TFVC = "VsoTfvc"
    GIT_HUB = "GitHub"


class TagOperators(str, Enum):
    """
    Filter VMs by Any or All specified tags.
    """
    ALL = "All"
    ANY = "Any"


class TokenType(str, Enum):
    """
    The token type. Must be either PersonalAccessToken or Oauth.
    """
    PERSONAL_ACCESS_TOKEN = "PersonalAccessToken"
    OAUTH = "Oauth"


class WindowsUpdateClasses(str, Enum):
    """
    Update classification included in the software update configuration. A comma separated string with required values
    """
    UNCLASSIFIED = "Unclassified"
    CRITICAL = "Critical"
    SECURITY = "Security"
    UPDATE_ROLLUP = "UpdateRollup"
    FEATURE_PACK = "FeaturePack"
    SERVICE_PACK = "ServicePack"
    DEFINITION = "Definition"
    TOOLS = "Tools"
    UPDATES = "Updates"
