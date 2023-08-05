# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ApplicationTypeVersionArgs', 'ApplicationTypeVersion']

@pulumi.input_type
class ApplicationTypeVersionArgs:
    def __init__(__self__, *,
                 app_package_url: pulumi.Input[str],
                 application_type_name: pulumi.Input[str],
                 cluster_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApplicationTypeVersion resource.
        :param pulumi.Input[str] app_package_url: The URL to the application package
        :param pulumi.Input[str] application_type_name: The name of the application type name resource.
        :param pulumi.Input[str] cluster_name: The name of the cluster resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] location: It will be deprecated in New API, resource location depends on the parent resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Azure resource tags.
        :param pulumi.Input[str] version: The application type version.
        """
        pulumi.set(__self__, "app_package_url", app_package_url)
        pulumi.set(__self__, "application_type_name", application_type_name)
        pulumi.set(__self__, "cluster_name", cluster_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="appPackageUrl")
    def app_package_url(self) -> pulumi.Input[str]:
        """
        The URL to the application package
        """
        return pulumi.get(self, "app_package_url")

    @app_package_url.setter
    def app_package_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "app_package_url", value)

    @property
    @pulumi.getter(name="applicationTypeName")
    def application_type_name(self) -> pulumi.Input[str]:
        """
        The name of the application type name resource.
        """
        return pulumi.get(self, "application_type_name")

    @application_type_name.setter
    def application_type_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_type_name", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Input[str]:
        """
        The name of the cluster resource.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_name", value)

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
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        It will be deprecated in New API, resource location depends on the parent resource.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Azure resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The application type version.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class ApplicationTypeVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_package_url: Optional[pulumi.Input[str]] = None,
                 application_type_name: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An application type version resource for the specified application type name resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_package_url: The URL to the application package
        :param pulumi.Input[str] application_type_name: The name of the application type name resource.
        :param pulumi.Input[str] cluster_name: The name of the cluster resource.
        :param pulumi.Input[str] location: It will be deprecated in New API, resource location depends on the parent resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Azure resource tags.
        :param pulumi.Input[str] version: The application type version.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationTypeVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An application type version resource for the specified application type name resource.

        :param str resource_name: The name of the resource.
        :param ApplicationTypeVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationTypeVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_package_url: Optional[pulumi.Input[str]] = None,
                 application_type_name: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
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
            __props__ = ApplicationTypeVersionArgs.__new__(ApplicationTypeVersionArgs)

            if app_package_url is None and not opts.urn:
                raise TypeError("Missing required property 'app_package_url'")
            __props__.__dict__["app_package_url"] = app_package_url
            if application_type_name is None and not opts.urn:
                raise TypeError("Missing required property 'application_type_name'")
            __props__.__dict__["application_type_name"] = application_type_name
            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["version"] = version
            __props__.__dict__["default_parameter_list"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:servicefabric/v20191101preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric/v20170701preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric/v20170701preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric/v20190301:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric/v20190301:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric/v20190301preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric/v20190301preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric/v20190601preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric/v20190601preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric/v20200301:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric/v20200301:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric/v20201201preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric/v20201201preview:ApplicationTypeVersion"), pulumi.Alias(type_="azure-native:servicefabric/v20210601:ApplicationTypeVersion"), pulumi.Alias(type_="azure-nextgen:servicefabric/v20210601:ApplicationTypeVersion")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApplicationTypeVersion, __self__).__init__(
            'azure-native:servicefabric/v20191101preview:ApplicationTypeVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationTypeVersion':
        """
        Get an existing ApplicationTypeVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationTypeVersionArgs.__new__(ApplicationTypeVersionArgs)

        __props__.__dict__["app_package_url"] = None
        __props__.__dict__["default_parameter_list"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ApplicationTypeVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appPackageUrl")
    def app_package_url(self) -> pulumi.Output[str]:
        """
        The URL to the application package
        """
        return pulumi.get(self, "app_package_url")

    @property
    @pulumi.getter(name="defaultParameterList")
    def default_parameter_list(self) -> pulumi.Output[Mapping[str, str]]:
        """
        List of application type parameters that can be overridden when creating or updating the application.
        """
        return pulumi.get(self, "default_parameter_list")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Azure resource etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        It will be deprecated in New API, resource location depends on the parent resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The current deployment or provisioning state, which only appears in the response
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Azure resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type.
        """
        return pulumi.get(self, "type")

