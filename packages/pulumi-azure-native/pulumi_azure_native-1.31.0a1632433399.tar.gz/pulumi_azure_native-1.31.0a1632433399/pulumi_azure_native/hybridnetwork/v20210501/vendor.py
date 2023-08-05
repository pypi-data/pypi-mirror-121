# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = ['VendorArgs', 'Vendor']

@pulumi.input_type
class VendorArgs:
    def __init__(__self__, *,
                 vendor_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Vendor resource.
        :param pulumi.Input[str] vendor_name: The name of the vendor.
        """
        if vendor_name is not None:
            pulumi.set(__self__, "vendor_name", vendor_name)

    @property
    @pulumi.getter(name="vendorName")
    def vendor_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the vendor.
        """
        return pulumi.get(self, "vendor_name")

    @vendor_name.setter
    def vendor_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vendor_name", value)


class Vendor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 vendor_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Vendor resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] vendor_name: The name of the vendor.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[VendorArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Vendor resource.

        :param str resource_name: The name of the resource.
        :param VendorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VendorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 vendor_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = VendorArgs.__new__(VendorArgs)

            __props__.__dict__["vendor_name"] = vendor_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["skus"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:hybridnetwork/v20210501:Vendor"), pulumi.Alias(type_="azure-native:hybridnetwork:Vendor"), pulumi.Alias(type_="azure-nextgen:hybridnetwork:Vendor"), pulumi.Alias(type_="azure-native:hybridnetwork/v20200101preview:Vendor"), pulumi.Alias(type_="azure-nextgen:hybridnetwork/v20200101preview:Vendor")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Vendor, __self__).__init__(
            'azure-native:hybridnetwork/v20210501:Vendor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Vendor':
        """
        Get an existing Vendor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VendorArgs.__new__(VendorArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["skus"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return Vendor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the vendor resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def skus(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        A list of IDs of the vendor skus offered by the vendor.
        """
        return pulumi.get(self, "skus")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

