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
    'GetShareResult',
    'AwaitableGetShareResult',
    'get_share',
]

@pulumi.output_type
class GetShareResult:
    """
    Represents a share on the  Data Box Edge/Gateway device.
    """
    def __init__(__self__, access_protocol=None, azure_container_info=None, client_access_rights=None, data_policy=None, description=None, id=None, monitoring_status=None, name=None, refresh_details=None, share_mappings=None, share_status=None, system_data=None, type=None, user_access_rights=None):
        if access_protocol and not isinstance(access_protocol, str):
            raise TypeError("Expected argument 'access_protocol' to be a str")
        pulumi.set(__self__, "access_protocol", access_protocol)
        if azure_container_info and not isinstance(azure_container_info, dict):
            raise TypeError("Expected argument 'azure_container_info' to be a dict")
        pulumi.set(__self__, "azure_container_info", azure_container_info)
        if client_access_rights and not isinstance(client_access_rights, list):
            raise TypeError("Expected argument 'client_access_rights' to be a list")
        pulumi.set(__self__, "client_access_rights", client_access_rights)
        if data_policy and not isinstance(data_policy, str):
            raise TypeError("Expected argument 'data_policy' to be a str")
        pulumi.set(__self__, "data_policy", data_policy)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if monitoring_status and not isinstance(monitoring_status, str):
            raise TypeError("Expected argument 'monitoring_status' to be a str")
        pulumi.set(__self__, "monitoring_status", monitoring_status)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if refresh_details and not isinstance(refresh_details, dict):
            raise TypeError("Expected argument 'refresh_details' to be a dict")
        pulumi.set(__self__, "refresh_details", refresh_details)
        if share_mappings and not isinstance(share_mappings, list):
            raise TypeError("Expected argument 'share_mappings' to be a list")
        pulumi.set(__self__, "share_mappings", share_mappings)
        if share_status and not isinstance(share_status, str):
            raise TypeError("Expected argument 'share_status' to be a str")
        pulumi.set(__self__, "share_status", share_status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_access_rights and not isinstance(user_access_rights, list):
            raise TypeError("Expected argument 'user_access_rights' to be a list")
        pulumi.set(__self__, "user_access_rights", user_access_rights)

    @property
    @pulumi.getter(name="accessProtocol")
    def access_protocol(self) -> str:
        """
        Access protocol to be used by the share.
        """
        return pulumi.get(self, "access_protocol")

    @property
    @pulumi.getter(name="azureContainerInfo")
    def azure_container_info(self) -> Optional['outputs.AzureContainerInfoResponse']:
        """
        Azure container mapping for the share.
        """
        return pulumi.get(self, "azure_container_info")

    @property
    @pulumi.getter(name="clientAccessRights")
    def client_access_rights(self) -> Optional[Sequence['outputs.ClientAccessRightResponse']]:
        """
        List of IP addresses and corresponding access rights on the share(required for NFS protocol).
        """
        return pulumi.get(self, "client_access_rights")

    @property
    @pulumi.getter(name="dataPolicy")
    def data_policy(self) -> Optional[str]:
        """
        Data policy of the share.
        """
        return pulumi.get(self, "data_policy")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description for the share.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="monitoringStatus")
    def monitoring_status(self) -> str:
        """
        Current monitoring status of the share.
        """
        return pulumi.get(self, "monitoring_status")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="refreshDetails")
    def refresh_details(self) -> Optional['outputs.RefreshDetailsResponse']:
        """
        Details of the refresh job on this share.
        """
        return pulumi.get(self, "refresh_details")

    @property
    @pulumi.getter(name="shareMappings")
    def share_mappings(self) -> Sequence['outputs.MountPointMapResponse']:
        """
        Share mount point to the role.
        """
        return pulumi.get(self, "share_mappings")

    @property
    @pulumi.getter(name="shareStatus")
    def share_status(self) -> str:
        """
        Current status of the share.
        """
        return pulumi.get(self, "share_status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Share on ASE device
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAccessRights")
    def user_access_rights(self) -> Optional[Sequence['outputs.UserAccessRightResponse']]:
        """
        Mapping of users and corresponding access rights on the share (required for SMB protocol).
        """
        return pulumi.get(self, "user_access_rights")


class AwaitableGetShareResult(GetShareResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetShareResult(
            access_protocol=self.access_protocol,
            azure_container_info=self.azure_container_info,
            client_access_rights=self.client_access_rights,
            data_policy=self.data_policy,
            description=self.description,
            id=self.id,
            monitoring_status=self.monitoring_status,
            name=self.name,
            refresh_details=self.refresh_details,
            share_mappings=self.share_mappings,
            share_status=self.share_status,
            system_data=self.system_data,
            type=self.type,
            user_access_rights=self.user_access_rights)


def get_share(device_name: Optional[str] = None,
              name: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetShareResult:
    """
    Represents a share on the  Data Box Edge/Gateway device.


    :param str device_name: The device name.
    :param str name: The share name.
    :param str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['deviceName'] = device_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:databoxedge/v20210201preview:getShare', __args__, opts=opts, typ=GetShareResult).value

    return AwaitableGetShareResult(
        access_protocol=__ret__.access_protocol,
        azure_container_info=__ret__.azure_container_info,
        client_access_rights=__ret__.client_access_rights,
        data_policy=__ret__.data_policy,
        description=__ret__.description,
        id=__ret__.id,
        monitoring_status=__ret__.monitoring_status,
        name=__ret__.name,
        refresh_details=__ret__.refresh_details,
        share_mappings=__ret__.share_mappings,
        share_status=__ret__.share_status,
        system_data=__ret__.system_data,
        type=__ret__.type,
        user_access_rights=__ret__.user_access_rights)
