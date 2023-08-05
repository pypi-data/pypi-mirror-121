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
    'GetConnectivityConfigurationResult',
    'AwaitableGetConnectivityConfigurationResult',
    'get_connectivity_configuration',
]

@pulumi.output_type
class GetConnectivityConfigurationResult:
    """
    The network manager connectivity configuration resource
    """
    def __init__(__self__, applies_to_groups=None, connectivity_topology=None, delete_existing_peering=None, description=None, display_name=None, etag=None, hubs=None, id=None, is_global=None, name=None, provisioning_state=None, system_data=None, type=None):
        if applies_to_groups and not isinstance(applies_to_groups, list):
            raise TypeError("Expected argument 'applies_to_groups' to be a list")
        pulumi.set(__self__, "applies_to_groups", applies_to_groups)
        if connectivity_topology and not isinstance(connectivity_topology, str):
            raise TypeError("Expected argument 'connectivity_topology' to be a str")
        pulumi.set(__self__, "connectivity_topology", connectivity_topology)
        if delete_existing_peering and not isinstance(delete_existing_peering, str):
            raise TypeError("Expected argument 'delete_existing_peering' to be a str")
        pulumi.set(__self__, "delete_existing_peering", delete_existing_peering)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if hubs and not isinstance(hubs, list):
            raise TypeError("Expected argument 'hubs' to be a list")
        pulumi.set(__self__, "hubs", hubs)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_global and not isinstance(is_global, str):
            raise TypeError("Expected argument 'is_global' to be a str")
        pulumi.set(__self__, "is_global", is_global)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="appliesToGroups")
    def applies_to_groups(self) -> Optional[Sequence['outputs.ConnectivityGroupItemResponse']]:
        """
        Groups for configuration
        """
        return pulumi.get(self, "applies_to_groups")

    @property
    @pulumi.getter(name="connectivityTopology")
    def connectivity_topology(self) -> str:
        """
        Connectivity topology type.
        """
        return pulumi.get(self, "connectivity_topology")

    @property
    @pulumi.getter(name="deleteExistingPeering")
    def delete_existing_peering(self) -> Optional[str]:
        """
        Flag if need to remove current existing peerings.
        """
        return pulumi.get(self, "delete_existing_peering")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the connectivity configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        A friendly name for the resource.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def hubs(self) -> Optional[Sequence['outputs.HubResponse']]:
        """
        List of hubItems
        """
        return pulumi.get(self, "hubs")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isGlobal")
    def is_global(self) -> Optional[str]:
        """
        Flag if global mesh is supported.
        """
        return pulumi.get(self, "is_global")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the connectivity configuration resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata related to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetConnectivityConfigurationResult(GetConnectivityConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectivityConfigurationResult(
            applies_to_groups=self.applies_to_groups,
            connectivity_topology=self.connectivity_topology,
            delete_existing_peering=self.delete_existing_peering,
            description=self.description,
            display_name=self.display_name,
            etag=self.etag,
            hubs=self.hubs,
            id=self.id,
            is_global=self.is_global,
            name=self.name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            type=self.type)


def get_connectivity_configuration(configuration_name: Optional[str] = None,
                                   network_manager_name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectivityConfigurationResult:
    """
    The network manager connectivity configuration resource


    :param str configuration_name: The name of the network manager connectivity configuration.
    :param str network_manager_name: The name of the network manager.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['configurationName'] = configuration_name
    __args__['networkManagerName'] = network_manager_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20210201preview:getConnectivityConfiguration', __args__, opts=opts, typ=GetConnectivityConfigurationResult).value

    return AwaitableGetConnectivityConfigurationResult(
        applies_to_groups=__ret__.applies_to_groups,
        connectivity_topology=__ret__.connectivity_topology,
        delete_existing_peering=__ret__.delete_existing_peering,
        description=__ret__.description,
        display_name=__ret__.display_name,
        etag=__ret__.etag,
        hubs=__ret__.hubs,
        id=__ret__.id,
        is_global=__ret__.is_global,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        type=__ret__.type)
