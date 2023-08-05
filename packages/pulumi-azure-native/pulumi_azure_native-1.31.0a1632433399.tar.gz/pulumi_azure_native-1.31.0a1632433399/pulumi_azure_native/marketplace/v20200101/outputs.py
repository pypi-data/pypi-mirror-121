# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'PlanResponse',
]

@pulumi.output_type
class PlanResponse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "altStackReference":
            suggest = "alt_stack_reference"
        elif key == "planDisplayName":
            suggest = "plan_display_name"
        elif key == "planId":
            suggest = "plan_id"
        elif key == "skuId":
            suggest = "sku_id"
        elif key == "stackType":
            suggest = "stack_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PlanResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PlanResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PlanResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 alt_stack_reference: str,
                 plan_display_name: str,
                 plan_id: str,
                 sku_id: str,
                 stack_type: str,
                 accessibility: Optional[str] = None):
        """
        :param str alt_stack_reference: Alternative stack type
        :param str plan_display_name: Friendly name for the plan for display in the marketplace
        :param str plan_id: Text identifier for this plan
        :param str sku_id: Identifier for this plan
        :param str stack_type: Stack type (classic or arm)
        :param str accessibility: Plan accessibility
        """
        pulumi.set(__self__, "alt_stack_reference", alt_stack_reference)
        pulumi.set(__self__, "plan_display_name", plan_display_name)
        pulumi.set(__self__, "plan_id", plan_id)
        pulumi.set(__self__, "sku_id", sku_id)
        pulumi.set(__self__, "stack_type", stack_type)
        if accessibility is not None:
            pulumi.set(__self__, "accessibility", accessibility)

    @property
    @pulumi.getter(name="altStackReference")
    def alt_stack_reference(self) -> str:
        """
        Alternative stack type
        """
        return pulumi.get(self, "alt_stack_reference")

    @property
    @pulumi.getter(name="planDisplayName")
    def plan_display_name(self) -> str:
        """
        Friendly name for the plan for display in the marketplace
        """
        return pulumi.get(self, "plan_display_name")

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> str:
        """
        Text identifier for this plan
        """
        return pulumi.get(self, "plan_id")

    @property
    @pulumi.getter(name="skuId")
    def sku_id(self) -> str:
        """
        Identifier for this plan
        """
        return pulumi.get(self, "sku_id")

    @property
    @pulumi.getter(name="stackType")
    def stack_type(self) -> str:
        """
        Stack type (classic or arm)
        """
        return pulumi.get(self, "stack_type")

    @property
    @pulumi.getter
    def accessibility(self) -> Optional[str]:
        """
        Plan accessibility
        """
        return pulumi.get(self, "accessibility")


