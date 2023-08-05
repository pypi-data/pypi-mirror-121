# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AddonType',
    'DhcpTypeEnum',
    'DnsServiceLogLevelEnum',
    'InternetEnum',
    'PortMirroringDirectionEnum',
    'ScriptExecutionParameterType',
    'SslEnum',
]


class AddonType(str, Enum):
    """
    The type of private cloud addon
    """
    SRM = "SRM"
    VR = "VR"


class DhcpTypeEnum(str, Enum):
    """
    Type of DHCP: SERVER or RELAY.
    """
    SERVE_R_RELAY = "SERVER, RELAY"


class DnsServiceLogLevelEnum(str, Enum):
    """
    DNS Service log level.
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class InternetEnum(str, Enum):
    """
    Connectivity to internet is enabled or disabled
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class PortMirroringDirectionEnum(str, Enum):
    """
    Direction of port mirroring profile.
    """
    INGRES_S_EGRES_S_BIDIRECTIONAL = "INGRESS, EGRESS, BIDIRECTIONAL"


class ScriptExecutionParameterType(str, Enum):
    """
    The type of execution parameter
    """
    VALUE = "Value"
    SECURE_VALUE = "SecureValue"
    CREDENTIAL = "Credential"


class SslEnum(str, Enum):
    """
    Protect LDAP communication using SSL certificate (LDAPS)
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"
