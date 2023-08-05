# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetPrivateEndpointConnectionResult',
    'AwaitableGetPrivateEndpointConnectionResult',
    'get_private_endpoint_connection',
]

@pulumi.output_type
class GetPrivateEndpointConnectionResult:
    """
    A private endpoint connection for a project.
    """
    def __init__(__self__, e_tag=None, id=None, name=None, properties=None, type=None):
        if e_tag and not isinstance(e_tag, str):
            raise TypeError("Expected argument 'e_tag' to be a str")
        pulumi.set(__self__, "e_tag", e_tag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> Optional[str]:
        """
        For optimistic concurrency control.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Path reference to this private endpoint endpoint connection. /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/assessmentProjects/{projectName}/privateEndpointConnections/{privateEndpointConnectionName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the private endpoint endpoint connection.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.PrivateEndpointConnectionPropertiesResponse':
        """
        Properties of the private endpoint endpoint connection.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the object = [Microsoft.Migrate/assessmentProjects/privateEndpointConnections].
        """
        return pulumi.get(self, "type")


class AwaitableGetPrivateEndpointConnectionResult(GetPrivateEndpointConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrivateEndpointConnectionResult(
            e_tag=self.e_tag,
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_private_endpoint_connection(private_endpoint_connection_name: Optional[str] = None,
                                    project_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrivateEndpointConnectionResult:
    """
    A private endpoint connection for a project.
    API Version: 2019-10-01.


    :param str private_endpoint_connection_name: Unique name of a private endpoint connection within a project.
    :param str project_name: Name of the Azure Migrate project.
    :param str resource_group_name: Name of the Azure Resource Group that project is part of.
    """
    __args__ = dict()
    __args__['privateEndpointConnectionName'] = private_endpoint_connection_name
    __args__['projectName'] = project_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:migrate:getPrivateEndpointConnection', __args__, opts=opts, typ=GetPrivateEndpointConnectionResult).value

    return AwaitableGetPrivateEndpointConnectionResult(
        e_tag=__ret__.e_tag,
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)
