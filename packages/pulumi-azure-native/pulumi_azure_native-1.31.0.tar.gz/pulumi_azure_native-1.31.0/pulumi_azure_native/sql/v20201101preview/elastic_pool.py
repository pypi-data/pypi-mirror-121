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

__all__ = ['ElasticPoolArgs', 'ElasticPool']

@pulumi.input_type
class ElasticPoolArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 elastic_pool_name: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ElasticPoolLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 max_size_bytes: Optional[pulumi.Input[float]] = None,
                 per_database_settings: Optional[pulumi.Input['ElasticPoolPerDatabaseSettingsArgs']] = None,
                 sku: Optional[pulumi.Input['SkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a ElasticPool resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] elastic_pool_name: The name of the elastic pool.
        :param pulumi.Input[Union[str, 'ElasticPoolLicenseType']] license_type: The license type to apply for this elastic pool.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] maintenance_configuration_id: Maintenance configuration id assigned to the elastic pool. This configuration defines the period when the maintenance updates will will occur.
        :param pulumi.Input[float] max_size_bytes: The storage limit for the database elastic pool in bytes.
        :param pulumi.Input['ElasticPoolPerDatabaseSettingsArgs'] per_database_settings: The per database settings for the elastic pool.
        :param pulumi.Input['SkuArgs'] sku: The elastic pool SKU.
               
               The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or the following command:
               
               ```azurecli
               az sql elastic-pool list-editions -l <location> -o table
               ````
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[bool] zone_redundant: Whether or not this elastic pool is zone redundant, which means the replicas of this elastic pool will be spread across multiple availability zones.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server_name", server_name)
        if elastic_pool_name is not None:
            pulumi.set(__self__, "elastic_pool_name", elastic_pool_name)
        if license_type is not None:
            pulumi.set(__self__, "license_type", license_type)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maintenance_configuration_id is not None:
            pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        if max_size_bytes is not None:
            pulumi.set(__self__, "max_size_bytes", max_size_bytes)
        if per_database_settings is not None:
            pulumi.set(__self__, "per_database_settings", per_database_settings)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if zone_redundant is not None:
            pulumi.set(__self__, "zone_redundant", zone_redundant)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> pulumi.Input[str]:
        """
        The name of the server.
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter(name="elasticPoolName")
    def elastic_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the elastic pool.
        """
        return pulumi.get(self, "elastic_pool_name")

    @elastic_pool_name.setter
    def elastic_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "elastic_pool_name", value)

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> Optional[pulumi.Input[Union[str, 'ElasticPoolLicenseType']]]:
        """
        The license type to apply for this elastic pool.
        """
        return pulumi.get(self, "license_type")

    @license_type.setter
    def license_type(self, value: Optional[pulumi.Input[Union[str, 'ElasticPoolLicenseType']]]):
        pulumi.set(self, "license_type", value)

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
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        Maintenance configuration id assigned to the elastic pool. This configuration defines the period when the maintenance updates will will occur.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @maintenance_configuration_id.setter
    def maintenance_configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maintenance_configuration_id", value)

    @property
    @pulumi.getter(name="maxSizeBytes")
    def max_size_bytes(self) -> Optional[pulumi.Input[float]]:
        """
        The storage limit for the database elastic pool in bytes.
        """
        return pulumi.get(self, "max_size_bytes")

    @max_size_bytes.setter
    def max_size_bytes(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_size_bytes", value)

    @property
    @pulumi.getter(name="perDatabaseSettings")
    def per_database_settings(self) -> Optional[pulumi.Input['ElasticPoolPerDatabaseSettingsArgs']]:
        """
        The per database settings for the elastic pool.
        """
        return pulumi.get(self, "per_database_settings")

    @per_database_settings.setter
    def per_database_settings(self, value: Optional[pulumi.Input['ElasticPoolPerDatabaseSettingsArgs']]):
        pulumi.set(self, "per_database_settings", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        The elastic pool SKU.
        
        The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or the following command:
        
        ```azurecli
        az sql elastic-pool list-editions -l <location> -o table
        ````
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
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
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not this elastic pool is zone redundant, which means the replicas of this elastic pool will be spread across multiple availability zones.
        """
        return pulumi.get(self, "zone_redundant")

    @zone_redundant.setter
    def zone_redundant(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "zone_redundant", value)


class ElasticPool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 elastic_pool_name: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ElasticPoolLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 max_size_bytes: Optional[pulumi.Input[float]] = None,
                 per_database_settings: Optional[pulumi.Input[pulumi.InputType['ElasticPoolPerDatabaseSettingsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        An elastic pool.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] elastic_pool_name: The name of the elastic pool.
        :param pulumi.Input[Union[str, 'ElasticPoolLicenseType']] license_type: The license type to apply for this elastic pool.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] maintenance_configuration_id: Maintenance configuration id assigned to the elastic pool. This configuration defines the period when the maintenance updates will will occur.
        :param pulumi.Input[float] max_size_bytes: The storage limit for the database elastic pool in bytes.
        :param pulumi.Input[pulumi.InputType['ElasticPoolPerDatabaseSettingsArgs']] per_database_settings: The per database settings for the elastic pool.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The elastic pool SKU.
               
               The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or the following command:
               
               ```azurecli
               az sql elastic-pool list-editions -l <location> -o table
               ````
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[bool] zone_redundant: Whether or not this elastic pool is zone redundant, which means the replicas of this elastic pool will be spread across multiple availability zones.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ElasticPoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An elastic pool.

        :param str resource_name: The name of the resource.
        :param ElasticPoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ElasticPoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 elastic_pool_name: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ElasticPoolLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 max_size_bytes: Optional[pulumi.Input[float]] = None,
                 per_database_settings: Optional[pulumi.Input[pulumi.InputType['ElasticPoolPerDatabaseSettingsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
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
            __props__ = ElasticPoolArgs.__new__(ElasticPoolArgs)

            __props__.__dict__["elastic_pool_name"] = elastic_pool_name
            __props__.__dict__["license_type"] = license_type
            __props__.__dict__["location"] = location
            __props__.__dict__["maintenance_configuration_id"] = maintenance_configuration_id
            __props__.__dict__["max_size_bytes"] = max_size_bytes
            __props__.__dict__["per_database_settings"] = per_database_settings
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["zone_redundant"] = zone_redundant
            __props__.__dict__["creation_date"] = None
            __props__.__dict__["kind"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/v20201101preview:ElasticPool"), pulumi.Alias(type_="azure-native:sql:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql:ElasticPool"), pulumi.Alias(type_="azure-native:sql/v20140401:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20140401:ElasticPool"), pulumi.Alias(type_="azure-native:sql/v20171001preview:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20171001preview:ElasticPool"), pulumi.Alias(type_="azure-native:sql/v20200202preview:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:ElasticPool"), pulumi.Alias(type_="azure-native:sql/v20200801preview:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:ElasticPool"), pulumi.Alias(type_="azure-native:sql/v20210201preview:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20210201preview:ElasticPool")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ElasticPool, __self__).__init__(
            'azure-native:sql/v20201101preview:ElasticPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ElasticPool':
        """
        Get an existing ElasticPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ElasticPoolArgs.__new__(ElasticPoolArgs)

        __props__.__dict__["creation_date"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["license_type"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["maintenance_configuration_id"] = None
        __props__.__dict__["max_size_bytes"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["per_database_settings"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["zone_redundant"] = None
        return ElasticPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of the elastic pool (ISO8601 format).
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Kind of elastic pool. This is metadata used for the Azure portal experience.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Output[Optional[str]]:
        """
        The license type to apply for this elastic pool.
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Output[Optional[str]]:
        """
        Maintenance configuration id assigned to the elastic pool. This configuration defines the period when the maintenance updates will will occur.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter(name="maxSizeBytes")
    def max_size_bytes(self) -> pulumi.Output[Optional[float]]:
        """
        The storage limit for the database elastic pool in bytes.
        """
        return pulumi.get(self, "max_size_bytes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="perDatabaseSettings")
    def per_database_settings(self) -> pulumi.Output[Optional['outputs.ElasticPoolPerDatabaseSettingsResponse']]:
        """
        The per database settings for the elastic pool.
        """
        return pulumi.get(self, "per_database_settings")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The elastic pool SKU.
        
        The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or the following command:
        
        ```azurecli
        az sql elastic-pool list-editions -l <location> -o table
        ````
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the elastic pool.
        """
        return pulumi.get(self, "state")

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
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not this elastic pool is zone redundant, which means the replicas of this elastic pool will be spread across multiple availability zones.
        """
        return pulumi.get(self, "zone_redundant")

