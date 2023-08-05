# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ApplicationPackageArgs', 'ApplicationPackage']

@pulumi.input_type
class ApplicationPackageArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 application_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 version_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApplicationPackage resource.
        :param pulumi.Input[str] account_name: The name of the Batch account.
        :param pulumi.Input[str] application_name: The name of the application. This must be unique within the account.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the Batch account.
        :param pulumi.Input[str] version_name: The version of the application.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "application_name", application_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if version_name is not None:
            pulumi.set(__self__, "version_name", version_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the Batch account.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="applicationName")
    def application_name(self) -> pulumi.Input[str]:
        """
        The name of the application. This must be unique within the account.
        """
        return pulumi.get(self, "application_name")

    @application_name.setter
    def application_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the Batch account.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="versionName")
    def version_name(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the application.
        """
        return pulumi.get(self, "version_name")

    @version_name.setter
    def version_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_name", value)


class ApplicationPackage(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An application package which represents a particular version of an application.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Batch account.
        :param pulumi.Input[str] application_name: The name of the application. This must be unique within the account.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the Batch account.
        :param pulumi.Input[str] version_name: The version of the application.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationPackageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An application package which represents a particular version of an application.

        :param str resource_name: The name of the resource.
        :param ApplicationPackageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationPackageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ApplicationPackageArgs.__new__(ApplicationPackageArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            if application_name is None and not opts.urn:
                raise TypeError("Missing required property 'application_name'")
            __props__.__dict__["application_name"] = application_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["version_name"] = version_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["format"] = None
            __props__.__dict__["last_activation_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["storage_url"] = None
            __props__.__dict__["storage_url_expiry"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:batch/v20200901:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20151201:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20151201:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20170101:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20170101:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20170501:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20170501:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20170901:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20170901:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20181201:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20181201:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20190401:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20190401:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20190801:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20190801:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20200301:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20200301:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20200501:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20200501:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20210101:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20210101:ApplicationPackage"), pulumi.Alias(type_="azure-native:batch/v20210601:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20210601:ApplicationPackage")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApplicationPackage, __self__).__init__(
            'azure-native:batch/v20200901:ApplicationPackage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationPackage':
        """
        Get an existing ApplicationPackage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationPackageArgs.__new__(ApplicationPackageArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["format"] = None
        __props__.__dict__["last_activation_time"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["storage_url"] = None
        __props__.__dict__["storage_url_expiry"] = None
        __props__.__dict__["type"] = None
        return ApplicationPackage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The ETag of the resource, used for concurrency statements.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def format(self) -> pulumi.Output[str]:
        """
        The format of the application package, if the package is active.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter(name="lastActivationTime")
    def last_activation_time(self) -> pulumi.Output[str]:
        """
        The time at which the package was last activated, if the package is active.
        """
        return pulumi.get(self, "last_activation_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the application package.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageUrl")
    def storage_url(self) -> pulumi.Output[str]:
        """
        The URL for the application package in Azure Storage.
        """
        return pulumi.get(self, "storage_url")

    @property
    @pulumi.getter(name="storageUrlExpiry")
    def storage_url_expiry(self) -> pulumi.Output[str]:
        """
        The UTC time at which the Azure Storage URL will expire.
        """
        return pulumi.get(self, "storage_url_expiry")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

