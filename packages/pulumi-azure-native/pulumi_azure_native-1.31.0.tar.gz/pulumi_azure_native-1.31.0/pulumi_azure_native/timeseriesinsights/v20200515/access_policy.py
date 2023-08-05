# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['AccessPolicyArgs', 'AccessPolicy']

@pulumi.input_type
class AccessPolicyArgs:
    def __init__(__self__, *,
                 environment_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 access_policy_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 principal_object_id: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AccessPolicyRole']]]]] = None):
        """
        The set of arguments for constructing a AccessPolicy resource.
        :param pulumi.Input[str] environment_name: The name of the Time Series Insights environment associated with the specified resource group.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[str] access_policy_name: Name of the access policy.
        :param pulumi.Input[str] description: An description of the access policy.
        :param pulumi.Input[str] principal_object_id: The objectId of the principal in Azure Active Directory.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AccessPolicyRole']]]] roles: The list of roles the principal is assigned on the environment.
        """
        pulumi.set(__self__, "environment_name", environment_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if access_policy_name is not None:
            pulumi.set(__self__, "access_policy_name", access_policy_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if principal_object_id is not None:
            pulumi.set(__self__, "principal_object_id", principal_object_id)
        if roles is not None:
            pulumi.set(__self__, "roles", roles)

    @property
    @pulumi.getter(name="environmentName")
    def environment_name(self) -> pulumi.Input[str]:
        """
        The name of the Time Series Insights environment associated with the specified resource group.
        """
        return pulumi.get(self, "environment_name")

    @environment_name.setter
    def environment_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "environment_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of an Azure Resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="accessPolicyName")
    def access_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the access policy.
        """
        return pulumi.get(self, "access_policy_name")

    @access_policy_name.setter
    def access_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_policy_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An description of the access policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="principalObjectId")
    def principal_object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The objectId of the principal in Azure Active Directory.
        """
        return pulumi.get(self, "principal_object_id")

    @principal_object_id.setter
    def principal_object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_object_id", value)

    @property
    @pulumi.getter
    def roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AccessPolicyRole']]]]]:
        """
        The list of roles the principal is assigned on the environment.
        """
        return pulumi.get(self, "roles")

    @roles.setter
    def roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AccessPolicyRole']]]]]):
        pulumi.set(self, "roles", value)


class AccessPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_name: Optional[pulumi.Input[str]] = None,
                 principal_object_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AccessPolicyRole']]]]] = None,
                 __props__=None):
        """
        An access policy is used to grant users and applications access to the environment. Roles are assigned to service principals in Azure Active Directory. These roles define the actions the principal can perform through the Time Series Insights data plane APIs.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_policy_name: Name of the access policy.
        :param pulumi.Input[str] description: An description of the access policy.
        :param pulumi.Input[str] environment_name: The name of the Time Series Insights environment associated with the specified resource group.
        :param pulumi.Input[str] principal_object_id: The objectId of the principal in Azure Active Directory.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AccessPolicyRole']]]] roles: The list of roles the principal is assigned on the environment.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccessPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An access policy is used to grant users and applications access to the environment. Roles are assigned to service principals in Azure Active Directory. These roles define the actions the principal can perform through the Time Series Insights data plane APIs.

        :param str resource_name: The name of the resource.
        :param AccessPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_name: Optional[pulumi.Input[str]] = None,
                 principal_object_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AccessPolicyRole']]]]] = None,
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
            __props__ = AccessPolicyArgs.__new__(AccessPolicyArgs)

            __props__.__dict__["access_policy_name"] = access_policy_name
            __props__.__dict__["description"] = description
            if environment_name is None and not opts.urn:
                raise TypeError("Missing required property 'environment_name'")
            __props__.__dict__["environment_name"] = environment_name
            __props__.__dict__["principal_object_id"] = principal_object_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["roles"] = roles
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:timeseriesinsights/v20200515:AccessPolicy"), pulumi.Alias(type_="azure-native:timeseriesinsights:AccessPolicy"), pulumi.Alias(type_="azure-nextgen:timeseriesinsights:AccessPolicy"), pulumi.Alias(type_="azure-native:timeseriesinsights/v20170228preview:AccessPolicy"), pulumi.Alias(type_="azure-nextgen:timeseriesinsights/v20170228preview:AccessPolicy"), pulumi.Alias(type_="azure-native:timeseriesinsights/v20171115:AccessPolicy"), pulumi.Alias(type_="azure-nextgen:timeseriesinsights/v20171115:AccessPolicy"), pulumi.Alias(type_="azure-native:timeseriesinsights/v20180815preview:AccessPolicy"), pulumi.Alias(type_="azure-nextgen:timeseriesinsights/v20180815preview:AccessPolicy"), pulumi.Alias(type_="azure-native:timeseriesinsights/v20210630preview:AccessPolicy"), pulumi.Alias(type_="azure-nextgen:timeseriesinsights/v20210630preview:AccessPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AccessPolicy, __self__).__init__(
            'azure-native:timeseriesinsights/v20200515:AccessPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AccessPolicy':
        """
        Get an existing AccessPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AccessPolicyArgs.__new__(AccessPolicyArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["principal_object_id"] = None
        __props__.__dict__["roles"] = None
        __props__.__dict__["type"] = None
        return AccessPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An description of the access policy.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="principalObjectId")
    def principal_object_id(self) -> pulumi.Output[Optional[str]]:
        """
        The objectId of the principal in Azure Active Directory.
        """
        return pulumi.get(self, "principal_object_id")

    @property
    @pulumi.getter
    def roles(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of roles the principal is assigned on the environment.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

