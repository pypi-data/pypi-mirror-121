# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AddRemove',
    'ConfigurationState',
    'LabUserAccessMode',
    'ManagedLabVmSize',
]


class AddRemove(str, Enum):
    """
    Enum indicating if user is adding or removing a favorite lab
    """
    ADD = "Add"
    """Indicates that a user is adding a favorite lab"""
    REMOVE = "Remove"
    """Indicates that a user is removing a favorite lab"""


class ConfigurationState(str, Enum):
    """
    Describes the user's progress in configuring their environment setting
    """
    NOT_APPLICABLE = "NotApplicable"
    """User either hasn't started configuring their template
or they haven't started the configuration process."""
    COMPLETED = "Completed"
    """User is finished modifying the template."""


class LabUserAccessMode(str, Enum):
    """
    Lab user access mode (open to all vs. restricted to those listed on the lab).
    """
    RESTRICTED = "Restricted"
    """Only users registered with the lab can access VMs."""
    OPEN = "Open"
    """Any user can register with the lab and access its VMs."""


class ManagedLabVmSize(str, Enum):
    """
    The size of the virtual machine
    """
    BASIC = "Basic"
    """The base VM size"""
    STANDARD = "Standard"
    """The standard or default VM size"""
    PERFORMANCE = "Performance"
    """The most performant VM size"""
