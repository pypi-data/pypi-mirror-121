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
    'GetNamespaceNetworkRuleSetResult',
    'AwaitableGetNamespaceNetworkRuleSetResult',
    'get_namespace_network_rule_set',
]

@pulumi.output_type
class GetNamespaceNetworkRuleSetResult:
    """
    Description of topic resource.
    """
    def __init__(__self__, default_action=None, id=None, ip_rules=None, name=None, system_data=None, trusted_service_access_enabled=None, type=None, virtual_network_rules=None):
        if default_action and not isinstance(default_action, str):
            raise TypeError("Expected argument 'default_action' to be a str")
        pulumi.set(__self__, "default_action", default_action)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_rules and not isinstance(ip_rules, list):
            raise TypeError("Expected argument 'ip_rules' to be a list")
        pulumi.set(__self__, "ip_rules", ip_rules)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if trusted_service_access_enabled and not isinstance(trusted_service_access_enabled, bool):
            raise TypeError("Expected argument 'trusted_service_access_enabled' to be a bool")
        pulumi.set(__self__, "trusted_service_access_enabled", trusted_service_access_enabled)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if virtual_network_rules and not isinstance(virtual_network_rules, list):
            raise TypeError("Expected argument 'virtual_network_rules' to be a list")
        pulumi.set(__self__, "virtual_network_rules", virtual_network_rules)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> Optional[str]:
        """
        Default Action for Network Rule Set
        """
        return pulumi.get(self, "default_action")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipRules")
    def ip_rules(self) -> Optional[Sequence['outputs.NWRuleSetIpRulesResponse']]:
        """
        List of IpRules
        """
        return pulumi.get(self, "ip_rules")

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
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="trustedServiceAccessEnabled")
    def trusted_service_access_enabled(self) -> Optional[bool]:
        """
        Value that indicates whether Trusted Service Access is Enabled or not.
        """
        return pulumi.get(self, "trusted_service_access_enabled")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> Optional[Sequence['outputs.NWRuleSetVirtualNetworkRulesResponse']]:
        """
        List VirtualNetwork Rules
        """
        return pulumi.get(self, "virtual_network_rules")


class AwaitableGetNamespaceNetworkRuleSetResult(GetNamespaceNetworkRuleSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamespaceNetworkRuleSetResult(
            default_action=self.default_action,
            id=self.id,
            ip_rules=self.ip_rules,
            name=self.name,
            system_data=self.system_data,
            trusted_service_access_enabled=self.trusted_service_access_enabled,
            type=self.type,
            virtual_network_rules=self.virtual_network_rules)


def get_namespace_network_rule_set(namespace_name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamespaceNetworkRuleSetResult:
    """
    Description of topic resource.


    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    __args__ = dict()
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:eventhub/v20210101preview:getNamespaceNetworkRuleSet', __args__, opts=opts, typ=GetNamespaceNetworkRuleSetResult).value

    return AwaitableGetNamespaceNetworkRuleSetResult(
        default_action=__ret__.default_action,
        id=__ret__.id,
        ip_rules=__ret__.ip_rules,
        name=__ret__.name,
        system_data=__ret__.system_data,
        trusted_service_access_enabled=__ret__.trusted_service_access_enabled,
        type=__ret__.type,
        virtual_network_rules=__ret__.virtual_network_rules)
