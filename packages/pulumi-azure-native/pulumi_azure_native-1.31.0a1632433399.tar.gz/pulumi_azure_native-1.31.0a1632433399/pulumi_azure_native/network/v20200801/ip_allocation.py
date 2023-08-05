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

__all__ = ['IpAllocationArgs', 'IpAllocation']

@pulumi.input_type
class IpAllocationArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 allocation_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_allocation_name: Optional[pulumi.Input[str]] = None,
                 ipam_allocation_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None,
                 prefix_length: Optional[pulumi.Input[int]] = None,
                 prefix_type: Optional[pulumi.Input[Union[str, 'IPVersion']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[Union[str, 'IpAllocationType']]] = None):
        """
        The set of arguments for constructing a IpAllocation resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] allocation_tags: IpAllocation tags.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] ip_allocation_name: The name of the IpAllocation.
        :param pulumi.Input[str] ipam_allocation_id: The IPAM allocation ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] prefix: The address prefix for the IpAllocation.
        :param pulumi.Input[int] prefix_length: The address prefix length for the IpAllocation.
        :param pulumi.Input[Union[str, 'IPVersion']] prefix_type: The address prefix Type for the IpAllocation.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Union[str, 'IpAllocationType']] type: The type for the IpAllocation.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if allocation_tags is not None:
            pulumi.set(__self__, "allocation_tags", allocation_tags)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ip_allocation_name is not None:
            pulumi.set(__self__, "ip_allocation_name", ip_allocation_name)
        if ipam_allocation_id is not None:
            pulumi.set(__self__, "ipam_allocation_id", ipam_allocation_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)
        if prefix_length is None:
            prefix_length = 0
        if prefix_length is not None:
            pulumi.set(__self__, "prefix_length", prefix_length)
        if prefix_type is not None:
            pulumi.set(__self__, "prefix_type", prefix_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

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
    @pulumi.getter(name="allocationTags")
    def allocation_tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        IpAllocation tags.
        """
        return pulumi.get(self, "allocation_tags")

    @allocation_tags.setter
    def allocation_tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "allocation_tags", value)

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
    @pulumi.getter(name="ipAllocationName")
    def ip_allocation_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the IpAllocation.
        """
        return pulumi.get(self, "ip_allocation_name")

    @ip_allocation_name.setter
    def ip_allocation_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_allocation_name", value)

    @property
    @pulumi.getter(name="ipamAllocationId")
    def ipam_allocation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The IPAM allocation ID.
        """
        return pulumi.get(self, "ipam_allocation_id")

    @ipam_allocation_id.setter
    def ipam_allocation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipam_allocation_id", value)

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
    def prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The address prefix for the IpAllocation.
        """
        return pulumi.get(self, "prefix")

    @prefix.setter
    def prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prefix", value)

    @property
    @pulumi.getter(name="prefixLength")
    def prefix_length(self) -> Optional[pulumi.Input[int]]:
        """
        The address prefix length for the IpAllocation.
        """
        return pulumi.get(self, "prefix_length")

    @prefix_length.setter
    def prefix_length(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "prefix_length", value)

    @property
    @pulumi.getter(name="prefixType")
    def prefix_type(self) -> Optional[pulumi.Input[Union[str, 'IPVersion']]]:
        """
        The address prefix Type for the IpAllocation.
        """
        return pulumi.get(self, "prefix_type")

    @prefix_type.setter
    def prefix_type(self, value: Optional[pulumi.Input[Union[str, 'IPVersion']]]):
        pulumi.set(self, "prefix_type", value)

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
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'IpAllocationType']]]:
        """
        The type for the IpAllocation.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'IpAllocationType']]]):
        pulumi.set(self, "type", value)


class IpAllocation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocation_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_allocation_name: Optional[pulumi.Input[str]] = None,
                 ipam_allocation_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None,
                 prefix_length: Optional[pulumi.Input[int]] = None,
                 prefix_type: Optional[pulumi.Input[Union[str, 'IPVersion']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[Union[str, 'IpAllocationType']]] = None,
                 __props__=None):
        """
        IpAllocation resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] allocation_tags: IpAllocation tags.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] ip_allocation_name: The name of the IpAllocation.
        :param pulumi.Input[str] ipam_allocation_id: The IPAM allocation ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] prefix: The address prefix for the IpAllocation.
        :param pulumi.Input[int] prefix_length: The address prefix length for the IpAllocation.
        :param pulumi.Input[Union[str, 'IPVersion']] prefix_type: The address prefix Type for the IpAllocation.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Union[str, 'IpAllocationType']] type: The type for the IpAllocation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IpAllocationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        IpAllocation resource.

        :param str resource_name: The name of the resource.
        :param IpAllocationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IpAllocationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocation_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_allocation_name: Optional[pulumi.Input[str]] = None,
                 ipam_allocation_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None,
                 prefix_length: Optional[pulumi.Input[int]] = None,
                 prefix_type: Optional[pulumi.Input[Union[str, 'IPVersion']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[Union[str, 'IpAllocationType']]] = None,
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
            __props__ = IpAllocationArgs.__new__(IpAllocationArgs)

            __props__.__dict__["allocation_tags"] = allocation_tags
            __props__.__dict__["id"] = id
            __props__.__dict__["ip_allocation_name"] = ip_allocation_name
            __props__.__dict__["ipam_allocation_id"] = ipam_allocation_id
            __props__.__dict__["location"] = location
            __props__.__dict__["prefix"] = prefix
            if prefix_length is None:
                prefix_length = 0
            __props__.__dict__["prefix_length"] = prefix_length
            __props__.__dict__["prefix_type"] = prefix_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["subnet"] = None
            __props__.__dict__["virtual_network"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/v20200801:IpAllocation"), pulumi.Alias(type_="azure-native:network:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20200301:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20200301:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20200401:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20200401:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20200501:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20200501:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20200601:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20200601:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20200701:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20200701:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20201101:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20201101:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20210201:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20210201:IpAllocation"), pulumi.Alias(type_="azure-native:network/v20210301:IpAllocation"), pulumi.Alias(type_="azure-nextgen:network/v20210301:IpAllocation")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(IpAllocation, __self__).__init__(
            'azure-native:network/v20200801:IpAllocation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'IpAllocation':
        """
        Get an existing IpAllocation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IpAllocationArgs.__new__(IpAllocationArgs)

        __props__.__dict__["allocation_tags"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["ipam_allocation_id"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["prefix"] = None
        __props__.__dict__["prefix_length"] = None
        __props__.__dict__["prefix_type"] = None
        __props__.__dict__["subnet"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["virtual_network"] = None
        return IpAllocation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allocationTags")
    def allocation_tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        IpAllocation tags.
        """
        return pulumi.get(self, "allocation_tags")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="ipamAllocationId")
    def ipam_allocation_id(self) -> pulumi.Output[Optional[str]]:
        """
        The IPAM allocation ID.
        """
        return pulumi.get(self, "ipam_allocation_id")

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
    @pulumi.getter
    def prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The address prefix for the IpAllocation.
        """
        return pulumi.get(self, "prefix")

    @property
    @pulumi.getter(name="prefixLength")
    def prefix_length(self) -> pulumi.Output[Optional[int]]:
        """
        The address prefix length for the IpAllocation.
        """
        return pulumi.get(self, "prefix_length")

    @property
    @pulumi.getter(name="prefixType")
    def prefix_type(self) -> pulumi.Output[Optional[str]]:
        """
        The address prefix Type for the IpAllocation.
        """
        return pulumi.get(self, "prefix_type")

    @property
    @pulumi.getter
    def subnet(self) -> pulumi.Output['outputs.SubResourceResponse']:
        """
        The Subnet that using the prefix of this IpAllocation resource.
        """
        return pulumi.get(self, "subnet")

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

    @property
    @pulumi.getter(name="virtualNetwork")
    def virtual_network(self) -> pulumi.Output['outputs.SubResourceResponse']:
        """
        The VirtualNetwork that using the prefix of this IpAllocation resource.
        """
        return pulumi.get(self, "virtual_network")

