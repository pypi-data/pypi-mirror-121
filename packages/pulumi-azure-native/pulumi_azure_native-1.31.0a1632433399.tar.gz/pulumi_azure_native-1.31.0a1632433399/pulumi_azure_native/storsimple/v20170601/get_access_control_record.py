# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetAccessControlRecordResult',
    'AwaitableGetAccessControlRecordResult',
    'get_access_control_record',
]

@pulumi.output_type
class GetAccessControlRecordResult:
    """
    The access control record.
    """
    def __init__(__self__, id=None, initiator_name=None, kind=None, name=None, type=None, volume_count=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if initiator_name and not isinstance(initiator_name, str):
            raise TypeError("Expected argument 'initiator_name' to be a str")
        pulumi.set(__self__, "initiator_name", initiator_name)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if volume_count and not isinstance(volume_count, int):
            raise TypeError("Expected argument 'volume_count' to be a int")
        pulumi.set(__self__, "volume_count", volume_count)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="initiatorName")
    def initiator_name(self) -> str:
        """
        The iSCSI initiator name (IQN).
        """
        return pulumi.get(self, "initiator_name")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        The Kind of the object. Currently only Series8000 is supported
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the object.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="volumeCount")
    def volume_count(self) -> int:
        """
        The number of volumes using the access control record.
        """
        return pulumi.get(self, "volume_count")


class AwaitableGetAccessControlRecordResult(GetAccessControlRecordResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessControlRecordResult(
            id=self.id,
            initiator_name=self.initiator_name,
            kind=self.kind,
            name=self.name,
            type=self.type,
            volume_count=self.volume_count)


def get_access_control_record(access_control_record_name: Optional[str] = None,
                              manager_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccessControlRecordResult:
    """
    The access control record.


    :param str access_control_record_name: Name of access control record to be fetched.
    :param str manager_name: The manager name
    :param str resource_group_name: The resource group name
    """
    __args__ = dict()
    __args__['accessControlRecordName'] = access_control_record_name
    __args__['managerName'] = manager_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:storsimple/v20170601:getAccessControlRecord', __args__, opts=opts, typ=GetAccessControlRecordResult).value

    return AwaitableGetAccessControlRecordResult(
        id=__ret__.id,
        initiator_name=__ret__.initiator_name,
        kind=__ret__.kind,
        name=__ret__.name,
        type=__ret__.type,
        volume_count=__ret__.volume_count)
