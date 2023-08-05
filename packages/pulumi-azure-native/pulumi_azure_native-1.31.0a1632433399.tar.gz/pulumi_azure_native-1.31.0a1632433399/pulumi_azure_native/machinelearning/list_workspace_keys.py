# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ListWorkspaceKeysResult',
    'AwaitableListWorkspaceKeysResult',
    'list_workspace_keys',
]

@pulumi.output_type
class ListWorkspaceKeysResult:
    """
    Workspace authorization keys for a workspace.
    """
    def __init__(__self__, primary_token=None, secondary_token=None):
        if primary_token and not isinstance(primary_token, str):
            raise TypeError("Expected argument 'primary_token' to be a str")
        pulumi.set(__self__, "primary_token", primary_token)
        if secondary_token and not isinstance(secondary_token, str):
            raise TypeError("Expected argument 'secondary_token' to be a str")
        pulumi.set(__self__, "secondary_token", secondary_token)

    @property
    @pulumi.getter(name="primaryToken")
    def primary_token(self) -> Optional[str]:
        """
        Primary authorization key for this workspace.
        """
        return pulumi.get(self, "primary_token")

    @property
    @pulumi.getter(name="secondaryToken")
    def secondary_token(self) -> Optional[str]:
        """
        Secondary authorization key for this workspace.
        """
        return pulumi.get(self, "secondary_token")


class AwaitableListWorkspaceKeysResult(ListWorkspaceKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWorkspaceKeysResult(
            primary_token=self.primary_token,
            secondary_token=self.secondary_token)


def list_workspace_keys(resource_group_name: Optional[str] = None,
                        workspace_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWorkspaceKeysResult:
    """
    Workspace authorization keys for a workspace.
    API Version: 2016-04-01.


    :param str resource_group_name: The name of the resource group to which the machine learning workspace belongs.
    :param str workspace_name: The name of the machine learning workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:machinelearning:listWorkspaceKeys', __args__, opts=opts, typ=ListWorkspaceKeysResult).value

    return AwaitableListWorkspaceKeysResult(
        primary_token=__ret__.primary_token,
        secondary_token=__ret__.secondary_token)
