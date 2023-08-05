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
    'GetUserRuleResult',
    'AwaitableGetUserRuleResult',
    'get_user_rule',
]

warnings.warn("""Please use one of the variants: DefaultUserRule, UserRule.""", DeprecationWarning)

@pulumi.output_type
class GetUserRuleResult:
    """
    Network base rule.
    """
    def __init__(__self__, etag=None, id=None, kind=None, name=None, system_data=None, type=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Whether the rule is custom or default.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

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


class AwaitableGetUserRuleResult(GetUserRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserRuleResult(
            etag=self.etag,
            id=self.id,
            kind=self.kind,
            name=self.name,
            system_data=self.system_data,
            type=self.type)


def get_user_rule(configuration_name: Optional[str] = None,
                  network_manager_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  rule_collection_name: Optional[str] = None,
                  rule_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserRuleResult:
    """
    Network base rule.
    API Version: 2021-02-01-preview.


    :param str configuration_name: The name of the network manager security Configuration.
    :param str network_manager_name: The name of the network manager.
    :param str resource_group_name: The name of the resource group.
    :param str rule_collection_name: The name of the network manager security Configuration rule collection.
    :param str rule_name: The name of the rule.
    """
    pulumi.log.warn("""get_user_rule is deprecated: Please use one of the variants: DefaultUserRule, UserRule.""")
    __args__ = dict()
    __args__['configurationName'] = configuration_name
    __args__['networkManagerName'] = network_manager_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleCollectionName'] = rule_collection_name
    __args__['ruleName'] = rule_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network:getUserRule', __args__, opts=opts, typ=GetUserRuleResult).value

    return AwaitableGetUserRuleResult(
        etag=__ret__.etag,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        system_data=__ret__.system_data,
        type=__ret__.type)
