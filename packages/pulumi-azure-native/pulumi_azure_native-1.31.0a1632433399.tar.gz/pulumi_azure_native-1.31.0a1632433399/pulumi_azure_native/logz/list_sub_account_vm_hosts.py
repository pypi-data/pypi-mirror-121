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
    'ListSubAccountVMHostsResult',
    'AwaitableListSubAccountVMHostsResult',
    'list_sub_account_vm_hosts',
]

@pulumi.output_type
class ListSubAccountVMHostsResult:
    """
    Response of a list VM Host Update Operation.
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
    def next_link(self) -> Optional[str]:
        """
        Link to the next set of results, if any.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.VMResourcesResponse']]:
        """
        Response of a list vm host update operation.
        """
        return pulumi.get(self, "value")


class AwaitableListSubAccountVMHostsResult(ListSubAccountVMHostsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListSubAccountVMHostsResult(
            next_link=self.next_link,
            value=self.value)


def list_sub_account_vm_hosts(monitor_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              sub_account_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListSubAccountVMHostsResult:
    """
    Response of a list VM Host Update Operation.
    API Version: 2020-10-01.


    :param str monitor_name: Monitor resource name
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sub_account_name: Sub Account resource name
    """
    __args__ = dict()
    __args__['monitorName'] = monitor_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['subAccountName'] = sub_account_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:logz:listSubAccountVMHosts', __args__, opts=opts, typ=ListSubAccountVMHostsResult).value

    return AwaitableListSubAccountVMHostsResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
