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
    'GetNamespaceResult',
    'AwaitableGetNamespaceResult',
    'get_namespace',
]

@pulumi.output_type
class GetNamespaceResult:
    """
    Description of a namespace resource.
    """
    def __init__(__self__, created_at=None, encryption=None, id=None, identity=None, location=None, metric_id=None, name=None, private_endpoint_connections=None, provisioning_state=None, service_bus_endpoint=None, sku=None, status=None, system_data=None, tags=None, type=None, updated_at=None, zone_redundant=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if encryption and not isinstance(encryption, dict):
            raise TypeError("Expected argument 'encryption' to be a dict")
        pulumi.set(__self__, "encryption", encryption)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if metric_id and not isinstance(metric_id, str):
            raise TypeError("Expected argument 'metric_id' to be a str")
        pulumi.set(__self__, "metric_id", metric_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_endpoint_connections and not isinstance(private_endpoint_connections, list):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if service_bus_endpoint and not isinstance(service_bus_endpoint, str):
            raise TypeError("Expected argument 'service_bus_endpoint' to be a str")
        pulumi.set(__self__, "service_bus_endpoint", service_bus_endpoint)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if zone_redundant and not isinstance(zone_redundant, bool):
            raise TypeError("Expected argument 'zone_redundant' to be a bool")
        pulumi.set(__self__, "zone_redundant", zone_redundant)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The time the namespace was created
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.EncryptionResponse']:
        """
        Properties of BYOK Encryption description
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        Properties of BYOK Identity description
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="metricId")
    def metric_id(self) -> str:
        """
        Identifier for Azure Insights metrics
        """
        return pulumi.get(self, "metric_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Optional[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        List of private endpoint connections.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the namespace.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceBusEndpoint")
    def service_bus_endpoint(self) -> str:
        """
        Endpoint you can use to perform Service Bus operations.
        """
        return pulumi.get(self, "service_bus_endpoint")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SBSkuResponse']:
        """
        Properties of SKU
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the namespace.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The time the namespace was updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> Optional[bool]:
        """
        Enabling this property creates a Premium Service Bus Namespace in regions supported availability zones.
        """
        return pulumi.get(self, "zone_redundant")


class AwaitableGetNamespaceResult(GetNamespaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamespaceResult(
            created_at=self.created_at,
            encryption=self.encryption,
            id=self.id,
            identity=self.identity,
            location=self.location,
            metric_id=self.metric_id,
            name=self.name,
            private_endpoint_connections=self.private_endpoint_connections,
            provisioning_state=self.provisioning_state,
            service_bus_endpoint=self.service_bus_endpoint,
            sku=self.sku,
            status=self.status,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            updated_at=self.updated_at,
            zone_redundant=self.zone_redundant)


def get_namespace(namespace_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamespaceResult:
    """
    Description of a namespace resource.


    :param str namespace_name: The namespace name
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:servicebus/v20210101preview:getNamespace', __args__, opts=opts, typ=GetNamespaceResult).value

    return AwaitableGetNamespaceResult(
        created_at=__ret__.created_at,
        encryption=__ret__.encryption,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        metric_id=__ret__.metric_id,
        name=__ret__.name,
        private_endpoint_connections=__ret__.private_endpoint_connections,
        provisioning_state=__ret__.provisioning_state,
        service_bus_endpoint=__ret__.service_bus_endpoint,
        sku=__ret__.sku,
        status=__ret__.status,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        updated_at=__ret__.updated_at,
        zone_redundant=__ret__.zone_redundant)
