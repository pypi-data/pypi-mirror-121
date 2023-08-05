# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetRestorePointResult',
    'AwaitableGetRestorePointResult',
    'get_restore_point',
]

@pulumi.output_type
class GetRestorePointResult:
    """
    Restore Point details.
    """
    def __init__(__self__, consistency_mode=None, exclude_disks=None, id=None, name=None, provisioning_details=None, provisioning_state=None, source_metadata=None, type=None):
        if consistency_mode and not isinstance(consistency_mode, str):
            raise TypeError("Expected argument 'consistency_mode' to be a str")
        pulumi.set(__self__, "consistency_mode", consistency_mode)
        if exclude_disks and not isinstance(exclude_disks, list):
            raise TypeError("Expected argument 'exclude_disks' to be a list")
        pulumi.set(__self__, "exclude_disks", exclude_disks)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_details and not isinstance(provisioning_details, dict):
            raise TypeError("Expected argument 'provisioning_details' to be a dict")
        pulumi.set(__self__, "provisioning_details", provisioning_details)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if source_metadata and not isinstance(source_metadata, dict):
            raise TypeError("Expected argument 'source_metadata' to be a dict")
        pulumi.set(__self__, "source_metadata", source_metadata)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="consistencyMode")
    def consistency_mode(self) -> str:
        """
        Gets the consistency mode for the restore point. Please refer to https://aka.ms/RestorePoints for more details.
        """
        return pulumi.get(self, "consistency_mode")

    @property
    @pulumi.getter(name="excludeDisks")
    def exclude_disks(self) -> Optional[Sequence['outputs.ApiEntityReferenceResponse']]:
        """
        List of disk resource ids that the customer wishes to exclude from the restore point. If no disks are specified, all disks will be included.
        """
        return pulumi.get(self, "exclude_disks")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningDetails")
    def provisioning_details(self) -> 'outputs.RestorePointProvisioningDetailsResponse':
        """
        Gets the provisioning details set by the server during Create restore point operation.
        """
        return pulumi.get(self, "provisioning_details")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Gets the provisioning state of the restore point.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sourceMetadata")
    def source_metadata(self) -> 'outputs.RestorePointSourceMetadataResponse':
        """
        Gets the details of the VM captured at the time of the restore point creation.
        """
        return pulumi.get(self, "source_metadata")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetRestorePointResult(GetRestorePointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRestorePointResult(
            consistency_mode=self.consistency_mode,
            exclude_disks=self.exclude_disks,
            id=self.id,
            name=self.name,
            provisioning_details=self.provisioning_details,
            provisioning_state=self.provisioning_state,
            source_metadata=self.source_metadata,
            type=self.type)


def get_restore_point(resource_group_name: Optional[str] = None,
                      restore_point_collection_name: Optional[str] = None,
                      restore_point_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRestorePointResult:
    """
    Restore Point details.


    :param str resource_group_name: The name of the resource group.
    :param str restore_point_collection_name: The name of the restore point collection.
    :param str restore_point_name: The name of the restore point.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['restorePointCollectionName'] = restore_point_collection_name
    __args__['restorePointName'] = restore_point_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20210701:getRestorePoint', __args__, opts=opts, typ=GetRestorePointResult).value

    return AwaitableGetRestorePointResult(
        consistency_mode=__ret__.consistency_mode,
        exclude_disks=__ret__.exclude_disks,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_details=__ret__.provisioning_details,
        provisioning_state=__ret__.provisioning_state,
        source_metadata=__ret__.source_metadata,
        type=__ret__.type)
