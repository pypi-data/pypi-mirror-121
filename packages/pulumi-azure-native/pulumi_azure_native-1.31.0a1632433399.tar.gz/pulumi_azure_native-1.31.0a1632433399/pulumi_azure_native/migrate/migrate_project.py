# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['MigrateProjectArgs', 'MigrateProject']

@pulumi.input_type
class MigrateProjectArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 e_tag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 migrate_project_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['MigrateProjectPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input['MigrateProjectTagsArgs']] = None):
        """
        The set of arguments for constructing a MigrateProject resource.
        :param pulumi.Input[str] resource_group_name: Name of the Azure Resource Group that migrate project is part of.
        :param pulumi.Input[str] e_tag: Gets or sets the eTag for concurrency control.
        :param pulumi.Input[str] location: Gets or sets the Azure location in which migrate project is created.
        :param pulumi.Input[str] migrate_project_name: Name of the Azure Migrate project.
        :param pulumi.Input['MigrateProjectPropertiesArgs'] properties: Gets or sets the nested properties.
        :param pulumi.Input['MigrateProjectTagsArgs'] tags: Gets or sets the tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if e_tag is not None:
            pulumi.set(__self__, "e_tag", e_tag)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if migrate_project_name is not None:
            pulumi.set(__self__, "migrate_project_name", migrate_project_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the Azure Resource Group that migrate project is part of.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the eTag for concurrency control.
        """
        return pulumi.get(self, "e_tag")

    @e_tag.setter
    def e_tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "e_tag", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the Azure location in which migrate project is created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="migrateProjectName")
    def migrate_project_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Azure Migrate project.
        """
        return pulumi.get(self, "migrate_project_name")

    @migrate_project_name.setter
    def migrate_project_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "migrate_project_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['MigrateProjectPropertiesArgs']]:
        """
        Gets or sets the nested properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['MigrateProjectPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input['MigrateProjectTagsArgs']]:
        """
        Gets or sets the tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input['MigrateProjectTagsArgs']]):
        pulumi.set(self, "tags", value)


class MigrateProject(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 migrate_project_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['MigrateProjectPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[pulumi.InputType['MigrateProjectTagsArgs']]] = None,
                 __props__=None):
        """
        Migrate Project REST Resource.
        API Version: 2018-09-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] e_tag: Gets or sets the eTag for concurrency control.
        :param pulumi.Input[str] location: Gets or sets the Azure location in which migrate project is created.
        :param pulumi.Input[str] migrate_project_name: Name of the Azure Migrate project.
        :param pulumi.Input[pulumi.InputType['MigrateProjectPropertiesArgs']] properties: Gets or sets the nested properties.
        :param pulumi.Input[str] resource_group_name: Name of the Azure Resource Group that migrate project is part of.
        :param pulumi.Input[pulumi.InputType['MigrateProjectTagsArgs']] tags: Gets or sets the tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MigrateProjectArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Migrate Project REST Resource.
        API Version: 2018-09-01-preview.

        :param str resource_name: The name of the resource.
        :param MigrateProjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MigrateProjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 migrate_project_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['MigrateProjectPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[pulumi.InputType['MigrateProjectTagsArgs']]] = None,
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
            __props__ = MigrateProjectArgs.__new__(MigrateProjectArgs)

            __props__.__dict__["e_tag"] = e_tag
            __props__.__dict__["location"] = location
            __props__.__dict__["migrate_project_name"] = migrate_project_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:migrate:MigrateProject"), pulumi.Alias(type_="azure-native:migrate/v20180901preview:MigrateProject"), pulumi.Alias(type_="azure-nextgen:migrate/v20180901preview:MigrateProject"), pulumi.Alias(type_="azure-native:migrate/v20200501:MigrateProject"), pulumi.Alias(type_="azure-nextgen:migrate/v20200501:MigrateProject")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MigrateProject, __self__).__init__(
            'azure-native:migrate:MigrateProject',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MigrateProject':
        """
        Get an existing MigrateProject resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MigrateProjectArgs.__new__(MigrateProjectArgs)

        __props__.__dict__["e_tag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return MigrateProject(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the eTag for concurrency control.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the Azure location in which migrate project is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets the name of the migrate project.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.MigrateProjectPropertiesResponse']:
        """
        Gets or sets the nested properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional['outputs.MigrateProjectResponseTags']]:
        """
        Gets or sets the tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Handled by resource provider. Type = Microsoft.Migrate/MigrateProject.
        """
        return pulumi.get(self, "type")

