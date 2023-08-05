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

__all__ = ['StorageTargetArgs', 'StorageTarget']

@pulumi.input_type
class StorageTargetArgs:
    def __init__(__self__, *,
                 cache_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 target_type: pulumi.Input[Union[str, 'StorageTargetType']],
                 clfs: Optional[pulumi.Input['ClfsTargetArgs']] = None,
                 junctions: Optional[pulumi.Input[Sequence[pulumi.Input['NamespaceJunctionArgs']]]] = None,
                 nfs3: Optional[pulumi.Input['Nfs3TargetArgs']] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningStateType']]] = None,
                 storage_target_name: Optional[pulumi.Input[str]] = None,
                 unknown: Optional[pulumi.Input['UnknownTargetArgs']] = None):
        """
        The set of arguments for constructing a StorageTarget resource.
        :param pulumi.Input[str] cache_name: Name of Cache. Length of name must be not greater than 80 and chars must be in list of [-0-9a-zA-Z_] char class.
        :param pulumi.Input[str] resource_group_name: Target resource group.
        :param pulumi.Input[Union[str, 'StorageTargetType']] target_type: Type of the Storage Target.
        :param pulumi.Input['ClfsTargetArgs'] clfs: Properties when targetType is clfs.
        :param pulumi.Input[Sequence[pulumi.Input['NamespaceJunctionArgs']]] junctions: List of Cache namespace junctions to target for namespace associations.
        :param pulumi.Input['Nfs3TargetArgs'] nfs3: Properties when targetType is nfs3.
        :param pulumi.Input[Union[str, 'ProvisioningStateType']] provisioning_state: ARM provisioning state, see https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/Addendum.md#provisioningstate-property
        :param pulumi.Input[str] storage_target_name: Name of the Storage Target. Length of name must be not greater than 80 and chars must be in list of [-0-9a-zA-Z_] char class.
        :param pulumi.Input['UnknownTargetArgs'] unknown: Properties when targetType is unknown.
        """
        pulumi.set(__self__, "cache_name", cache_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "target_type", target_type)
        if clfs is not None:
            pulumi.set(__self__, "clfs", clfs)
        if junctions is not None:
            pulumi.set(__self__, "junctions", junctions)
        if nfs3 is not None:
            pulumi.set(__self__, "nfs3", nfs3)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if storage_target_name is not None:
            pulumi.set(__self__, "storage_target_name", storage_target_name)
        if unknown is not None:
            pulumi.set(__self__, "unknown", unknown)

    @property
    @pulumi.getter(name="cacheName")
    def cache_name(self) -> pulumi.Input[str]:
        """
        Name of Cache. Length of name must be not greater than 80 and chars must be in list of [-0-9a-zA-Z_] char class.
        """
        return pulumi.get(self, "cache_name")

    @cache_name.setter
    def cache_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cache_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Target resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Input[Union[str, 'StorageTargetType']]:
        """
        Type of the Storage Target.
        """
        return pulumi.get(self, "target_type")

    @target_type.setter
    def target_type(self, value: pulumi.Input[Union[str, 'StorageTargetType']]):
        pulumi.set(self, "target_type", value)

    @property
    @pulumi.getter
    def clfs(self) -> Optional[pulumi.Input['ClfsTargetArgs']]:
        """
        Properties when targetType is clfs.
        """
        return pulumi.get(self, "clfs")

    @clfs.setter
    def clfs(self, value: Optional[pulumi.Input['ClfsTargetArgs']]):
        pulumi.set(self, "clfs", value)

    @property
    @pulumi.getter
    def junctions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NamespaceJunctionArgs']]]]:
        """
        List of Cache namespace junctions to target for namespace associations.
        """
        return pulumi.get(self, "junctions")

    @junctions.setter
    def junctions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NamespaceJunctionArgs']]]]):
        pulumi.set(self, "junctions", value)

    @property
    @pulumi.getter
    def nfs3(self) -> Optional[pulumi.Input['Nfs3TargetArgs']]:
        """
        Properties when targetType is nfs3.
        """
        return pulumi.get(self, "nfs3")

    @nfs3.setter
    def nfs3(self, value: Optional[pulumi.Input['Nfs3TargetArgs']]):
        pulumi.set(self, "nfs3", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[Union[str, 'ProvisioningStateType']]]:
        """
        ARM provisioning state, see https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/Addendum.md#provisioningstate-property
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[Union[str, 'ProvisioningStateType']]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter(name="storageTargetName")
    def storage_target_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Storage Target. Length of name must be not greater than 80 and chars must be in list of [-0-9a-zA-Z_] char class.
        """
        return pulumi.get(self, "storage_target_name")

    @storage_target_name.setter
    def storage_target_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_target_name", value)

    @property
    @pulumi.getter
    def unknown(self) -> Optional[pulumi.Input['UnknownTargetArgs']]:
        """
        Properties when targetType is unknown.
        """
        return pulumi.get(self, "unknown")

    @unknown.setter
    def unknown(self, value: Optional[pulumi.Input['UnknownTargetArgs']]):
        pulumi.set(self, "unknown", value)


class StorageTarget(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cache_name: Optional[pulumi.Input[str]] = None,
                 clfs: Optional[pulumi.Input[pulumi.InputType['ClfsTargetArgs']]] = None,
                 junctions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NamespaceJunctionArgs']]]]] = None,
                 nfs3: Optional[pulumi.Input[pulumi.InputType['Nfs3TargetArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningStateType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_target_name: Optional[pulumi.Input[str]] = None,
                 target_type: Optional[pulumi.Input[Union[str, 'StorageTargetType']]] = None,
                 unknown: Optional[pulumi.Input[pulumi.InputType['UnknownTargetArgs']]] = None,
                 __props__=None):
        """
        Type of the Storage Target.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cache_name: Name of Cache. Length of name must be not greater than 80 and chars must be in list of [-0-9a-zA-Z_] char class.
        :param pulumi.Input[pulumi.InputType['ClfsTargetArgs']] clfs: Properties when targetType is clfs.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NamespaceJunctionArgs']]]] junctions: List of Cache namespace junctions to target for namespace associations.
        :param pulumi.Input[pulumi.InputType['Nfs3TargetArgs']] nfs3: Properties when targetType is nfs3.
        :param pulumi.Input[Union[str, 'ProvisioningStateType']] provisioning_state: ARM provisioning state, see https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/Addendum.md#provisioningstate-property
        :param pulumi.Input[str] resource_group_name: Target resource group.
        :param pulumi.Input[str] storage_target_name: Name of the Storage Target. Length of name must be not greater than 80 and chars must be in list of [-0-9a-zA-Z_] char class.
        :param pulumi.Input[Union[str, 'StorageTargetType']] target_type: Type of the Storage Target.
        :param pulumi.Input[pulumi.InputType['UnknownTargetArgs']] unknown: Properties when targetType is unknown.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StorageTargetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Type of the Storage Target.

        :param str resource_name: The name of the resource.
        :param StorageTargetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StorageTargetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cache_name: Optional[pulumi.Input[str]] = None,
                 clfs: Optional[pulumi.Input[pulumi.InputType['ClfsTargetArgs']]] = None,
                 junctions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NamespaceJunctionArgs']]]]] = None,
                 nfs3: Optional[pulumi.Input[pulumi.InputType['Nfs3TargetArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningStateType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_target_name: Optional[pulumi.Input[str]] = None,
                 target_type: Optional[pulumi.Input[Union[str, 'StorageTargetType']]] = None,
                 unknown: Optional[pulumi.Input[pulumi.InputType['UnknownTargetArgs']]] = None,
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
            __props__ = StorageTargetArgs.__new__(StorageTargetArgs)

            if cache_name is None and not opts.urn:
                raise TypeError("Missing required property 'cache_name'")
            __props__.__dict__["cache_name"] = cache_name
            __props__.__dict__["clfs"] = clfs
            __props__.__dict__["junctions"] = junctions
            __props__.__dict__["nfs3"] = nfs3
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["storage_target_name"] = storage_target_name
            if target_type is None and not opts.urn:
                raise TypeError("Missing required property 'target_type'")
            __props__.__dict__["target_type"] = target_type
            __props__.__dict__["unknown"] = unknown
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storagecache/v20200301:StorageTarget"), pulumi.Alias(type_="azure-native:storagecache:StorageTarget"), pulumi.Alias(type_="azure-nextgen:storagecache:StorageTarget"), pulumi.Alias(type_="azure-native:storagecache/v20190801preview:StorageTarget"), pulumi.Alias(type_="azure-nextgen:storagecache/v20190801preview:StorageTarget"), pulumi.Alias(type_="azure-native:storagecache/v20191101:StorageTarget"), pulumi.Alias(type_="azure-nextgen:storagecache/v20191101:StorageTarget"), pulumi.Alias(type_="azure-native:storagecache/v20201001:StorageTarget"), pulumi.Alias(type_="azure-nextgen:storagecache/v20201001:StorageTarget"), pulumi.Alias(type_="azure-native:storagecache/v20210301:StorageTarget"), pulumi.Alias(type_="azure-nextgen:storagecache/v20210301:StorageTarget"), pulumi.Alias(type_="azure-native:storagecache/v20210501:StorageTarget"), pulumi.Alias(type_="azure-nextgen:storagecache/v20210501:StorageTarget")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StorageTarget, __self__).__init__(
            'azure-native:storagecache/v20200301:StorageTarget',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageTarget':
        """
        Get an existing StorageTarget resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StorageTargetArgs.__new__(StorageTargetArgs)

        __props__.__dict__["clfs"] = None
        __props__.__dict__["junctions"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["nfs3"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["target_type"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["unknown"] = None
        return StorageTarget(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def clfs(self) -> pulumi.Output[Optional['outputs.ClfsTargetResponse']]:
        """
        Properties when targetType is clfs.
        """
        return pulumi.get(self, "clfs")

    @property
    @pulumi.getter
    def junctions(self) -> pulumi.Output[Optional[Sequence['outputs.NamespaceJunctionResponse']]]:
        """
        List of Cache namespace junctions to target for namespace associations.
        """
        return pulumi.get(self, "junctions")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Region name string.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Storage Target.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def nfs3(self) -> pulumi.Output[Optional['outputs.Nfs3TargetResponse']]:
        """
        Properties when targetType is nfs3.
        """
        return pulumi.get(self, "nfs3")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        ARM provisioning state, see https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/Addendum.md#provisioningstate-property
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[str]:
        """
        Type of the Storage Target.
        """
        return pulumi.get(self, "target_type")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the Storage Target; Microsoft.StorageCache/Cache/StorageTarget
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def unknown(self) -> pulumi.Output[Optional['outputs.UnknownTargetResponse']]:
        """
        Properties when targetType is unknown.
        """
        return pulumi.get(self, "unknown")

