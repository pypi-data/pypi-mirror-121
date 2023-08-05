# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ApplicationGroupType',
    'CommandLineSetting',
    'HostPoolType',
    'LoadBalancerType',
    'PersonalDesktopAssignmentType',
    'PreferredAppGroupType',
    'RegistrationTokenOperation',
    'RemoteApplicationType',
]


class ApplicationGroupType(str, Enum):
    """
    Resource Type of ApplicationGroup.
    """
    REMOTE_APP = "RemoteApp"
    DESKTOP = "Desktop"


class CommandLineSetting(str, Enum):
    """
    Specifies whether this published application can be launched with command line arguments provided by the client, command line arguments specified at publish time, or no command line arguments at all.
    """
    DO_NOT_ALLOW = "DoNotAllow"
    ALLOW = "Allow"
    REQUIRE = "Require"


class HostPoolType(str, Enum):
    """
    HostPool type for desktop.
    """
    PERSONAL = "Personal"
    POOLED = "Pooled"


class LoadBalancerType(str, Enum):
    """
    The type of the load balancer.
    """
    BREADTH_FIRST = "BreadthFirst"
    DEPTH_FIRST = "DepthFirst"
    PERSISTENT = "Persistent"


class PersonalDesktopAssignmentType(str, Enum):
    """
    PersonalDesktopAssignment type for HostPool.
    """
    AUTOMATIC = "Automatic"
    DIRECT = "Direct"


class PreferredAppGroupType(str, Enum):
    """
    The type of preferred application group type, default to Desktop Application Group
    """
    NONE = "None"
    DESKTOP = "Desktop"
    RAIL_APPLICATIONS = "RailApplications"


class RegistrationTokenOperation(str, Enum):
    """
    The type of resetting the token.
    """
    DELETE = "Delete"
    NONE = "None"
    UPDATE = "Update"


class RemoteApplicationType(str, Enum):
    """
    Resource Type of Application.
    """
    IN_BUILT = "InBuilt"
    MSIX_APPLICATION = "MsixApplication"
