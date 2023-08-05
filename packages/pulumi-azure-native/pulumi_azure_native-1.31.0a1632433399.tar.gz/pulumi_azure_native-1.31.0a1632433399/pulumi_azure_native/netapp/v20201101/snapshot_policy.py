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

__all__ = ['SnapshotPolicyArgs', 'SnapshotPolicy']

@pulumi.input_type
class SnapshotPolicyArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 daily_schedule: Optional[pulumi.Input['DailyScheduleArgs']] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 hourly_schedule: Optional[pulumi.Input['HourlyScheduleArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 monthly_schedule: Optional[pulumi.Input['MonthlyScheduleArgs']] = None,
                 snapshot_policy_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 weekly_schedule: Optional[pulumi.Input['WeeklyScheduleArgs']] = None):
        """
        The set of arguments for constructing a SnapshotPolicy resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['DailyScheduleArgs'] daily_schedule: Schedule for daily snapshots
        :param pulumi.Input[bool] enabled: The property to decide policy is enabled or not
        :param pulumi.Input['HourlyScheduleArgs'] hourly_schedule: Schedule for hourly snapshots
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input['MonthlyScheduleArgs'] monthly_schedule: Schedule for monthly snapshots
        :param pulumi.Input[str] snapshot_policy_name: The name of the snapshot policy
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input['WeeklyScheduleArgs'] weekly_schedule: Schedule for weekly snapshots
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if daily_schedule is not None:
            pulumi.set(__self__, "daily_schedule", daily_schedule)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if hourly_schedule is not None:
            pulumi.set(__self__, "hourly_schedule", hourly_schedule)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if monthly_schedule is not None:
            pulumi.set(__self__, "monthly_schedule", monthly_schedule)
        if snapshot_policy_name is not None:
            pulumi.set(__self__, "snapshot_policy_name", snapshot_policy_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if weekly_schedule is not None:
            pulumi.set(__self__, "weekly_schedule", weekly_schedule)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the NetApp account
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

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
    @pulumi.getter(name="dailySchedule")
    def daily_schedule(self) -> Optional[pulumi.Input['DailyScheduleArgs']]:
        """
        Schedule for daily snapshots
        """
        return pulumi.get(self, "daily_schedule")

    @daily_schedule.setter
    def daily_schedule(self, value: Optional[pulumi.Input['DailyScheduleArgs']]):
        pulumi.set(self, "daily_schedule", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        The property to decide policy is enabled or not
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="hourlySchedule")
    def hourly_schedule(self) -> Optional[pulumi.Input['HourlyScheduleArgs']]:
        """
        Schedule for hourly snapshots
        """
        return pulumi.get(self, "hourly_schedule")

    @hourly_schedule.setter
    def hourly_schedule(self, value: Optional[pulumi.Input['HourlyScheduleArgs']]):
        pulumi.set(self, "hourly_schedule", value)

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
    @pulumi.getter(name="monthlySchedule")
    def monthly_schedule(self) -> Optional[pulumi.Input['MonthlyScheduleArgs']]:
        """
        Schedule for monthly snapshots
        """
        return pulumi.get(self, "monthly_schedule")

    @monthly_schedule.setter
    def monthly_schedule(self, value: Optional[pulumi.Input['MonthlyScheduleArgs']]):
        pulumi.set(self, "monthly_schedule", value)

    @property
    @pulumi.getter(name="snapshotPolicyName")
    def snapshot_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the snapshot policy
        """
        return pulumi.get(self, "snapshot_policy_name")

    @snapshot_policy_name.setter
    def snapshot_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_policy_name", value)

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
    @pulumi.getter(name="weeklySchedule")
    def weekly_schedule(self) -> Optional[pulumi.Input['WeeklyScheduleArgs']]:
        """
        Schedule for weekly snapshots
        """
        return pulumi.get(self, "weekly_schedule")

    @weekly_schedule.setter
    def weekly_schedule(self, value: Optional[pulumi.Input['WeeklyScheduleArgs']]):
        pulumi.set(self, "weekly_schedule", value)


class SnapshotPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 daily_schedule: Optional[pulumi.Input[pulumi.InputType['DailyScheduleArgs']]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 hourly_schedule: Optional[pulumi.Input[pulumi.InputType['HourlyScheduleArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 monthly_schedule: Optional[pulumi.Input[pulumi.InputType['MonthlyScheduleArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 snapshot_policy_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 weekly_schedule: Optional[pulumi.Input[pulumi.InputType['WeeklyScheduleArgs']]] = None,
                 __props__=None):
        """
        Snapshot policy information

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[pulumi.InputType['DailyScheduleArgs']] daily_schedule: Schedule for daily snapshots
        :param pulumi.Input[bool] enabled: The property to decide policy is enabled or not
        :param pulumi.Input[pulumi.InputType['HourlyScheduleArgs']] hourly_schedule: Schedule for hourly snapshots
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[pulumi.InputType['MonthlyScheduleArgs']] monthly_schedule: Schedule for monthly snapshots
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] snapshot_policy_name: The name of the snapshot policy
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[pulumi.InputType['WeeklyScheduleArgs']] weekly_schedule: Schedule for weekly snapshots
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SnapshotPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Snapshot policy information

        :param str resource_name: The name of the resource.
        :param SnapshotPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SnapshotPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 daily_schedule: Optional[pulumi.Input[pulumi.InputType['DailyScheduleArgs']]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 hourly_schedule: Optional[pulumi.Input[pulumi.InputType['HourlyScheduleArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 monthly_schedule: Optional[pulumi.Input[pulumi.InputType['MonthlyScheduleArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 snapshot_policy_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 weekly_schedule: Optional[pulumi.Input[pulumi.InputType['WeeklyScheduleArgs']]] = None,
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
            __props__ = SnapshotPolicyArgs.__new__(SnapshotPolicyArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["daily_schedule"] = daily_schedule
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["hourly_schedule"] = hourly_schedule
            __props__.__dict__["location"] = location
            __props__.__dict__["monthly_schedule"] = monthly_schedule
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["snapshot_policy_name"] = snapshot_policy_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["weekly_schedule"] = weekly_schedule
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:netapp/v20201101:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200501:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20200501:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200601:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20200601:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200701:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20200701:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200801:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20200801:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200901:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20200901:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20201201:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20201201:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210201:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20210201:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210401:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20210401:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210401preview:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20210401preview:SnapshotPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210601:SnapshotPolicy"), pulumi.Alias(type_="azure-nextgen:netapp/v20210601:SnapshotPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SnapshotPolicy, __self__).__init__(
            'azure-native:netapp/v20201101:SnapshotPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SnapshotPolicy':
        """
        Get an existing SnapshotPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SnapshotPolicyArgs.__new__(SnapshotPolicyArgs)

        __props__.__dict__["daily_schedule"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["hourly_schedule"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["monthly_schedule"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["weekly_schedule"] = None
        return SnapshotPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dailySchedule")
    def daily_schedule(self) -> pulumi.Output[Optional['outputs.DailyScheduleResponse']]:
        """
        Schedule for daily snapshots
        """
        return pulumi.get(self, "daily_schedule")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        The property to decide policy is enabled or not
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="hourlySchedule")
    def hourly_schedule(self) -> pulumi.Output[Optional['outputs.HourlyScheduleResponse']]:
        """
        Schedule for hourly snapshots
        """
        return pulumi.get(self, "hourly_schedule")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="monthlySchedule")
    def monthly_schedule(self) -> pulumi.Output[Optional['outputs.MonthlyScheduleResponse']]:
        """
        Schedule for monthly snapshots
        """
        return pulumi.get(self, "monthly_schedule")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Snapshot policy name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="weeklySchedule")
    def weekly_schedule(self) -> pulumi.Output[Optional['outputs.WeeklyScheduleResponse']]:
        """
        Schedule for weekly snapshots
        """
        return pulumi.get(self, "weekly_schedule")

