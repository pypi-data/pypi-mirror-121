# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AuthorizationArgs', 'Authorization']

@pulumi.input_type
class AuthorizationArgs:
    def __init__(__self__, *,
                 private_cloud_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 authorization_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Authorization resource.
        :param pulumi.Input[str] private_cloud_name: The name of the private cloud.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] authorization_name: Name of the ExpressRoute Circuit Authorization in the private cloud
        """
        pulumi.set(__self__, "private_cloud_name", private_cloud_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if authorization_name is not None:
            pulumi.set(__self__, "authorization_name", authorization_name)

    @property
    @pulumi.getter(name="privateCloudName")
    def private_cloud_name(self) -> pulumi.Input[str]:
        """
        The name of the private cloud.
        """
        return pulumi.get(self, "private_cloud_name")

    @private_cloud_name.setter
    def private_cloud_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "private_cloud_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="authorizationName")
    def authorization_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the ExpressRoute Circuit Authorization in the private cloud
        """
        return pulumi.get(self, "authorization_name")

    @authorization_name.setter
    def authorization_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorization_name", value)


class Authorization(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_name: Optional[pulumi.Input[str]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ExpressRoute Circuit Authorization
        API Version: 2020-03-20.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorization_name: Name of the ExpressRoute Circuit Authorization in the private cloud
        :param pulumi.Input[str] private_cloud_name: The name of the private cloud.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AuthorizationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ExpressRoute Circuit Authorization
        API Version: 2020-03-20.

        :param str resource_name: The name of the resource.
        :param AuthorizationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AuthorizationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_name: Optional[pulumi.Input[str]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = AuthorizationArgs.__new__(AuthorizationArgs)

            __props__.__dict__["authorization_name"] = authorization_name
            if private_cloud_name is None and not opts.urn:
                raise TypeError("Missing required property 'private_cloud_name'")
            __props__.__dict__["private_cloud_name"] = private_cloud_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["express_route_authorization_id"] = None
            __props__.__dict__["express_route_authorization_key"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:avs:Authorization"), pulumi.Alias(type_="azure-native:avs/v20200320:Authorization"), pulumi.Alias(type_="azure-nextgen:avs/v20200320:Authorization"), pulumi.Alias(type_="azure-native:avs/v20200717preview:Authorization"), pulumi.Alias(type_="azure-nextgen:avs/v20200717preview:Authorization"), pulumi.Alias(type_="azure-native:avs/v20210101preview:Authorization"), pulumi.Alias(type_="azure-nextgen:avs/v20210101preview:Authorization"), pulumi.Alias(type_="azure-native:avs/v20210601:Authorization"), pulumi.Alias(type_="azure-nextgen:avs/v20210601:Authorization")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Authorization, __self__).__init__(
            'azure-native:avs:Authorization',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Authorization':
        """
        Get an existing Authorization resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AuthorizationArgs.__new__(AuthorizationArgs)

        __props__.__dict__["express_route_authorization_id"] = None
        __props__.__dict__["express_route_authorization_key"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["type"] = None
        return Authorization(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="expressRouteAuthorizationId")
    def express_route_authorization_id(self) -> pulumi.Output[str]:
        """
        The ID of the ExpressRoute Circuit Authorization
        """
        return pulumi.get(self, "express_route_authorization_id")

    @property
    @pulumi.getter(name="expressRouteAuthorizationKey")
    def express_route_authorization_key(self) -> pulumi.Output[str]:
        """
        The key of the ExpressRoute Circuit Authorization
        """
        return pulumi.get(self, "express_route_authorization_key")

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
        The state of the  ExpressRoute Circuit Authorization provisioning
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

