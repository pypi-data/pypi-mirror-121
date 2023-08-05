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
    'GetNetworkSecurityGroupResult',
    'AwaitableGetNetworkSecurityGroupResult',
    'get_network_security_group',
]

@pulumi.output_type
class GetNetworkSecurityGroupResult:
    """
    NetworkSecurityGroup resource.
    """
    def __init__(__self__, default_security_rules=None, etag=None, flow_logs=None, id=None, location=None, name=None, network_interfaces=None, provisioning_state=None, resource_guid=None, security_rules=None, subnets=None, tags=None, type=None):
        if default_security_rules and not isinstance(default_security_rules, list):
            raise TypeError("Expected argument 'default_security_rules' to be a list")
        pulumi.set(__self__, "default_security_rules", default_security_rules)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if flow_logs and not isinstance(flow_logs, list):
            raise TypeError("Expected argument 'flow_logs' to be a list")
        pulumi.set(__self__, "flow_logs", flow_logs)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_guid and not isinstance(resource_guid, str):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, "resource_guid", resource_guid)
        if security_rules and not isinstance(security_rules, list):
            raise TypeError("Expected argument 'security_rules' to be a list")
        pulumi.set(__self__, "security_rules", security_rules)
        if subnets and not isinstance(subnets, list):
            raise TypeError("Expected argument 'subnets' to be a list")
        pulumi.set(__self__, "subnets", subnets)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="defaultSecurityRules")
    def default_security_rules(self) -> Sequence['outputs.SecurityRuleResponse']:
        """
        The default security rules of network security group.
        """
        return pulumi.get(self, "default_security_rules")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="flowLogs")
    def flow_logs(self) -> Sequence['outputs.FlowLogResponse']:
        """
        A collection of references to flow log resources.
        """
        return pulumi.get(self, "flow_logs")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Sequence['outputs.NetworkInterfaceResponse']:
        """
        A collection of references to network interfaces.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the network security group resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> str:
        """
        The resource GUID property of the network security group resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter(name="securityRules")
    def security_rules(self) -> Optional[Sequence['outputs.SecurityRuleResponse']]:
        """
        A collection of security rules of the network security group.
        """
        return pulumi.get(self, "security_rules")

    @property
    @pulumi.getter
    def subnets(self) -> Sequence['outputs.SubnetResponse']:
        """
        A collection of references to subnets.
        """
        return pulumi.get(self, "subnets")

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


class AwaitableGetNetworkSecurityGroupResult(GetNetworkSecurityGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkSecurityGroupResult(
            default_security_rules=self.default_security_rules,
            etag=self.etag,
            flow_logs=self.flow_logs,
            id=self.id,
            location=self.location,
            name=self.name,
            network_interfaces=self.network_interfaces,
            provisioning_state=self.provisioning_state,
            resource_guid=self.resource_guid,
            security_rules=self.security_rules,
            subnets=self.subnets,
            tags=self.tags,
            type=self.type)


def get_network_security_group(expand: Optional[str] = None,
                               network_security_group_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkSecurityGroupResult:
    """
    NetworkSecurityGroup resource.
    API Version: 2020-11-01.


    :param str expand: Expands referenced resources.
    :param str network_security_group_name: The name of the network security group.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['networkSecurityGroupName'] = network_security_group_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network:getNetworkSecurityGroup', __args__, opts=opts, typ=GetNetworkSecurityGroupResult).value

    return AwaitableGetNetworkSecurityGroupResult(
        default_security_rules=__ret__.default_security_rules,
        etag=__ret__.etag,
        flow_logs=__ret__.flow_logs,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        network_interfaces=__ret__.network_interfaces,
        provisioning_state=__ret__.provisioning_state,
        resource_guid=__ret__.resource_guid,
        security_rules=__ret__.security_rules,
        subnets=__ret__.subnets,
        tags=__ret__.tags,
        type=__ret__.type)
