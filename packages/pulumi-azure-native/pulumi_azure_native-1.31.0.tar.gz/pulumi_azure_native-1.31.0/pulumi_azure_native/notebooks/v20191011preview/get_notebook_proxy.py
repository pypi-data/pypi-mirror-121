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
    'GetNotebookProxyResult',
    'AwaitableGetNotebookProxyResult',
    'get_notebook_proxy',
]

@pulumi.output_type
class GetNotebookProxyResult:
    """
    A NotebookProxy resource.
    """
    def __init__(__self__, hostname=None, id=None, name=None, public_dns=None, public_network_access=None, region=None, resource_id=None, secondary_app_id=None, system_data=None, type=None):
        if hostname and not isinstance(hostname, str):
            raise TypeError("Expected argument 'hostname' to be a str")
        pulumi.set(__self__, "hostname", hostname)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if public_dns and not isinstance(public_dns, str):
            raise TypeError("Expected argument 'public_dns' to be a str")
        pulumi.set(__self__, "public_dns", public_dns)
        if public_network_access and not isinstance(public_network_access, str):
            raise TypeError("Expected argument 'public_network_access' to be a str")
        pulumi.set(__self__, "public_network_access", public_network_access)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if secondary_app_id and not isinstance(secondary_app_id, str):
            raise TypeError("Expected argument 'secondary_app_id' to be a str")
        pulumi.set(__self__, "secondary_app_id", secondary_app_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def hostname(self) -> Optional[str]:
        """
        The friendly string identifier of the creator of the NotebookProxy resource.
        """
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicDns")
    def public_dns(self) -> Optional[str]:
        """
        The public DNS name
        """
        return pulumi.get(self, "public_dns")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[str]:
        """
        Allow public network access on a V-Net locked notebook resource
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        """
        The region of the NotebookProxy resource.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        """
        The unique identifier (a GUID) generated for every resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="secondaryAppId")
    def secondary_app_id(self) -> Optional[str]:
        """
        The alternate application ID used for auth token request in the data plane
        """
        return pulumi.get(self, "secondary_app_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> Optional['outputs.NotebookResourceSystemDataResponse']:
        """
        System data for notebook resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Storage/storageAccounts or Microsoft.Notebooks/notebookProxies.
        """
        return pulumi.get(self, "type")


class AwaitableGetNotebookProxyResult(GetNotebookProxyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNotebookProxyResult(
            hostname=self.hostname,
            id=self.id,
            name=self.name,
            public_dns=self.public_dns,
            public_network_access=self.public_network_access,
            region=self.region,
            resource_id=self.resource_id,
            secondary_app_id=self.secondary_app_id,
            system_data=self.system_data,
            type=self.type)


def get_notebook_proxy(resource_group_name: Optional[str] = None,
                       resource_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNotebookProxyResult:
    """
    A NotebookProxy resource.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: The name of the resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:notebooks/v20191011preview:getNotebookProxy', __args__, opts=opts, typ=GetNotebookProxyResult).value

    return AwaitableGetNotebookProxyResult(
        hostname=__ret__.hostname,
        id=__ret__.id,
        name=__ret__.name,
        public_dns=__ret__.public_dns,
        public_network_access=__ret__.public_network_access,
        region=__ret__.region,
        resource_id=__ret__.resource_id,
        secondary_app_id=__ret__.secondary_app_id,
        system_data=__ret__.system_data,
        type=__ret__.type)
