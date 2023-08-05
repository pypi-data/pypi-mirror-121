# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'StorageAccountArgs',
]

@pulumi.input_type
class StorageAccountArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str],
                 is_primary: pulumi.Input[bool]):
        """
        The properties of a storage account associated with this resource.
        :param pulumi.Input[str] id: The id of the storage account resource. Media Services relies on tables and queues as well as blobs, so the primary storage account must be a Standard Storage account (either Microsoft.ClassicStorage or Microsoft.Storage). Blob only storage accounts can be added as secondary storage accounts (isPrimary false).
        :param pulumi.Input[bool] is_primary: Is this storage account resource the primary storage account for the Media Service resource. Blob only storage must set this to false.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "is_primary", is_primary)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        The id of the storage account resource. Media Services relies on tables and queues as well as blobs, so the primary storage account must be a Standard Storage account (either Microsoft.ClassicStorage or Microsoft.Storage). Blob only storage accounts can be added as secondary storage accounts (isPrimary false).
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="isPrimary")
    def is_primary(self) -> pulumi.Input[bool]:
        """
        Is this storage account resource the primary storage account for the Media Service resource. Blob only storage must set this to false.
        """
        return pulumi.get(self, "is_primary")

    @is_primary.setter
    def is_primary(self, value: pulumi.Input[bool]):
        pulumi.set(self, "is_primary", value)


