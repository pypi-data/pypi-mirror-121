# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['VirtualNetworkTapInitArgs', 'VirtualNetworkTap']

@pulumi.input_type
class VirtualNetworkTapInitArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 destination_load_balancer_front_end_ip_configuration: Optional[pulumi.Input['FrontendIPConfigurationArgs']] = None,
                 destination_network_interface_ip_configuration: Optional[pulumi.Input['NetworkInterfaceIPConfigurationArgs']] = None,
                 destination_port: Optional[pulumi.Input[int]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tap_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a VirtualNetworkTap resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['FrontendIPConfigurationArgs'] destination_load_balancer_front_end_ip_configuration: The reference to the private IP address on the internal Load Balancer that will receive the tap.
        :param pulumi.Input['NetworkInterfaceIPConfigurationArgs'] destination_network_interface_ip_configuration: The reference to the private IP Address of the collector nic that will receive the tap.
        :param pulumi.Input[int] destination_port: The VXLAN destination port that will receive the tapped traffic.
        :param pulumi.Input[str] etag: Gets a unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] tap_name: The name of the virtual network tap.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if destination_load_balancer_front_end_ip_configuration is not None:
            pulumi.set(__self__, "destination_load_balancer_front_end_ip_configuration", destination_load_balancer_front_end_ip_configuration)
        if destination_network_interface_ip_configuration is not None:
            pulumi.set(__self__, "destination_network_interface_ip_configuration", destination_network_interface_ip_configuration)
        if destination_port is not None:
            pulumi.set(__self__, "destination_port", destination_port)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tap_name is not None:
            pulumi.set(__self__, "tap_name", tap_name)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="destinationLoadBalancerFrontEndIPConfiguration")
    def destination_load_balancer_front_end_ip_configuration(self) -> Optional[pulumi.Input['FrontendIPConfigurationArgs']]:
        """
        The reference to the private IP address on the internal Load Balancer that will receive the tap.
        """
        return pulumi.get(self, "destination_load_balancer_front_end_ip_configuration")

    @destination_load_balancer_front_end_ip_configuration.setter
    def destination_load_balancer_front_end_ip_configuration(self, value: Optional[pulumi.Input['FrontendIPConfigurationArgs']]):
        pulumi.set(self, "destination_load_balancer_front_end_ip_configuration", value)

    @property
    @pulumi.getter(name="destinationNetworkInterfaceIPConfiguration")
    def destination_network_interface_ip_configuration(self) -> Optional[pulumi.Input['NetworkInterfaceIPConfigurationArgs']]:
        """
        The reference to the private IP Address of the collector nic that will receive the tap.
        """
        return pulumi.get(self, "destination_network_interface_ip_configuration")

    @destination_network_interface_ip_configuration.setter
    def destination_network_interface_ip_configuration(self, value: Optional[pulumi.Input['NetworkInterfaceIPConfigurationArgs']]):
        pulumi.set(self, "destination_network_interface_ip_configuration", value)

    @property
    @pulumi.getter(name="destinationPort")
    def destination_port(self) -> Optional[pulumi.Input[int]]:
        """
        The VXLAN destination port that will receive the tapped traffic.
        """
        return pulumi.get(self, "destination_port")

    @destination_port.setter
    def destination_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "destination_port", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tapName")
    def tap_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the virtual network tap.
        """
        return pulumi.get(self, "tap_name")

    @tap_name.setter
    def tap_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tap_name", value)


class VirtualNetworkTap(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_load_balancer_front_end_ip_configuration: Optional[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]] = None,
                 destination_network_interface_ip_configuration: Optional[pulumi.Input[pulumi.InputType['NetworkInterfaceIPConfigurationArgs']]] = None,
                 destination_port: Optional[pulumi.Input[int]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tap_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Virtual Network Tap resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']] destination_load_balancer_front_end_ip_configuration: The reference to the private IP address on the internal Load Balancer that will receive the tap.
        :param pulumi.Input[pulumi.InputType['NetworkInterfaceIPConfigurationArgs']] destination_network_interface_ip_configuration: The reference to the private IP Address of the collector nic that will receive the tap.
        :param pulumi.Input[int] destination_port: The VXLAN destination port that will receive the tapped traffic.
        :param pulumi.Input[str] etag: Gets a unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] tap_name: The name of the virtual network tap.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualNetworkTapInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Virtual Network Tap resource.

        :param str resource_name: The name of the resource.
        :param VirtualNetworkTapInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualNetworkTapInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_load_balancer_front_end_ip_configuration: Optional[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]] = None,
                 destination_network_interface_ip_configuration: Optional[pulumi.Input[pulumi.InputType['NetworkInterfaceIPConfigurationArgs']]] = None,
                 destination_port: Optional[pulumi.Input[int]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tap_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VirtualNetworkTapInitArgs.__new__(VirtualNetworkTapInitArgs)

            __props__.__dict__["destination_load_balancer_front_end_ip_configuration"] = destination_load_balancer_front_end_ip_configuration
            __props__.__dict__["destination_network_interface_ip_configuration"] = destination_network_interface_ip_configuration
            __props__.__dict__["destination_port"] = destination_port
            __props__.__dict__["etag"] = etag
            __props__.__dict__["id"] = id
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tap_name"] = tap_name
            __props__.__dict__["name"] = None
            __props__.__dict__["network_interface_tap_configurations"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_guid"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/v20190401:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20180801:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20180801:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20181001:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20181001:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20181101:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20181101:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20181201:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20181201:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20190201:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20190201:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20190601:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20190601:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20190701:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20190701:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20190801:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20190801:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20190901:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20190901:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20191101:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20191101:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20191201:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20191201:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20200301:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20200301:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20200401:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20200401:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20200501:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20200501:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20200601:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20200601:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20200701:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20200701:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20200801:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20200801:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20201101:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20201101:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20210201:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20210201:VirtualNetworkTap"), pulumi.Alias(type_="azure-native:network/v20210301:VirtualNetworkTap"), pulumi.Alias(type_="azure-nextgen:network/v20210301:VirtualNetworkTap")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualNetworkTap, __self__).__init__(
            'azure-native:network/v20190401:VirtualNetworkTap',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualNetworkTap':
        """
        Get an existing VirtualNetworkTap resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VirtualNetworkTapInitArgs.__new__(VirtualNetworkTapInitArgs)

        __props__.__dict__["destination_load_balancer_front_end_ip_configuration"] = None
        __props__.__dict__["destination_network_interface_ip_configuration"] = None
        __props__.__dict__["destination_port"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_interface_tap_configurations"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_guid"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return VirtualNetworkTap(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="destinationLoadBalancerFrontEndIPConfiguration")
    def destination_load_balancer_front_end_ip_configuration(self) -> pulumi.Output[Optional['outputs.FrontendIPConfigurationResponse']]:
        """
        The reference to the private IP address on the internal Load Balancer that will receive the tap.
        """
        return pulumi.get(self, "destination_load_balancer_front_end_ip_configuration")

    @property
    @pulumi.getter(name="destinationNetworkInterfaceIPConfiguration")
    def destination_network_interface_ip_configuration(self) -> pulumi.Output[Optional['outputs.NetworkInterfaceIPConfigurationResponse']]:
        """
        The reference to the private IP Address of the collector nic that will receive the tap.
        """
        return pulumi.get(self, "destination_network_interface_ip_configuration")

    @property
    @pulumi.getter(name="destinationPort")
    def destination_port(self) -> pulumi.Output[Optional[int]]:
        """
        The VXLAN destination port that will receive the tapped traffic.
        """
        return pulumi.get(self, "destination_port")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaceTapConfigurations")
    def network_interface_tap_configurations(self) -> pulumi.Output[Sequence['outputs.NetworkInterfaceTapConfigurationResponse']]:
        """
        Specifies the list of resource IDs for the network interface IP configuration that needs to be tapped.
        """
        return pulumi.get(self, "network_interface_tap_configurations")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the virtual network tap. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resourceGuid property of the virtual network tap.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

