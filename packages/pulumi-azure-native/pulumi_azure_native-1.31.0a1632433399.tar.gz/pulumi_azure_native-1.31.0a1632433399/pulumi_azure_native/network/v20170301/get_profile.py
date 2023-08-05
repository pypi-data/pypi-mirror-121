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
    'GetProfileResult',
    'AwaitableGetProfileResult',
    'get_profile',
]

@pulumi.output_type
class GetProfileResult:
    """
    Class representing a Traffic Manager profile.
    """
    def __init__(__self__, dns_config=None, endpoints=None, id=None, location=None, monitor_config=None, name=None, profile_status=None, tags=None, traffic_routing_method=None, type=None):
        if dns_config and not isinstance(dns_config, dict):
            raise TypeError("Expected argument 'dns_config' to be a dict")
        pulumi.set(__self__, "dns_config", dns_config)
        if endpoints and not isinstance(endpoints, list):
            raise TypeError("Expected argument 'endpoints' to be a list")
        pulumi.set(__self__, "endpoints", endpoints)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if monitor_config and not isinstance(monitor_config, dict):
            raise TypeError("Expected argument 'monitor_config' to be a dict")
        pulumi.set(__self__, "monitor_config", monitor_config)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if profile_status and not isinstance(profile_status, str):
            raise TypeError("Expected argument 'profile_status' to be a str")
        pulumi.set(__self__, "profile_status", profile_status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if traffic_routing_method and not isinstance(traffic_routing_method, str):
            raise TypeError("Expected argument 'traffic_routing_method' to be a str")
        pulumi.set(__self__, "traffic_routing_method", traffic_routing_method)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dnsConfig")
    def dns_config(self) -> Optional['outputs.DnsConfigResponse']:
        """
        Gets or sets the DNS settings of the Traffic Manager profile.
        """
        return pulumi.get(self, "dns_config")

    @property
    @pulumi.getter
    def endpoints(self) -> Optional[Sequence['outputs.EndpointResponse']]:
        """
        Gets or sets the list of endpoints in the Traffic Manager profile.
        """
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="monitorConfig")
    def monitor_config(self) -> Optional['outputs.MonitorConfigResponse']:
        """
        Gets or sets the endpoint monitoring settings of the Traffic Manager profile.
        """
        return pulumi.get(self, "monitor_config")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="profileStatus")
    def profile_status(self) -> Optional[str]:
        """
        Gets or sets the status of the Traffic Manager profile.  Possible values are 'Enabled' and 'Disabled'.
        """
        return pulumi.get(self, "profile_status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trafficRoutingMethod")
    def traffic_routing_method(self) -> Optional[str]:
        """
        Gets or sets the traffic routing method of the Traffic Manager profile.  Possible values are 'Performance', 'Weighted', 'Priority' or 'Geographic'.
        """
        return pulumi.get(self, "traffic_routing_method")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetProfileResult(GetProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProfileResult(
            dns_config=self.dns_config,
            endpoints=self.endpoints,
            id=self.id,
            location=self.location,
            monitor_config=self.monitor_config,
            name=self.name,
            profile_status=self.profile_status,
            tags=self.tags,
            traffic_routing_method=self.traffic_routing_method,
            type=self.type)


def get_profile(profile_name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProfileResult:
    """
    Class representing a Traffic Manager profile.


    :param str profile_name: The name of the Traffic Manager profile.
    :param str resource_group_name: The name of the resource group containing the Traffic Manager profile.
    """
    __args__ = dict()
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20170301:getProfile', __args__, opts=opts, typ=GetProfileResult).value

    return AwaitableGetProfileResult(
        dns_config=__ret__.dns_config,
        endpoints=__ret__.endpoints,
        id=__ret__.id,
        location=__ret__.location,
        monitor_config=__ret__.monitor_config,
        name=__ret__.name,
        profile_status=__ret__.profile_status,
        tags=__ret__.tags,
        traffic_routing_method=__ret__.traffic_routing_method,
        type=__ret__.type)
