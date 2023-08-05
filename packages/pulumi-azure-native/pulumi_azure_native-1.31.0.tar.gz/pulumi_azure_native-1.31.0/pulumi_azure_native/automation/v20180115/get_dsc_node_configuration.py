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
    'GetDscNodeConfigurationResult',
    'AwaitableGetDscNodeConfigurationResult',
    'get_dsc_node_configuration',
]

@pulumi.output_type
class GetDscNodeConfigurationResult:
    """
    Definition of the dsc node configuration.
    """
    def __init__(__self__, configuration=None, creation_time=None, id=None, increment_node_configuration_build=None, last_modified_time=None, name=None, node_count=None, source=None, type=None):
        if configuration and not isinstance(configuration, dict):
            raise TypeError("Expected argument 'configuration' to be a dict")
        pulumi.set(__self__, "configuration", configuration)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if increment_node_configuration_build and not isinstance(increment_node_configuration_build, bool):
            raise TypeError("Expected argument 'increment_node_configuration_build' to be a bool")
        pulumi.set(__self__, "increment_node_configuration_build", increment_node_configuration_build)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if node_count and not isinstance(node_count, float):
            raise TypeError("Expected argument 'node_count' to be a float")
        pulumi.set(__self__, "node_count", node_count)
        if source and not isinstance(source, str):
            raise TypeError("Expected argument 'source' to be a str")
        pulumi.set(__self__, "source", source)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def configuration(self) -> Optional['outputs.DscConfigurationAssociationPropertyResponse']:
        """
        Gets or sets the configuration of the node.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        Gets or sets creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="incrementNodeConfigurationBuild")
    def increment_node_configuration_build(self) -> Optional[bool]:
        """
        If a new build version of NodeConfiguration is required.
        """
        return pulumi.get(self, "increment_node_configuration_build")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> Optional[str]:
        """
        Gets or sets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nodeCount")
    def node_count(self) -> Optional[float]:
        """
        Number of nodes with this node configuration assigned
        """
        return pulumi.get(self, "node_count")

    @property
    @pulumi.getter
    def source(self) -> Optional[str]:
        """
        Source of node configuration.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetDscNodeConfigurationResult(GetDscNodeConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDscNodeConfigurationResult(
            configuration=self.configuration,
            creation_time=self.creation_time,
            id=self.id,
            increment_node_configuration_build=self.increment_node_configuration_build,
            last_modified_time=self.last_modified_time,
            name=self.name,
            node_count=self.node_count,
            source=self.source,
            type=self.type)


def get_dsc_node_configuration(automation_account_name: Optional[str] = None,
                               node_configuration_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDscNodeConfigurationResult:
    """
    Definition of the dsc node configuration.


    :param str automation_account_name: The name of the automation account.
    :param str node_configuration_name: The Dsc node configuration name.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['automationAccountName'] = automation_account_name
    __args__['nodeConfigurationName'] = node_configuration_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:automation/v20180115:getDscNodeConfiguration', __args__, opts=opts, typ=GetDscNodeConfigurationResult).value

    return AwaitableGetDscNodeConfigurationResult(
        configuration=__ret__.configuration,
        creation_time=__ret__.creation_time,
        id=__ret__.id,
        increment_node_configuration_build=__ret__.increment_node_configuration_build,
        last_modified_time=__ret__.last_modified_time,
        name=__ret__.name,
        node_count=__ret__.node_count,
        source=__ret__.source,
        type=__ret__.type)
