# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'LevelType',
    'OperatorScopeType',
    'OperatorType',
    'ResourceIdentityType',
]


class LevelType(str, Enum):
    """
    Level of the status.
    """
    ERROR = "Error"
    WARNING = "Warning"
    INFORMATION = "Information"


class OperatorScopeType(str, Enum):
    """
    Scope at which the operator will be installed.
    """
    CLUSTER = "cluster"
    NAMESPACE = "namespace"


class OperatorType(str, Enum):
    """
    Type of the operator
    """
    FLUX = "Flux"


class ResourceIdentityType(str, Enum):
    """
    The identity type.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
