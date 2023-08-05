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
    'ListRemediationDeploymentsAtResourceResult',
    'AwaitableListRemediationDeploymentsAtResourceResult',
    'list_remediation_deployments_at_resource',
]

@pulumi.output_type
class ListRemediationDeploymentsAtResourceResult:
    """
    List of deployments for a remediation.
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
        The URL to get the next set of results.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.RemediationDeploymentResponse']:
        """
        Array of deployments for the remediation.
        """
        return pulumi.get(self, "value")


class AwaitableListRemediationDeploymentsAtResourceResult(ListRemediationDeploymentsAtResourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListRemediationDeploymentsAtResourceResult(
            next_link=self.next_link,
            value=self.value)


def list_remediation_deployments_at_resource(remediation_name: Optional[str] = None,
                                             resource_id: Optional[str] = None,
                                             top: Optional[int] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListRemediationDeploymentsAtResourceResult:
    """
    List of deployments for a remediation.


    :param str remediation_name: The name of the remediation.
    :param str resource_id: Resource ID.
    :param int top: Maximum number of records to return.
    """
    __args__ = dict()
    __args__['remediationName'] = remediation_name
    __args__['resourceId'] = resource_id
    __args__['top'] = top
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:policyinsights/v20180701preview:listRemediationDeploymentsAtResource', __args__, opts=opts, typ=ListRemediationDeploymentsAtResourceResult).value

    return AwaitableListRemediationDeploymentsAtResourceResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
