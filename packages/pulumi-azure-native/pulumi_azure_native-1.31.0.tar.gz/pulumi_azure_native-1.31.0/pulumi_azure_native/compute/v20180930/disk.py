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

__all__ = ['DiskArgs', 'Disk']

@pulumi.input_type
class DiskArgs:
    def __init__(__self__, *,
                 creation_data: pulumi.Input['CreationDataArgs'],
                 resource_group_name: pulumi.Input[str],
                 disk_iops_read_write: Optional[pulumi.Input[float]] = None,
                 disk_m_bps_read_write: Optional[pulumi.Input[int]] = None,
                 disk_name: Optional[pulumi.Input[str]] = None,
                 disk_size_gb: Optional[pulumi.Input[int]] = None,
                 encryption_settings_collection: Optional[pulumi.Input['EncryptionSettingsCollectionArgs']] = None,
                 hyper_v_generation: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input['OperatingSystemTypes']] = None,
                 sku: Optional[pulumi.Input['DiskSkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Disk resource.
        :param pulumi.Input['CreationDataArgs'] creation_data: Disk source information. CreationData information cannot be changed after the disk has been created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[float] disk_iops_read_write: The number of IOPS allowed for this disk; only settable for UltraSSD disks. One operation can transfer between 4k and 256k bytes.
        :param pulumi.Input[int] disk_m_bps_read_write: The bandwidth allowed for this disk; only settable for UltraSSD disks. MBps means millions of bytes per second - MB here uses the ISO notation, of powers of 10.
        :param pulumi.Input[str] disk_name: The name of the managed disk that is being created. The name can't be changed after the disk is created. Supported characters for the name are a-z, A-Z, 0-9 and _. The maximum name length is 80 characters.
        :param pulumi.Input[int] disk_size_gb: If creationData.createOption is Empty, this field is mandatory and it indicates the size of the VHD to create. If this field is present for updates or creation with other options, it indicates a resize. Resizes are only allowed if the disk is not attached to a running VM, and can only increase the disk's size.
        :param pulumi.Input['EncryptionSettingsCollectionArgs'] encryption_settings_collection: Encryption settings collection used for Azure Disk Encryption, can contain multiple encryption settings per disk or snapshot.
        :param pulumi.Input[Union[str, 'HyperVGeneration']] hyper_v_generation: The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input['OperatingSystemTypes'] os_type: The Operating System type.
        :param pulumi.Input['DiskSkuArgs'] sku: The disks sku name. Can be Standard_LRS, Premium_LRS, StandardSSD_LRS, or UltraSSD_LRS.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: The Logical zone list for Disk.
        """
        pulumi.set(__self__, "creation_data", creation_data)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if disk_iops_read_write is not None:
            pulumi.set(__self__, "disk_iops_read_write", disk_iops_read_write)
        if disk_m_bps_read_write is not None:
            pulumi.set(__self__, "disk_m_bps_read_write", disk_m_bps_read_write)
        if disk_name is not None:
            pulumi.set(__self__, "disk_name", disk_name)
        if disk_size_gb is not None:
            pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if encryption_settings_collection is not None:
            pulumi.set(__self__, "encryption_settings_collection", encryption_settings_collection)
        if hyper_v_generation is not None:
            pulumi.set(__self__, "hyper_v_generation", hyper_v_generation)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="creationData")
    def creation_data(self) -> pulumi.Input['CreationDataArgs']:
        """
        Disk source information. CreationData information cannot be changed after the disk has been created.
        """
        return pulumi.get(self, "creation_data")

    @creation_data.setter
    def creation_data(self, value: pulumi.Input['CreationDataArgs']):
        pulumi.set(self, "creation_data", value)

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
    @pulumi.getter(name="diskIOPSReadWrite")
    def disk_iops_read_write(self) -> Optional[pulumi.Input[float]]:
        """
        The number of IOPS allowed for this disk; only settable for UltraSSD disks. One operation can transfer between 4k and 256k bytes.
        """
        return pulumi.get(self, "disk_iops_read_write")

    @disk_iops_read_write.setter
    def disk_iops_read_write(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "disk_iops_read_write", value)

    @property
    @pulumi.getter(name="diskMBpsReadWrite")
    def disk_m_bps_read_write(self) -> Optional[pulumi.Input[int]]:
        """
        The bandwidth allowed for this disk; only settable for UltraSSD disks. MBps means millions of bytes per second - MB here uses the ISO notation, of powers of 10.
        """
        return pulumi.get(self, "disk_m_bps_read_write")

    @disk_m_bps_read_write.setter
    def disk_m_bps_read_write(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "disk_m_bps_read_write", value)

    @property
    @pulumi.getter(name="diskName")
    def disk_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the managed disk that is being created. The name can't be changed after the disk is created. Supported characters for the name are a-z, A-Z, 0-9 and _. The maximum name length is 80 characters.
        """
        return pulumi.get(self, "disk_name")

    @disk_name.setter
    def disk_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk_name", value)

    @property
    @pulumi.getter(name="diskSizeGB")
    def disk_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        If creationData.createOption is Empty, this field is mandatory and it indicates the size of the VHD to create. If this field is present for updates or creation with other options, it indicates a resize. Resizes are only allowed if the disk is not attached to a running VM, and can only increase the disk's size.
        """
        return pulumi.get(self, "disk_size_gb")

    @disk_size_gb.setter
    def disk_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "disk_size_gb", value)

    @property
    @pulumi.getter(name="encryptionSettingsCollection")
    def encryption_settings_collection(self) -> Optional[pulumi.Input['EncryptionSettingsCollectionArgs']]:
        """
        Encryption settings collection used for Azure Disk Encryption, can contain multiple encryption settings per disk or snapshot.
        """
        return pulumi.get(self, "encryption_settings_collection")

    @encryption_settings_collection.setter
    def encryption_settings_collection(self, value: Optional[pulumi.Input['EncryptionSettingsCollectionArgs']]):
        pulumi.set(self, "encryption_settings_collection", value)

    @property
    @pulumi.getter(name="hyperVGeneration")
    def hyper_v_generation(self) -> Optional[pulumi.Input[Union[str, 'HyperVGeneration']]]:
        """
        The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        """
        return pulumi.get(self, "hyper_v_generation")

    @hyper_v_generation.setter
    def hyper_v_generation(self, value: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]]):
        pulumi.set(self, "hyper_v_generation", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input['OperatingSystemTypes']]:
        """
        The Operating System type.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input['OperatingSystemTypes']]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['DiskSkuArgs']]:
        """
        The disks sku name. Can be Standard_LRS, Premium_LRS, StandardSSD_LRS, or UltraSSD_LRS.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['DiskSkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The Logical zone list for Disk.
        """
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "zones", value)


class Disk(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 creation_data: Optional[pulumi.Input[pulumi.InputType['CreationDataArgs']]] = None,
                 disk_iops_read_write: Optional[pulumi.Input[float]] = None,
                 disk_m_bps_read_write: Optional[pulumi.Input[int]] = None,
                 disk_name: Optional[pulumi.Input[str]] = None,
                 disk_size_gb: Optional[pulumi.Input[int]] = None,
                 encryption_settings_collection: Optional[pulumi.Input[pulumi.InputType['EncryptionSettingsCollectionArgs']]] = None,
                 hyper_v_generation: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input['OperatingSystemTypes']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['DiskSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Disk resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['CreationDataArgs']] creation_data: Disk source information. CreationData information cannot be changed after the disk has been created.
        :param pulumi.Input[float] disk_iops_read_write: The number of IOPS allowed for this disk; only settable for UltraSSD disks. One operation can transfer between 4k and 256k bytes.
        :param pulumi.Input[int] disk_m_bps_read_write: The bandwidth allowed for this disk; only settable for UltraSSD disks. MBps means millions of bytes per second - MB here uses the ISO notation, of powers of 10.
        :param pulumi.Input[str] disk_name: The name of the managed disk that is being created. The name can't be changed after the disk is created. Supported characters for the name are a-z, A-Z, 0-9 and _. The maximum name length is 80 characters.
        :param pulumi.Input[int] disk_size_gb: If creationData.createOption is Empty, this field is mandatory and it indicates the size of the VHD to create. If this field is present for updates or creation with other options, it indicates a resize. Resizes are only allowed if the disk is not attached to a running VM, and can only increase the disk's size.
        :param pulumi.Input[pulumi.InputType['EncryptionSettingsCollectionArgs']] encryption_settings_collection: Encryption settings collection used for Azure Disk Encryption, can contain multiple encryption settings per disk or snapshot.
        :param pulumi.Input[Union[str, 'HyperVGeneration']] hyper_v_generation: The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input['OperatingSystemTypes'] os_type: The Operating System type.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['DiskSkuArgs']] sku: The disks sku name. Can be Standard_LRS, Premium_LRS, StandardSSD_LRS, or UltraSSD_LRS.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: The Logical zone list for Disk.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DiskArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Disk resource.

        :param str resource_name: The name of the resource.
        :param DiskArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DiskArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 creation_data: Optional[pulumi.Input[pulumi.InputType['CreationDataArgs']]] = None,
                 disk_iops_read_write: Optional[pulumi.Input[float]] = None,
                 disk_m_bps_read_write: Optional[pulumi.Input[int]] = None,
                 disk_name: Optional[pulumi.Input[str]] = None,
                 disk_size_gb: Optional[pulumi.Input[int]] = None,
                 encryption_settings_collection: Optional[pulumi.Input[pulumi.InputType['EncryptionSettingsCollectionArgs']]] = None,
                 hyper_v_generation: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input['OperatingSystemTypes']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['DiskSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = DiskArgs.__new__(DiskArgs)

            if creation_data is None and not opts.urn:
                raise TypeError("Missing required property 'creation_data'")
            __props__.__dict__["creation_data"] = creation_data
            __props__.__dict__["disk_iops_read_write"] = disk_iops_read_write
            __props__.__dict__["disk_m_bps_read_write"] = disk_m_bps_read_write
            __props__.__dict__["disk_name"] = disk_name
            __props__.__dict__["disk_size_gb"] = disk_size_gb
            __props__.__dict__["encryption_settings_collection"] = encryption_settings_collection
            __props__.__dict__["hyper_v_generation"] = hyper_v_generation
            __props__.__dict__["location"] = location
            __props__.__dict__["os_type"] = os_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["zones"] = zones
            __props__.__dict__["disk_state"] = None
            __props__.__dict__["managed_by"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["time_created"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute/v20180930:Disk"), pulumi.Alias(type_="azure-native:compute:Disk"), pulumi.Alias(type_="azure-nextgen:compute:Disk"), pulumi.Alias(type_="azure-native:compute/v20160430preview:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20160430preview:Disk"), pulumi.Alias(type_="azure-native:compute/v20170330:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20170330:Disk"), pulumi.Alias(type_="azure-native:compute/v20180401:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20180401:Disk"), pulumi.Alias(type_="azure-native:compute/v20180601:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20180601:Disk"), pulumi.Alias(type_="azure-native:compute/v20190301:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:Disk"), pulumi.Alias(type_="azure-native:compute/v20190701:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:Disk"), pulumi.Alias(type_="azure-native:compute/v20191101:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20191101:Disk"), pulumi.Alias(type_="azure-native:compute/v20200501:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20200501:Disk"), pulumi.Alias(type_="azure-native:compute/v20200630:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20200630:Disk"), pulumi.Alias(type_="azure-native:compute/v20200930:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20200930:Disk"), pulumi.Alias(type_="azure-native:compute/v20201201:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20201201:Disk"), pulumi.Alias(type_="azure-native:compute/v20210401:Disk"), pulumi.Alias(type_="azure-nextgen:compute/v20210401:Disk")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Disk, __self__).__init__(
            'azure-native:compute/v20180930:Disk',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Disk':
        """
        Get an existing Disk resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DiskArgs.__new__(DiskArgs)

        __props__.__dict__["creation_data"] = None
        __props__.__dict__["disk_iops_read_write"] = None
        __props__.__dict__["disk_m_bps_read_write"] = None
        __props__.__dict__["disk_size_gb"] = None
        __props__.__dict__["disk_state"] = None
        __props__.__dict__["encryption_settings_collection"] = None
        __props__.__dict__["hyper_v_generation"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["managed_by"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["os_type"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["time_created"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["zones"] = None
        return Disk(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationData")
    def creation_data(self) -> pulumi.Output['outputs.CreationDataResponse']:
        """
        Disk source information. CreationData information cannot be changed after the disk has been created.
        """
        return pulumi.get(self, "creation_data")

    @property
    @pulumi.getter(name="diskIOPSReadWrite")
    def disk_iops_read_write(self) -> pulumi.Output[Optional[float]]:
        """
        The number of IOPS allowed for this disk; only settable for UltraSSD disks. One operation can transfer between 4k and 256k bytes.
        """
        return pulumi.get(self, "disk_iops_read_write")

    @property
    @pulumi.getter(name="diskMBpsReadWrite")
    def disk_m_bps_read_write(self) -> pulumi.Output[Optional[int]]:
        """
        The bandwidth allowed for this disk; only settable for UltraSSD disks. MBps means millions of bytes per second - MB here uses the ISO notation, of powers of 10.
        """
        return pulumi.get(self, "disk_m_bps_read_write")

    @property
    @pulumi.getter(name="diskSizeGB")
    def disk_size_gb(self) -> pulumi.Output[Optional[int]]:
        """
        If creationData.createOption is Empty, this field is mandatory and it indicates the size of the VHD to create. If this field is present for updates or creation with other options, it indicates a resize. Resizes are only allowed if the disk is not attached to a running VM, and can only increase the disk's size.
        """
        return pulumi.get(self, "disk_size_gb")

    @property
    @pulumi.getter(name="diskState")
    def disk_state(self) -> pulumi.Output[str]:
        """
        The state of the disk.
        """
        return pulumi.get(self, "disk_state")

    @property
    @pulumi.getter(name="encryptionSettingsCollection")
    def encryption_settings_collection(self) -> pulumi.Output[Optional['outputs.EncryptionSettingsCollectionResponse']]:
        """
        Encryption settings collection used for Azure Disk Encryption, can contain multiple encryption settings per disk or snapshot.
        """
        return pulumi.get(self, "encryption_settings_collection")

    @property
    @pulumi.getter(name="hyperVGeneration")
    def hyper_v_generation(self) -> pulumi.Output[Optional[str]]:
        """
        The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        """
        return pulumi.get(self, "hyper_v_generation")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> pulumi.Output[str]:
        """
        A relative URI containing the ID of the VM that has the disk attached.
        """
        return pulumi.get(self, "managed_by")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[Optional[str]]:
        """
        The Operating System type.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The disk provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.DiskSkuResponse']]:
        """
        The disks sku name. Can be Standard_LRS, Premium_LRS, StandardSSD_LRS, or UltraSSD_LRS.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeCreated")
    def time_created(self) -> pulumi.Output[str]:
        """
        The time when the disk was created.
        """
        return pulumi.get(self, "time_created")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The Logical zone list for Disk.
        """
        return pulumi.get(self, "zones")

