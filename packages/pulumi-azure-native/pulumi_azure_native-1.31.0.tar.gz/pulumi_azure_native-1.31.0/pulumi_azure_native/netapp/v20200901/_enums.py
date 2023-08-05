# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'EndpointType',
    'QosType',
    'ReplicationSchedule',
    'SecurityStyle',
    'ServiceLevel',
]


class EndpointType(str, Enum):
    """
    Indicates whether the local volume is the source or destination for the Volume Replication
    """
    SRC = "src"
    DST = "dst"


class QosType(str, Enum):
    """
    The qos type of the pool
    """
    AUTO = "Auto"
    """qos type Auto"""
    MANUAL = "Manual"
    """qos type Manual"""


class ReplicationSchedule(str, Enum):
    """
    Schedule
    """
    REPLICATION_SCHEDULE_10MINUTELY = "_10minutely"
    HOURLY = "hourly"
    DAILY = "daily"


class SecurityStyle(str, Enum):
    """
    The security style of volume, default unix, ntfs for dual protocol or CIFS protocol
    """
    NTFS = "ntfs"
    UNIX = "unix"


class ServiceLevel(str, Enum):
    """
    The service level of the file system
    """
    STANDARD = "Standard"
    """Standard service level"""
    PREMIUM = "Premium"
    """Premium service level"""
    ULTRA = "Ultra"
    """Ultra service level"""
