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
    'ReferenceDataSetKeyPropertyResponse',
    'SkuResponse',
]

@pulumi.output_type
class ReferenceDataSetKeyPropertyResponse(dict):
    """
    A key property for the reference data set. A reference data set can have multiple key properties.
    """
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        A key property for the reference data set. A reference data set can have multiple key properties.
        :param str name: The name of the key property.
        :param str type: The type of the key property.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the key property.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the key property.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class SkuResponse(dict):
    """
    The sku determines the capacity of the environment, the SLA (in queries-per-minute and total capacity), and the billing rate.
    """
    def __init__(__self__, *,
                 capacity: int,
                 name: str):
        """
        The sku determines the capacity of the environment, the SLA (in queries-per-minute and total capacity), and the billing rate.
        :param int capacity: The capacity of the sku. This value can be changed to support scale out of environments after they have been created.
        :param str name: The name of this SKU.
        """
        pulumi.set(__self__, "capacity", capacity)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> int:
        """
        The capacity of the sku. This value can be changed to support scale out of environments after they have been created.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of this SKU.
        """
        return pulumi.get(self, "name")


