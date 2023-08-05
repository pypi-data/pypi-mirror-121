# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetApplicationGroupResult',
    'AwaitableGetApplicationGroupResult',
    'get_application_group',
]

@pulumi.output_type
class GetApplicationGroupResult:
    """
    Represents a ApplicationGroup definition.
    """
    def __init__(__self__, application_group_type=None, description=None, friendly_name=None, host_pool_arm_path=None, id=None, location=None, name=None, tags=None, type=None, workspace_arm_path=None):
        if application_group_type and not isinstance(application_group_type, str):
            raise TypeError("Expected argument 'application_group_type' to be a str")
        pulumi.set(__self__, "application_group_type", application_group_type)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if friendly_name and not isinstance(friendly_name, str):
            raise TypeError("Expected argument 'friendly_name' to be a str")
        pulumi.set(__self__, "friendly_name", friendly_name)
        if host_pool_arm_path and not isinstance(host_pool_arm_path, str):
            raise TypeError("Expected argument 'host_pool_arm_path' to be a str")
        pulumi.set(__self__, "host_pool_arm_path", host_pool_arm_path)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if workspace_arm_path and not isinstance(workspace_arm_path, str):
            raise TypeError("Expected argument 'workspace_arm_path' to be a str")
        pulumi.set(__self__, "workspace_arm_path", workspace_arm_path)

    @property
    @pulumi.getter(name="applicationGroupType")
    def application_group_type(self) -> str:
        """
        Resource Type of ApplicationGroup.
        """
        return pulumi.get(self, "application_group_type")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of ApplicationGroup.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[str]:
        """
        Friendly name of ApplicationGroup.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="hostPoolArmPath")
    def host_pool_arm_path(self) -> str:
        """
        HostPool arm path of ApplicationGroup.
        """
        return pulumi.get(self, "host_pool_arm_path")

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
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

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
    @pulumi.getter(name="workspaceArmPath")
    def workspace_arm_path(self) -> str:
        """
        Workspace arm path of ApplicationGroup.
        """
        return pulumi.get(self, "workspace_arm_path")


class AwaitableGetApplicationGroupResult(GetApplicationGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationGroupResult(
            application_group_type=self.application_group_type,
            description=self.description,
            friendly_name=self.friendly_name,
            host_pool_arm_path=self.host_pool_arm_path,
            id=self.id,
            location=self.location,
            name=self.name,
            tags=self.tags,
            type=self.type,
            workspace_arm_path=self.workspace_arm_path)


def get_application_group(application_group_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationGroupResult:
    """
    Represents a ApplicationGroup definition.


    :param str application_group_name: The name of the application group
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['applicationGroupName'] = application_group_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:desktopvirtualization/v20191210preview:getApplicationGroup', __args__, opts=opts, typ=GetApplicationGroupResult).value

    return AwaitableGetApplicationGroupResult(
        application_group_type=__ret__.application_group_type,
        description=__ret__.description,
        friendly_name=__ret__.friendly_name,
        host_pool_arm_path=__ret__.host_pool_arm_path,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        tags=__ret__.tags,
        type=__ret__.type,
        workspace_arm_path=__ret__.workspace_arm_path)
