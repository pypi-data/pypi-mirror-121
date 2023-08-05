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
    'ListSourceControlRepositoriesResult',
    'AwaitableListSourceControlRepositoriesResult',
    'list_source_control_repositories',
]

@pulumi.output_type
class ListSourceControlRepositoriesResult:
    """
    List all the source controls.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> str:
        """
        URL to fetch the next set of repositories.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.RepoResponse']:
        """
        Array of repositories.
        """
        return pulumi.get(self, "value")


class AwaitableListSourceControlRepositoriesResult(ListSourceControlRepositoriesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListSourceControlRepositoriesResult(
            next_link=self.next_link,
            value=self.value)


def list_source_control_repositories(operational_insights_resource_provider: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     workspace_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListSourceControlRepositoriesResult:
    """
    List all the source controls.


    :param str operational_insights_resource_provider: The namespace of workspaces resource provider- Microsoft.OperationalInsights.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['operationalInsightsResourceProvider'] = operational_insights_resource_provider
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20210301preview:listSourceControlRepositories', __args__, opts=opts, typ=ListSourceControlRepositoriesResult).value

    return AwaitableListSourceControlRepositoriesResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
