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

__all__ = ['NetworkVirtualApplianceArgs', 'NetworkVirtualAppliance']

@pulumi.input_type
class NetworkVirtualApplianceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 boot_strap_configuration_blob: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cloud_init_configuration_blob: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['ManagedServiceIdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_virtual_appliance_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['VirtualApplianceSkuPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_appliance_asn: Optional[pulumi.Input[float]] = None,
                 virtual_hub: Optional[pulumi.Input['SubResourceArgs']] = None):
        """
        The set of arguments for constructing a NetworkVirtualAppliance resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] boot_strap_configuration_blob: BootStrapConfigurationBlob storage URLs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] cloud_init_configuration_blob: CloudInitConfigurationBlob storage URLs.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: The service principal that has read access to cloud-init and config blob.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] network_virtual_appliance_name: The name of Network Virtual Appliance.
        :param pulumi.Input['VirtualApplianceSkuPropertiesArgs'] sku: Network Virtual Appliance SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[float] virtual_appliance_asn: VirtualAppliance ASN.
        :param pulumi.Input['SubResourceArgs'] virtual_hub: The Virtual Hub where Network Virtual Appliance is being deployed.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if boot_strap_configuration_blob is not None:
            pulumi.set(__self__, "boot_strap_configuration_blob", boot_strap_configuration_blob)
        if cloud_init_configuration_blob is not None:
            pulumi.set(__self__, "cloud_init_configuration_blob", cloud_init_configuration_blob)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_virtual_appliance_name is not None:
            pulumi.set(__self__, "network_virtual_appliance_name", network_virtual_appliance_name)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if virtual_appliance_asn is not None:
            pulumi.set(__self__, "virtual_appliance_asn", virtual_appliance_asn)
        if virtual_hub is not None:
            pulumi.set(__self__, "virtual_hub", virtual_hub)

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
    @pulumi.getter(name="bootStrapConfigurationBlob")
    def boot_strap_configuration_blob(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        BootStrapConfigurationBlob storage URLs.
        """
        return pulumi.get(self, "boot_strap_configuration_blob")

    @boot_strap_configuration_blob.setter
    def boot_strap_configuration_blob(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "boot_strap_configuration_blob", value)

    @property
    @pulumi.getter(name="cloudInitConfigurationBlob")
    def cloud_init_configuration_blob(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        CloudInitConfigurationBlob storage URLs.
        """
        return pulumi.get(self, "cloud_init_configuration_blob")

    @cloud_init_configuration_blob.setter
    def cloud_init_configuration_blob(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "cloud_init_configuration_blob", value)

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
    def identity(self) -> Optional[pulumi.Input['ManagedServiceIdentityArgs']]:
        """
        The service principal that has read access to cloud-init and config blob.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedServiceIdentityArgs']]):
        pulumi.set(self, "identity", value)

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
    @pulumi.getter(name="networkVirtualApplianceName")
    def network_virtual_appliance_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of Network Virtual Appliance.
        """
        return pulumi.get(self, "network_virtual_appliance_name")

    @network_virtual_appliance_name.setter
    def network_virtual_appliance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_virtual_appliance_name", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['VirtualApplianceSkuPropertiesArgs']]:
        """
        Network Virtual Appliance SKU.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['VirtualApplianceSkuPropertiesArgs']]):
        pulumi.set(self, "sku", value)

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
    @pulumi.getter(name="virtualApplianceAsn")
    def virtual_appliance_asn(self) -> Optional[pulumi.Input[float]]:
        """
        VirtualAppliance ASN.
        """
        return pulumi.get(self, "virtual_appliance_asn")

    @virtual_appliance_asn.setter
    def virtual_appliance_asn(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "virtual_appliance_asn", value)

    @property
    @pulumi.getter(name="virtualHub")
    def virtual_hub(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The Virtual Hub where Network Virtual Appliance is being deployed.
        """
        return pulumi.get(self, "virtual_hub")

    @virtual_hub.setter
    def virtual_hub(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "virtual_hub", value)


class NetworkVirtualAppliance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 boot_strap_configuration_blob: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cloud_init_configuration_blob: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_virtual_appliance_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['VirtualApplianceSkuPropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_appliance_asn: Optional[pulumi.Input[float]] = None,
                 virtual_hub: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 __props__=None):
        """
        NetworkVirtualAppliance Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] boot_strap_configuration_blob: BootStrapConfigurationBlob storage URLs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] cloud_init_configuration_blob: CloudInitConfigurationBlob storage URLs.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: The service principal that has read access to cloud-init and config blob.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] network_virtual_appliance_name: The name of Network Virtual Appliance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['VirtualApplianceSkuPropertiesArgs']] sku: Network Virtual Appliance SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[float] virtual_appliance_asn: VirtualAppliance ASN.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] virtual_hub: The Virtual Hub where Network Virtual Appliance is being deployed.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkVirtualApplianceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        NetworkVirtualAppliance Resource.

        :param str resource_name: The name of the resource.
        :param NetworkVirtualApplianceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkVirtualApplianceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 boot_strap_configuration_blob: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cloud_init_configuration_blob: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_virtual_appliance_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['VirtualApplianceSkuPropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_appliance_asn: Optional[pulumi.Input[float]] = None,
                 virtual_hub: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
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
            __props__ = NetworkVirtualApplianceArgs.__new__(NetworkVirtualApplianceArgs)

            __props__.__dict__["boot_strap_configuration_blob"] = boot_strap_configuration_blob
            __props__.__dict__["cloud_init_configuration_blob"] = cloud_init_configuration_blob
            __props__.__dict__["id"] = id
            __props__.__dict__["identity"] = identity
            __props__.__dict__["location"] = location
            __props__.__dict__["network_virtual_appliance_name"] = network_virtual_appliance_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["virtual_appliance_asn"] = virtual_appliance_asn
            __props__.__dict__["virtual_hub"] = virtual_hub
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["virtual_appliance_nics"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/v20200301:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20191201:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20191201:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20200401:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20200401:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20200501:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20200501:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20200601:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20200601:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20200701:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20200701:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20200801:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20200801:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20201101:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20201101:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20210201:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20210201:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-native:network/v20210301:NetworkVirtualAppliance"), pulumi.Alias(type_="azure-nextgen:network/v20210301:NetworkVirtualAppliance")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NetworkVirtualAppliance, __self__).__init__(
            'azure-native:network/v20200301:NetworkVirtualAppliance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NetworkVirtualAppliance':
        """
        Get an existing NetworkVirtualAppliance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkVirtualApplianceArgs.__new__(NetworkVirtualApplianceArgs)

        __props__.__dict__["boot_strap_configuration_blob"] = None
        __props__.__dict__["cloud_init_configuration_blob"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["virtual_appliance_asn"] = None
        __props__.__dict__["virtual_appliance_nics"] = None
        __props__.__dict__["virtual_hub"] = None
        return NetworkVirtualAppliance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bootStrapConfigurationBlob")
    def boot_strap_configuration_blob(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        BootStrapConfigurationBlob storage URLs.
        """
        return pulumi.get(self, "boot_strap_configuration_blob")

    @property
    @pulumi.getter(name="cloudInitConfigurationBlob")
    def cloud_init_configuration_blob(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        CloudInitConfigurationBlob storage URLs.
        """
        return pulumi.get(self, "cloud_init_configuration_blob")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedServiceIdentityResponse']]:
        """
        The service principal that has read access to cloud-init and config blob.
        """
        return pulumi.get(self, "identity")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.VirtualApplianceSkuPropertiesResponse']]:
        """
        Network Virtual Appliance SKU.
        """
        return pulumi.get(self, "sku")

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
    @pulumi.getter(name="virtualApplianceAsn")
    def virtual_appliance_asn(self) -> pulumi.Output[Optional[float]]:
        """
        VirtualAppliance ASN.
        """
        return pulumi.get(self, "virtual_appliance_asn")

    @property
    @pulumi.getter(name="virtualApplianceNics")
    def virtual_appliance_nics(self) -> pulumi.Output[Sequence['outputs.VirtualApplianceNicPropertiesResponse']]:
        """
        List of Virtual Appliance Network Interfaces.
        """
        return pulumi.get(self, "virtual_appliance_nics")

    @property
    @pulumi.getter(name="virtualHub")
    def virtual_hub(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The Virtual Hub where Network Virtual Appliance is being deployed.
        """
        return pulumi.get(self, "virtual_hub")

