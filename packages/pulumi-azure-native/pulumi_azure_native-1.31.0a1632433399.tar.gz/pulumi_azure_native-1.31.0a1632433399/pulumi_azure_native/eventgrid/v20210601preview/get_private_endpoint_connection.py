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
    def __init__(__self__, group_ids=None, id=None, name=None, private_endpoint=None, private_link_service_connection_state=None, provisioning_state=None, type=None):
        if group_ids and not isinstance(group_ids, list):
            raise TypeError("Expected argument 'group_ids' to be a list")
        pulumi.set(__self__, "group_ids", group_ids)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
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
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> Optional[Sequence[str]]:
        """
        GroupIds from the private link service resource.
        """
        return pulumi.get(self, "group_ids")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified identifier of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        The Private Endpoint resource for this Connection.
        """
        return pulumi.get(self, "private_endpoint")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> Optional['outputs.ConnectionStateResponse']:
        """
        Details about the state of the connection.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state of the Private Endpoint Connection.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetPrivateEndpointConnectionResult(GetPrivateEndpointConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrivateEndpointConnectionResult(
            group_ids=self.group_ids,
            id=self.id,
            name=self.name,
            private_endpoint=self.private_endpoint,
            private_link_service_connection_state=self.private_link_service_connection_state,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_private_endpoint_connection(parent_name: Optional[str] = None,
                                    parent_type: Optional[str] = None,
                                    private_endpoint_connection_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrivateEndpointConnectionResult:
    """
    Use this data source to access information about an existing resource.

    :param str parent_name: The name of the parent resource (namely, either, the topic name, domain name, or partner namespace name).
    :param str parent_type: The type of the parent resource. This can be either \'topics\', \'domains\', or \'partnerNamespaces\'.
    :param str private_endpoint_connection_name: The name of the private endpoint connection connection.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    """
    __args__ = dict()
    __args__['parentName'] = parent_name
    __args__['parentType'] = parent_type
    __args__['privateEndpointConnectionName'] = private_endpoint_connection_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:eventgrid/v20210601preview:getPrivateEndpointConnection', __args__, opts=opts, typ=GetPrivateEndpointConnectionResult).value

    return AwaitableGetPrivateEndpointConnectionResult(
        group_ids=__ret__.group_ids,
        id=__ret__.id,
        name=__ret__.name,
        private_endpoint=__ret__.private_endpoint,
        private_link_service_connection_state=__ret__.private_link_service_connection_state,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)
