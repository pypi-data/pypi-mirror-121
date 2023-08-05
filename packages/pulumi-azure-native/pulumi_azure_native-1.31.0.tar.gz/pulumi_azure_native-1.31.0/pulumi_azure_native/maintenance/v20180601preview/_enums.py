# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'MaintenanceScope',
]


class MaintenanceScope(str, Enum):
    """
    Gets or sets maintenanceScope of the configuration
    """
    ALL = "All"
    HOST = "Host"
    RESOURCE = "Resource"
    IN_RESOURCE = "InResource"
