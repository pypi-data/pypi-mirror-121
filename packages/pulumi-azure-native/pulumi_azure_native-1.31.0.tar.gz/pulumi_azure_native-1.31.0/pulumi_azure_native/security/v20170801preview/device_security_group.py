# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['DeviceSecurityGroupArgs', 'DeviceSecurityGroup']

@pulumi.input_type
class DeviceSecurityGroupArgs:
    def __init__(__self__, *,
                 resource_id: pulumi.Input[str],
                 allowlist_rules: Optional[pulumi.Input[Sequence[pulumi.Input['AllowlistCustomAlertRuleArgs']]]] = None,
                 denylist_rules: Optional[pulumi.Input[Sequence[pulumi.Input['DenylistCustomAlertRuleArgs']]]] = None,
                 device_security_group_name: Optional[pulumi.Input[str]] = None,
                 threshold_rules: Optional[pulumi.Input[Sequence[pulumi.Input['ThresholdCustomAlertRuleArgs']]]] = None,
                 time_window_rules: Optional[pulumi.Input[Sequence[pulumi.Input['TimeWindowCustomAlertRuleArgs']]]] = None):
        """
        The set of arguments for constructing a DeviceSecurityGroup resource.
        :param pulumi.Input[str] resource_id: The identifier of the resource.
        :param pulumi.Input[Sequence[pulumi.Input['AllowlistCustomAlertRuleArgs']]] allowlist_rules: The allow-list custom alert rules.
        :param pulumi.Input[Sequence[pulumi.Input['DenylistCustomAlertRuleArgs']]] denylist_rules: The deny-list custom alert rules.
        :param pulumi.Input[str] device_security_group_name: The name of the device security group. Note that the name of the device security group is case insensitive.
        :param pulumi.Input[Sequence[pulumi.Input['ThresholdCustomAlertRuleArgs']]] threshold_rules: The list of custom alert threshold rules.
        :param pulumi.Input[Sequence[pulumi.Input['TimeWindowCustomAlertRuleArgs']]] time_window_rules: The list of custom alert time-window rules.
        """
        pulumi.set(__self__, "resource_id", resource_id)
        if allowlist_rules is not None:
            pulumi.set(__self__, "allowlist_rules", allowlist_rules)
        if denylist_rules is not None:
            pulumi.set(__self__, "denylist_rules", denylist_rules)
        if device_security_group_name is not None:
            pulumi.set(__self__, "device_security_group_name", device_security_group_name)
        if threshold_rules is not None:
            pulumi.set(__self__, "threshold_rules", threshold_rules)
        if time_window_rules is not None:
            pulumi.set(__self__, "time_window_rules", time_window_rules)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Input[str]:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_id", value)

    @property
    @pulumi.getter(name="allowlistRules")
    def allowlist_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AllowlistCustomAlertRuleArgs']]]]:
        """
        The allow-list custom alert rules.
        """
        return pulumi.get(self, "allowlist_rules")

    @allowlist_rules.setter
    def allowlist_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AllowlistCustomAlertRuleArgs']]]]):
        pulumi.set(self, "allowlist_rules", value)

    @property
    @pulumi.getter(name="denylistRules")
    def denylist_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DenylistCustomAlertRuleArgs']]]]:
        """
        The deny-list custom alert rules.
        """
        return pulumi.get(self, "denylist_rules")

    @denylist_rules.setter
    def denylist_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DenylistCustomAlertRuleArgs']]]]):
        pulumi.set(self, "denylist_rules", value)

    @property
    @pulumi.getter(name="deviceSecurityGroupName")
    def device_security_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the device security group. Note that the name of the device security group is case insensitive.
        """
        return pulumi.get(self, "device_security_group_name")

    @device_security_group_name.setter
    def device_security_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device_security_group_name", value)

    @property
    @pulumi.getter(name="thresholdRules")
    def threshold_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ThresholdCustomAlertRuleArgs']]]]:
        """
        The list of custom alert threshold rules.
        """
        return pulumi.get(self, "threshold_rules")

    @threshold_rules.setter
    def threshold_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ThresholdCustomAlertRuleArgs']]]]):
        pulumi.set(self, "threshold_rules", value)

    @property
    @pulumi.getter(name="timeWindowRules")
    def time_window_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TimeWindowCustomAlertRuleArgs']]]]:
        """
        The list of custom alert time-window rules.
        """
        return pulumi.get(self, "time_window_rules")

    @time_window_rules.setter
    def time_window_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TimeWindowCustomAlertRuleArgs']]]]):
        pulumi.set(self, "time_window_rules", value)


class DeviceSecurityGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowlist_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AllowlistCustomAlertRuleArgs']]]]] = None,
                 denylist_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DenylistCustomAlertRuleArgs']]]]] = None,
                 device_security_group_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 threshold_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThresholdCustomAlertRuleArgs']]]]] = None,
                 time_window_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeWindowCustomAlertRuleArgs']]]]] = None,
                 __props__=None):
        """
        The device security group resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AllowlistCustomAlertRuleArgs']]]] allowlist_rules: The allow-list custom alert rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DenylistCustomAlertRuleArgs']]]] denylist_rules: The deny-list custom alert rules.
        :param pulumi.Input[str] device_security_group_name: The name of the device security group. Note that the name of the device security group is case insensitive.
        :param pulumi.Input[str] resource_id: The identifier of the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThresholdCustomAlertRuleArgs']]]] threshold_rules: The list of custom alert threshold rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeWindowCustomAlertRuleArgs']]]] time_window_rules: The list of custom alert time-window rules.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeviceSecurityGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The device security group resource

        :param str resource_name: The name of the resource.
        :param DeviceSecurityGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeviceSecurityGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowlist_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AllowlistCustomAlertRuleArgs']]]]] = None,
                 denylist_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DenylistCustomAlertRuleArgs']]]]] = None,
                 device_security_group_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 threshold_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThresholdCustomAlertRuleArgs']]]]] = None,
                 time_window_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeWindowCustomAlertRuleArgs']]]]] = None,
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
            __props__ = DeviceSecurityGroupArgs.__new__(DeviceSecurityGroupArgs)

            __props__.__dict__["allowlist_rules"] = allowlist_rules
            __props__.__dict__["denylist_rules"] = denylist_rules
            __props__.__dict__["device_security_group_name"] = device_security_group_name
            if resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'resource_id'")
            __props__.__dict__["resource_id"] = resource_id
            __props__.__dict__["threshold_rules"] = threshold_rules
            __props__.__dict__["time_window_rules"] = time_window_rules
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:security/v20170801preview:DeviceSecurityGroup"), pulumi.Alias(type_="azure-native:security:DeviceSecurityGroup"), pulumi.Alias(type_="azure-nextgen:security:DeviceSecurityGroup"), pulumi.Alias(type_="azure-native:security/v20190801:DeviceSecurityGroup"), pulumi.Alias(type_="azure-nextgen:security/v20190801:DeviceSecurityGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DeviceSecurityGroup, __self__).__init__(
            'azure-native:security/v20170801preview:DeviceSecurityGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DeviceSecurityGroup':
        """
        Get an existing DeviceSecurityGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DeviceSecurityGroupArgs.__new__(DeviceSecurityGroupArgs)

        __props__.__dict__["allowlist_rules"] = None
        __props__.__dict__["denylist_rules"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["threshold_rules"] = None
        __props__.__dict__["time_window_rules"] = None
        __props__.__dict__["type"] = None
        return DeviceSecurityGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowlistRules")
    def allowlist_rules(self) -> pulumi.Output[Optional[Sequence['outputs.AllowlistCustomAlertRuleResponse']]]:
        """
        The allow-list custom alert rules.
        """
        return pulumi.get(self, "allowlist_rules")

    @property
    @pulumi.getter(name="denylistRules")
    def denylist_rules(self) -> pulumi.Output[Optional[Sequence['outputs.DenylistCustomAlertRuleResponse']]]:
        """
        The deny-list custom alert rules.
        """
        return pulumi.get(self, "denylist_rules")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="thresholdRules")
    def threshold_rules(self) -> pulumi.Output[Optional[Sequence['outputs.ThresholdCustomAlertRuleResponse']]]:
        """
        The list of custom alert threshold rules.
        """
        return pulumi.get(self, "threshold_rules")

    @property
    @pulumi.getter(name="timeWindowRules")
    def time_window_rules(self) -> pulumi.Output[Optional[Sequence['outputs.TimeWindowCustomAlertRuleResponse']]]:
        """
        The list of custom alert time-window rules.
        """
        return pulumi.get(self, "time_window_rules")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

