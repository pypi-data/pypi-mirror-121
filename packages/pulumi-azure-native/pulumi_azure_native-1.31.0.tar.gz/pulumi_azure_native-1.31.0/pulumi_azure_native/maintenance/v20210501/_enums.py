# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'MaintenanceScope',
    'Visibility',
]


class MaintenanceScope(str, Enum):
    """
    Gets or sets maintenanceScope of the configuration
    """
    HOST = "Host"
    """This maintenance scope controls installation of azure platform updates i.e. services on physical nodes hosting customer VMs."""
    OS_IMAGE = "OSImage"
    """This maintenance scope controls os image installation on VM/VMSS"""
    EXTENSION = "Extension"
    """This maintenance scope controls extension installation on VM/VMSS"""
    IN_GUEST_PATCH = "InGuestPatch"
    """This maintenance scope controls installation of windows and linux packages on VM/VMSS"""
    SQLDB = "SQLDB"
    """This maintenance scope controls installation of SQL server platform updates."""
    SQL_MANAGED_INSTANCE = "SQLManagedInstance"
    """This maintenance scope controls installation of SQL managed instance platform update."""


class Visibility(str, Enum):
    """
    Gets or sets the visibility of the configuration. The default value is 'Custom'
    """
    CUSTOM = "Custom"
    """Only visible to users with permissions."""
    PUBLIC = "Public"
    """Visible to all users."""
