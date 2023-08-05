# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'CostAllocationPolicyType',
    'CostAllocationResourceType',
    'RuleStatus',
]


class CostAllocationPolicyType(str, Enum):
    """
    Method of cost allocation for the rule
    """
    FIXED_PROPORTION = "FixedProportion"


class CostAllocationResourceType(str, Enum):
    """
    Type of resources contained in this cost allocation rule
    """
    DIMENSION = "Dimension"
    """Indicates an Azure dimension such as a subscription id or resource group name is being used for allocation."""
    TAG = "Tag"
    """Allocates cost based on Azure Tag key value pairs."""


class RuleStatus(str, Enum):
    """
    Status of the rule
    """
    NOT_ACTIVE = "NotActive"
    """Rule is saved but not used to allocate costs."""
    ACTIVE = "Active"
    """Rule is saved and impacting cost allocation."""
    PROCESSING = "Processing"
    """Rule is saved and cost allocation is being updated. Readonly value that cannot be submitted in a put request."""
