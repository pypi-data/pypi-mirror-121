# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'BillingType',
    'ClusterSkuNameEnum',
    'IdentityType',
    'PublicNetworkAccessType',
    'WorkspaceEntityStatus',
    'WorkspaceSkuNameEnum',
]


class BillingType(str, Enum):
    """
    The cluster's billing type.
    """
    CLUSTER = "Cluster"
    WORKSPACES = "Workspaces"


class ClusterSkuNameEnum(str, Enum):
    """
    The name of the SKU.
    """
    CAPACITY_RESERVATION = "CapacityReservation"


class IdentityType(str, Enum):
    """
    Type of managed service identity.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    NONE = "None"


class PublicNetworkAccessType(str, Enum):
    """
    The network access type for accessing Log Analytics query.
    """
    ENABLED = "Enabled"
    """Enables connectivity to Log Analytics through public DNS."""
    DISABLED = "Disabled"
    """Disables public connectivity to Log Analytics through public DNS."""


class WorkspaceEntityStatus(str, Enum):
    """
    The provisioning state of the workspace.
    """
    CREATING = "Creating"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELED = "Canceled"
    DELETING = "Deleting"
    PROVISIONING_ACCOUNT = "ProvisioningAccount"
    UPDATING = "Updating"


class WorkspaceSkuNameEnum(str, Enum):
    """
    The name of the SKU.
    """
    FREE = "Free"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    PER_NODE = "PerNode"
    PER_GB2018 = "PerGB2018"
    STANDALONE = "Standalone"
    CAPACITY_RESERVATION = "CapacityReservation"
    LA_CLUSTER = "LACluster"
