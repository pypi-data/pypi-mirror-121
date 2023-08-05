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
    'GetSkusNestedResourceTypeSecondResult',
    'AwaitableGetSkusNestedResourceTypeSecondResult',
    'get_skus_nested_resource_type_second',
]

@pulumi.output_type
class GetSkusNestedResourceTypeSecondResult:
    def __init__(__self__, id=None, name=None, properties=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
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
    @pulumi.getter
    def properties(self) -> 'outputs.SkuResourceResponseProperties':
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetSkusNestedResourceTypeSecondResult(GetSkusNestedResourceTypeSecondResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSkusNestedResourceTypeSecondResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            system_data=self.system_data,
            type=self.type)


def get_skus_nested_resource_type_second(nested_resource_type_first: Optional[str] = None,
                                         nested_resource_type_second: Optional[str] = None,
                                         provider_namespace: Optional[str] = None,
                                         resource_type: Optional[str] = None,
                                         sku: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSkusNestedResourceTypeSecondResult:
    """
    Use this data source to access information about an existing resource.

    :param str nested_resource_type_first: The first child resource type.
    :param str nested_resource_type_second: The second child resource type.
    :param str provider_namespace: The name of the resource provider hosted within ProviderHub.
    :param str resource_type: The resource type.
    :param str sku: The SKU.
    """
    __args__ = dict()
    __args__['nestedResourceTypeFirst'] = nested_resource_type_first
    __args__['nestedResourceTypeSecond'] = nested_resource_type_second
    __args__['providerNamespace'] = provider_namespace
    __args__['resourceType'] = resource_type
    __args__['sku'] = sku
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:providerhub/v20210601preview:getSkusNestedResourceTypeSecond', __args__, opts=opts, typ=GetSkusNestedResourceTypeSecondResult).value

    return AwaitableGetSkusNestedResourceTypeSecondResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        system_data=__ret__.system_data,
        type=__ret__.type)
