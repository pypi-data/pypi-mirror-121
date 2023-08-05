# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PrivateDnsZoneGroupArgs', 'PrivateDnsZoneGroup']

@pulumi.input_type
class PrivateDnsZoneGroupArgs:
    def __init__(__self__, *,
                 private_endpoint_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_dns_zone_configs: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateDnsZoneConfigArgs']]]] = None,
                 private_dns_zone_group_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PrivateDnsZoneGroup resource.
        :param pulumi.Input[str] private_endpoint_name: The name of the private endpoint.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: Name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[Sequence[pulumi.Input['PrivateDnsZoneConfigArgs']]] private_dns_zone_configs: A collection of private dns zone configurations of the private dns zone group.
        :param pulumi.Input[str] private_dns_zone_group_name: The name of the private dns zone group.
        """
        pulumi.set(__self__, "private_endpoint_name", private_endpoint_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_dns_zone_configs is not None:
            pulumi.set(__self__, "private_dns_zone_configs", private_dns_zone_configs)
        if private_dns_zone_group_name is not None:
            pulumi.set(__self__, "private_dns_zone_group_name", private_dns_zone_group_name)

    @property
    @pulumi.getter(name="privateEndpointName")
    def private_endpoint_name(self) -> pulumi.Input[str]:
        """
        The name of the private endpoint.
        """
        return pulumi.get(self, "private_endpoint_name")

    @private_endpoint_name.setter
    def private_endpoint_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "private_endpoint_name", value)

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
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateDnsZoneConfigs")
    def private_dns_zone_configs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivateDnsZoneConfigArgs']]]]:
        """
        A collection of private dns zone configurations of the private dns zone group.
        """
        return pulumi.get(self, "private_dns_zone_configs")

    @private_dns_zone_configs.setter
    def private_dns_zone_configs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateDnsZoneConfigArgs']]]]):
        pulumi.set(self, "private_dns_zone_configs", value)

    @property
    @pulumi.getter(name="privateDnsZoneGroupName")
    def private_dns_zone_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the private dns zone group.
        """
        return pulumi.get(self, "private_dns_zone_group_name")

    @private_dns_zone_group_name.setter
    def private_dns_zone_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_dns_zone_group_name", value)


class PrivateDnsZoneGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_dns_zone_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateDnsZoneConfigArgs']]]]] = None,
                 private_dns_zone_group_name: Optional[pulumi.Input[str]] = None,
                 private_endpoint_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Private dns zone group resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: Name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateDnsZoneConfigArgs']]]] private_dns_zone_configs: A collection of private dns zone configurations of the private dns zone group.
        :param pulumi.Input[str] private_dns_zone_group_name: The name of the private dns zone group.
        :param pulumi.Input[str] private_endpoint_name: The name of the private endpoint.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateDnsZoneGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Private dns zone group resource.

        :param str resource_name: The name of the resource.
        :param PrivateDnsZoneGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateDnsZoneGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_dns_zone_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateDnsZoneConfigArgs']]]]] = None,
                 private_dns_zone_group_name: Optional[pulumi.Input[str]] = None,
                 private_endpoint_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = PrivateDnsZoneGroupArgs.__new__(PrivateDnsZoneGroupArgs)

            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            __props__.__dict__["private_dns_zone_configs"] = private_dns_zone_configs
            __props__.__dict__["private_dns_zone_group_name"] = private_dns_zone_group_name
            if private_endpoint_name is None and not opts.urn:
                raise TypeError("Missing required property 'private_endpoint_name'")
            __props__.__dict__["private_endpoint_name"] = private_endpoint_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["provisioning_state"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/v20200601:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20200301:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20200301:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20200401:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20200401:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20200501:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20200501:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20200701:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20200701:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20200801:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20200801:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20201101:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20201101:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20210201:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20210201:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-native:network/v20210301:PrivateDnsZoneGroup"), pulumi.Alias(type_="azure-nextgen:network/v20210301:PrivateDnsZoneGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateDnsZoneGroup, __self__).__init__(
            'azure-native:network/v20200601:PrivateDnsZoneGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrivateDnsZoneGroup':
        """
        Get an existing PrivateDnsZoneGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PrivateDnsZoneGroupArgs.__new__(PrivateDnsZoneGroupArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["private_dns_zone_configs"] = None
        __props__.__dict__["provisioning_state"] = None
        return PrivateDnsZoneGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateDnsZoneConfigs")
    def private_dns_zone_configs(self) -> pulumi.Output[Optional[Sequence['outputs.PrivateDnsZoneConfigResponse']]]:
        """
        A collection of private dns zone configurations of the private dns zone group.
        """
        return pulumi.get(self, "private_dns_zone_configs")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the private dns zone group resource.
        """
        return pulumi.get(self, "provisioning_state")

