# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['WorkspaceSettingArgs', 'WorkspaceSetting']

@pulumi.input_type
class WorkspaceSettingArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 workspace_id: pulumi.Input[str],
                 workspace_setting_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WorkspaceSetting resource.
        :param pulumi.Input[str] scope: All the VMs in this scope will send their security data to the mentioned workspace unless overridden by a setting with more specific scope
        :param pulumi.Input[str] workspace_id: The full Azure ID of the workspace to save the data in
        :param pulumi.Input[str] workspace_setting_name: Name of the security setting
        """
        pulumi.set(__self__, "scope", scope)
        pulumi.set(__self__, "workspace_id", workspace_id)
        if workspace_setting_name is not None:
            pulumi.set(__self__, "workspace_setting_name", workspace_setting_name)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        All the VMs in this scope will send their security data to the mentioned workspace unless overridden by a setting with more specific scope
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Input[str]:
        """
        The full Azure ID of the workspace to save the data in
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_id", value)

    @property
    @pulumi.getter(name="workspaceSettingName")
    def workspace_setting_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the security setting
        """
        return pulumi.get(self, "workspace_setting_name")

    @workspace_setting_name.setter
    def workspace_setting_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_setting_name", value)


class WorkspaceSetting(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 workspace_setting_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Configures where to store the OMS agent data for workspaces under a scope

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] scope: All the VMs in this scope will send their security data to the mentioned workspace unless overridden by a setting with more specific scope
        :param pulumi.Input[str] workspace_id: The full Azure ID of the workspace to save the data in
        :param pulumi.Input[str] workspace_setting_name: Name of the security setting
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WorkspaceSettingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Configures where to store the OMS agent data for workspaces under a scope

        :param str resource_name: The name of the resource.
        :param WorkspaceSettingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkspaceSettingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 workspace_setting_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = WorkspaceSettingArgs.__new__(WorkspaceSettingArgs)

            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            if workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_id'")
            __props__.__dict__["workspace_id"] = workspace_id
            __props__.__dict__["workspace_setting_name"] = workspace_setting_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:security/v20170801preview:WorkspaceSetting"), pulumi.Alias(type_="azure-native:security:WorkspaceSetting"), pulumi.Alias(type_="azure-nextgen:security:WorkspaceSetting")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WorkspaceSetting, __self__).__init__(
            'azure-native:security/v20170801preview:WorkspaceSetting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WorkspaceSetting':
        """
        Get an existing WorkspaceSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WorkspaceSettingArgs.__new__(WorkspaceSettingArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["scope"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["workspace_id"] = None
        return WorkspaceSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[str]:
        """
        All the VMs in this scope will send their security data to the mentioned workspace unless overridden by a setting with more specific scope
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[str]:
        """
        The full Azure ID of the workspace to save the data in
        """
        return pulumi.get(self, "workspace_id")

