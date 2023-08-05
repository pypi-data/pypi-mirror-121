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
    'GetPolicyResult',
    'AwaitableGetPolicyResult',
    'get_policy',
]

@pulumi.output_type
class GetPolicyResult:
    """
    Defines web application firewall policy for Azure CDN.
    """
    def __init__(__self__, custom_rules=None, endpoint_links=None, etag=None, id=None, location=None, managed_rules=None, name=None, policy_settings=None, provisioning_state=None, rate_limit_rules=None, resource_state=None, sku=None, system_data=None, tags=None, type=None):
        if custom_rules and not isinstance(custom_rules, dict):
            raise TypeError("Expected argument 'custom_rules' to be a dict")
        pulumi.set(__self__, "custom_rules", custom_rules)
        if endpoint_links and not isinstance(endpoint_links, list):
            raise TypeError("Expected argument 'endpoint_links' to be a list")
        pulumi.set(__self__, "endpoint_links", endpoint_links)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_rules and not isinstance(managed_rules, dict):
            raise TypeError("Expected argument 'managed_rules' to be a dict")
        pulumi.set(__self__, "managed_rules", managed_rules)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if policy_settings and not isinstance(policy_settings, dict):
            raise TypeError("Expected argument 'policy_settings' to be a dict")
        pulumi.set(__self__, "policy_settings", policy_settings)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if rate_limit_rules and not isinstance(rate_limit_rules, dict):
            raise TypeError("Expected argument 'rate_limit_rules' to be a dict")
        pulumi.set(__self__, "rate_limit_rules", rate_limit_rules)
        if resource_state and not isinstance(resource_state, str):
            raise TypeError("Expected argument 'resource_state' to be a str")
        pulumi.set(__self__, "resource_state", resource_state)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="customRules")
    def custom_rules(self) -> Optional['outputs.CustomRuleListResponse']:
        """
        Describes custom rules inside the policy.
        """
        return pulumi.get(self, "custom_rules")

    @property
    @pulumi.getter(name="endpointLinks")
    def endpoint_links(self) -> Sequence['outputs.CdnEndpointResponse']:
        """
        Describes Azure CDN endpoints associated with this Web Application Firewall policy.
        """
        return pulumi.get(self, "endpoint_links")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
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
    def location(self) -> str:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedRules")
    def managed_rules(self) -> Optional['outputs.ManagedRuleSetListResponse']:
        """
        Describes managed rules inside the policy.
        """
        return pulumi.get(self, "managed_rules")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policySettings")
    def policy_settings(self) -> Optional['outputs.PolicySettingsResponse']:
        """
        Describes  policySettings for policy
        """
        return pulumi.get(self, "policy_settings")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the WebApplicationFirewallPolicy.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="rateLimitRules")
    def rate_limit_rules(self) -> Optional['outputs.RateLimitRuleListResponse']:
        """
        Describes rate limit rules inside the policy.
        """
        return pulumi.get(self, "rate_limit_rules")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> str:
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        The pricing tier (defines a CDN provider, feature list and rate) of the CdnWebApplicationFirewallPolicy.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Read only system data
        """
        return pulumi.get(self, "system_data")

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
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetPolicyResult(GetPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyResult(
            custom_rules=self.custom_rules,
            endpoint_links=self.endpoint_links,
            etag=self.etag,
            id=self.id,
            location=self.location,
            managed_rules=self.managed_rules,
            name=self.name,
            policy_settings=self.policy_settings,
            provisioning_state=self.provisioning_state,
            rate_limit_rules=self.rate_limit_rules,
            resource_state=self.resource_state,
            sku=self.sku,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_policy(policy_name: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyResult:
    """
    Defines web application firewall policy for Azure CDN.


    :param str policy_name: The name of the CdnWebApplicationFirewallPolicy.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['policyName'] = policy_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:cdn/v20200901:getPolicy', __args__, opts=opts, typ=GetPolicyResult).value

    return AwaitableGetPolicyResult(
        custom_rules=__ret__.custom_rules,
        endpoint_links=__ret__.endpoint_links,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        managed_rules=__ret__.managed_rules,
        name=__ret__.name,
        policy_settings=__ret__.policy_settings,
        provisioning_state=__ret__.provisioning_state,
        rate_limit_rules=__ret__.rate_limit_rules,
        resource_state=__ret__.resource_state,
        sku=__ret__.sku,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)
