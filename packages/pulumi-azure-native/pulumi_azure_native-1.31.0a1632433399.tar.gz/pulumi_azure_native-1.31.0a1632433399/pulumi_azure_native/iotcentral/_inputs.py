# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'AppSkuInfoArgs',
]

@pulumi.input_type
class AppSkuInfoArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'AppSku']]):
        """
        Information about the SKU of the IoT Central application.
        :param pulumi.Input[Union[str, 'AppSku']] name: The name of the SKU.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'AppSku']]:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'AppSku']]):
        pulumi.set(self, "name", value)


