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
    'GetServerResult',
    'AwaitableGetServerResult',
    'get_server',
]

@pulumi.output_type
class GetServerResult:
    """
    Represents a server.
    """
    def __init__(__self__, administrator_login=None, availability_zone=None, backup=None, fully_qualified_domain_name=None, high_availability=None, id=None, location=None, maintenance_window=None, name=None, network=None, replica_capacity=None, replication_role=None, sku=None, source_server_resource_id=None, state=None, storage=None, system_data=None, tags=None, type=None, version=None):
        if administrator_login and not isinstance(administrator_login, str):
            raise TypeError("Expected argument 'administrator_login' to be a str")
        pulumi.set(__self__, "administrator_login", administrator_login)
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if backup and not isinstance(backup, dict):
            raise TypeError("Expected argument 'backup' to be a dict")
        pulumi.set(__self__, "backup", backup)
        if fully_qualified_domain_name and not isinstance(fully_qualified_domain_name, str):
            raise TypeError("Expected argument 'fully_qualified_domain_name' to be a str")
        pulumi.set(__self__, "fully_qualified_domain_name", fully_qualified_domain_name)
        if high_availability and not isinstance(high_availability, dict):
            raise TypeError("Expected argument 'high_availability' to be a dict")
        pulumi.set(__self__, "high_availability", high_availability)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if maintenance_window and not isinstance(maintenance_window, dict):
            raise TypeError("Expected argument 'maintenance_window' to be a dict")
        pulumi.set(__self__, "maintenance_window", maintenance_window)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network and not isinstance(network, dict):
            raise TypeError("Expected argument 'network' to be a dict")
        pulumi.set(__self__, "network", network)
        if replica_capacity and not isinstance(replica_capacity, int):
            raise TypeError("Expected argument 'replica_capacity' to be a int")
        pulumi.set(__self__, "replica_capacity", replica_capacity)
        if replication_role and not isinstance(replication_role, str):
            raise TypeError("Expected argument 'replication_role' to be a str")
        pulumi.set(__self__, "replication_role", replication_role)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if source_server_resource_id and not isinstance(source_server_resource_id, str):
            raise TypeError("Expected argument 'source_server_resource_id' to be a str")
        pulumi.set(__self__, "source_server_resource_id", source_server_resource_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if storage and not isinstance(storage, dict):
            raise TypeError("Expected argument 'storage' to be a dict")
        pulumi.set(__self__, "storage", storage)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> Optional[str]:
        """
        The administrator's login name of a server. Can only be specified when the server is being created (and is required for creation).
        """
        return pulumi.get(self, "administrator_login")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        availability Zone information of the server.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter
    def backup(self) -> Optional['outputs.BackupResponse']:
        """
        Backup related properties of a server.
        """
        return pulumi.get(self, "backup")

    @property
    @pulumi.getter(name="fullyQualifiedDomainName")
    def fully_qualified_domain_name(self) -> str:
        """
        The fully qualified domain name of a server.
        """
        return pulumi.get(self, "fully_qualified_domain_name")

    @property
    @pulumi.getter(name="highAvailability")
    def high_availability(self) -> Optional['outputs.HighAvailabilityResponse']:
        """
        High availability related properties of a server.
        """
        return pulumi.get(self, "high_availability")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> Optional['outputs.MaintenanceWindowResponse']:
        """
        Maintenance window of a server.
        """
        return pulumi.get(self, "maintenance_window")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> Optional['outputs.NetworkResponse']:
        """
        Network related properties of a server.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter(name="replicaCapacity")
    def replica_capacity(self) -> int:
        """
        The maximum number of replicas that a primary server can have.
        """
        return pulumi.get(self, "replica_capacity")

    @property
    @pulumi.getter(name="replicationRole")
    def replication_role(self) -> Optional[str]:
        """
        The replication role.
        """
        return pulumi.get(self, "replication_role")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The SKU (pricing tier) of the server.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="sourceServerResourceId")
    def source_server_resource_id(self) -> Optional[str]:
        """
        The source MySQL server id.
        """
        return pulumi.get(self, "source_server_resource_id")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of a server.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def storage(self) -> Optional['outputs.StorageResponse']:
        """
        Storage related properties of a server.
        """
        return pulumi.get(self, "storage")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Server version.
        """
        return pulumi.get(self, "version")


class AwaitableGetServerResult(GetServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerResult(
            administrator_login=self.administrator_login,
            availability_zone=self.availability_zone,
            backup=self.backup,
            fully_qualified_domain_name=self.fully_qualified_domain_name,
            high_availability=self.high_availability,
            id=self.id,
            location=self.location,
            maintenance_window=self.maintenance_window,
            name=self.name,
            network=self.network,
            replica_capacity=self.replica_capacity,
            replication_role=self.replication_role,
            sku=self.sku,
            source_server_resource_id=self.source_server_resource_id,
            state=self.state,
            storage=self.storage,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            version=self.version)


def get_server(resource_group_name: Optional[str] = None,
               server_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerResult:
    """
    Represents a server.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str server_name: The name of the server.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:dbformysql/v20210501:getServer', __args__, opts=opts, typ=GetServerResult).value

    return AwaitableGetServerResult(
        administrator_login=__ret__.administrator_login,
        availability_zone=__ret__.availability_zone,
        backup=__ret__.backup,
        fully_qualified_domain_name=__ret__.fully_qualified_domain_name,
        high_availability=__ret__.high_availability,
        id=__ret__.id,
        location=__ret__.location,
        maintenance_window=__ret__.maintenance_window,
        name=__ret__.name,
        network=__ret__.network,
        replica_capacity=__ret__.replica_capacity,
        replication_role=__ret__.replication_role,
        sku=__ret__.sku,
        source_server_resource_id=__ret__.source_server_resource_id,
        state=__ret__.state,
        storage=__ret__.storage,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        version=__ret__.version)
