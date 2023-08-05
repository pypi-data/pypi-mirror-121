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
    'GetPrivateEndpointConnectionResult',
    'AwaitableGetPrivateEndpointConnectionResult',
    'get_private_endpoint_connection',
]

@pulumi.output_type
class GetPrivateEndpointConnectionResult:
    """
    Private endpoint connection resource.
    """
    def __init__(__self__, etag=None, id=None, location=None, name=None, private_endpoint=None, private_link_service_connection_state=None, provisioning_state=None, tags=None, type=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_endpoint and not isinstance(private_endpoint, dict):
            raise TypeError("Expected argument 'private_endpoint' to be a dict")
        pulumi.set(__self__, "private_endpoint", private_endpoint)
        if private_link_service_connection_state and not isinstance(private_link_service_connection_state, dict):
            raise TypeError("Expected argument 'private_link_service_connection_state' to be a dict")
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Modified whenever there is a change in the state of private endpoint connection.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified identifier of the key vault resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Azure location of the key vault resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the key vault resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        Properties of the private endpoint object.
        """
        return pulumi.get(self, "private_endpoint")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> Optional['outputs.PrivateLinkServiceConnectionStateResponse']:
        """
        Approval state of the private link connection.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the private endpoint connection.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Tags assigned to the key vault resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type of the key vault resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetPrivateEndpointConnectionResult(GetPrivateEndpointConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrivateEndpointConnectionResult(
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            private_endpoint=self.private_endpoint,
            private_link_service_connection_state=self.private_link_service_connection_state,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type)


def get_private_endpoint_connection(private_endpoint_connection_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    vault_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrivateEndpointConnectionResult:
    """
    Private endpoint connection resource.


    :param str private_endpoint_connection_name: Name of the private endpoint connection associated with the key vault.
    :param str resource_group_name: Name of the resource group that contains the key vault.
    :param str vault_name: The name of the key vault.
    """
    __args__ = dict()
    __args__['privateEndpointConnectionName'] = private_endpoint_connection_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['vaultName'] = vault_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:keyvault/v20190901:getPrivateEndpointConnection', __args__, opts=opts, typ=GetPrivateEndpointConnectionResult).value

    return AwaitableGetPrivateEndpointConnectionResult(
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        private_endpoint=__ret__.private_endpoint,
        private_link_service_connection_state=__ret__.private_link_service_connection_state,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type)
