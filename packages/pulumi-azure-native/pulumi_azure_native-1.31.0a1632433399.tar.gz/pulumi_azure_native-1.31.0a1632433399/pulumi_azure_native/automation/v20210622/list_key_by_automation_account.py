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
    'ListKeyByAutomationAccountResult',
    'AwaitableListKeyByAutomationAccountResult',
    'list_key_by_automation_account',
]

@pulumi.output_type
class ListKeyByAutomationAccountResult:
    def __init__(__self__, keys=None):
        if keys and not isinstance(keys, list):
            raise TypeError("Expected argument 'keys' to be a list")
        pulumi.set(__self__, "keys", keys)

    @property
    @pulumi.getter
    def keys(self) -> Optional[Sequence['outputs.KeyResponse']]:
        """
        Lists the automation keys.
        """
        return pulumi.get(self, "keys")


class AwaitableListKeyByAutomationAccountResult(ListKeyByAutomationAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListKeyByAutomationAccountResult(
            keys=self.keys)


def list_key_by_automation_account(automation_account_name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListKeyByAutomationAccountResult:
    """
    Use this data source to access information about an existing resource.

    :param str automation_account_name: The name of the automation account.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['automationAccountName'] = automation_account_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:automation/v20210622:listKeyByAutomationAccount', __args__, opts=opts, typ=ListKeyByAutomationAccountResult).value

    return AwaitableListKeyByAutomationAccountResult(
        keys=__ret__.keys)
