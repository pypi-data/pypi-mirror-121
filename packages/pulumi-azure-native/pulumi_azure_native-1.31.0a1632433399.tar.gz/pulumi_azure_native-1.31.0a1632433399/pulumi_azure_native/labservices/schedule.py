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

__all__ = ['ScheduleArgs', 'Schedule']

@pulumi.input_type
class ScheduleArgs:
    def __init__(__self__, *,
                 lab_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 stop_at: pulumi.Input[str],
                 time_zone_id: pulumi.Input[str],
                 notes: Optional[pulumi.Input[str]] = None,
                 recurrence_pattern: Optional[pulumi.Input['RecurrencePatternArgs']] = None,
                 schedule_name: Optional[pulumi.Input[str]] = None,
                 start_at: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Schedule resource.
        :param pulumi.Input[str] lab_name: The name of the lab that uniquely identifies it within containing lab account. Used in resource URIs.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] stop_at: When lab user virtual machines will be stopped. Timestamp offsets will be ignored and timeZoneId is used instead.
        :param pulumi.Input[str] time_zone_id: The IANA timezone id for the schedule.
        :param pulumi.Input[str] notes: Notes for this schedule.
        :param pulumi.Input['RecurrencePatternArgs'] recurrence_pattern: The recurrence pattern of the scheduled actions.
        :param pulumi.Input[str] schedule_name: The name of the schedule that uniquely identifies it within containing lab. Used in resource URIs.
        :param pulumi.Input[str] start_at: When lab user virtual machines will be started. Timestamp offsets will be ignored and timeZoneId is used instead.
        """
        pulumi.set(__self__, "lab_name", lab_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "stop_at", stop_at)
        pulumi.set(__self__, "time_zone_id", time_zone_id)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if recurrence_pattern is not None:
            pulumi.set(__self__, "recurrence_pattern", recurrence_pattern)
        if schedule_name is not None:
            pulumi.set(__self__, "schedule_name", schedule_name)
        if start_at is not None:
            pulumi.set(__self__, "start_at", start_at)

    @property
    @pulumi.getter(name="labName")
    def lab_name(self) -> pulumi.Input[str]:
        """
        The name of the lab that uniquely identifies it within containing lab account. Used in resource URIs.
        """
        return pulumi.get(self, "lab_name")

    @lab_name.setter
    def lab_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "lab_name", value)

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
    @pulumi.getter(name="stopAt")
    def stop_at(self) -> pulumi.Input[str]:
        """
        When lab user virtual machines will be stopped. Timestamp offsets will be ignored and timeZoneId is used instead.
        """
        return pulumi.get(self, "stop_at")

    @stop_at.setter
    def stop_at(self, value: pulumi.Input[str]):
        pulumi.set(self, "stop_at", value)

    @property
    @pulumi.getter(name="timeZoneId")
    def time_zone_id(self) -> pulumi.Input[str]:
        """
        The IANA timezone id for the schedule.
        """
        return pulumi.get(self, "time_zone_id")

    @time_zone_id.setter
    def time_zone_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "time_zone_id", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        """
        Notes for this schedule.
        """
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter(name="recurrencePattern")
    def recurrence_pattern(self) -> Optional[pulumi.Input['RecurrencePatternArgs']]:
        """
        The recurrence pattern of the scheduled actions.
        """
        return pulumi.get(self, "recurrence_pattern")

    @recurrence_pattern.setter
    def recurrence_pattern(self, value: Optional[pulumi.Input['RecurrencePatternArgs']]):
        pulumi.set(self, "recurrence_pattern", value)

    @property
    @pulumi.getter(name="scheduleName")
    def schedule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the schedule that uniquely identifies it within containing lab. Used in resource URIs.
        """
        return pulumi.get(self, "schedule_name")

    @schedule_name.setter
    def schedule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule_name", value)

    @property
    @pulumi.getter(name="startAt")
    def start_at(self) -> Optional[pulumi.Input[str]]:
        """
        When lab user virtual machines will be started. Timestamp offsets will be ignored and timeZoneId is used instead.
        """
        return pulumi.get(self, "start_at")

    @start_at.setter
    def start_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_at", value)


class Schedule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 lab_name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 recurrence_pattern: Optional[pulumi.Input[pulumi.InputType['RecurrencePatternArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule_name: Optional[pulumi.Input[str]] = None,
                 start_at: Optional[pulumi.Input[str]] = None,
                 stop_at: Optional[pulumi.Input[str]] = None,
                 time_zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Schedule for automatically turning virtual machines in a lab on and off at specified times.
        API Version: 2021-10-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] lab_name: The name of the lab that uniquely identifies it within containing lab account. Used in resource URIs.
        :param pulumi.Input[str] notes: Notes for this schedule.
        :param pulumi.Input[pulumi.InputType['RecurrencePatternArgs']] recurrence_pattern: The recurrence pattern of the scheduled actions.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] schedule_name: The name of the schedule that uniquely identifies it within containing lab. Used in resource URIs.
        :param pulumi.Input[str] start_at: When lab user virtual machines will be started. Timestamp offsets will be ignored and timeZoneId is used instead.
        :param pulumi.Input[str] stop_at: When lab user virtual machines will be stopped. Timestamp offsets will be ignored and timeZoneId is used instead.
        :param pulumi.Input[str] time_zone_id: The IANA timezone id for the schedule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScheduleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Schedule for automatically turning virtual machines in a lab on and off at specified times.
        API Version: 2021-10-01-preview.

        :param str resource_name: The name of the resource.
        :param ScheduleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScheduleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 lab_name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 recurrence_pattern: Optional[pulumi.Input[pulumi.InputType['RecurrencePatternArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule_name: Optional[pulumi.Input[str]] = None,
                 start_at: Optional[pulumi.Input[str]] = None,
                 stop_at: Optional[pulumi.Input[str]] = None,
                 time_zone_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = ScheduleArgs.__new__(ScheduleArgs)

            if lab_name is None and not opts.urn:
                raise TypeError("Missing required property 'lab_name'")
            __props__.__dict__["lab_name"] = lab_name
            __props__.__dict__["notes"] = notes
            __props__.__dict__["recurrence_pattern"] = recurrence_pattern
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["schedule_name"] = schedule_name
            __props__.__dict__["start_at"] = start_at
            if stop_at is None and not opts.urn:
                raise TypeError("Missing required property 'stop_at'")
            __props__.__dict__["stop_at"] = stop_at
            if time_zone_id is None and not opts.urn:
                raise TypeError("Missing required property 'time_zone_id'")
            __props__.__dict__["time_zone_id"] = time_zone_id
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:labservices:Schedule"), pulumi.Alias(type_="azure-native:labservices/v20211001preview:Schedule"), pulumi.Alias(type_="azure-nextgen:labservices/v20211001preview:Schedule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Schedule, __self__).__init__(
            'azure-native:labservices:Schedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Schedule':
        """
        Get an existing Schedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ScheduleArgs.__new__(ScheduleArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["notes"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["recurrence_pattern"] = None
        __props__.__dict__["start_at"] = None
        __props__.__dict__["stop_at"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["time_zone_id"] = None
        __props__.__dict__["type"] = None
        return Schedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def notes(self) -> pulumi.Output[Optional[str]]:
        """
        Notes for this schedule.
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Current provisioning state of the schedule.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="recurrencePattern")
    def recurrence_pattern(self) -> pulumi.Output[Optional['outputs.RecurrencePatternResponse']]:
        """
        The recurrence pattern of the scheduled actions.
        """
        return pulumi.get(self, "recurrence_pattern")

    @property
    @pulumi.getter(name="startAt")
    def start_at(self) -> pulumi.Output[Optional[str]]:
        """
        When lab user virtual machines will be started. Timestamp offsets will be ignored and timeZoneId is used instead.
        """
        return pulumi.get(self, "start_at")

    @property
    @pulumi.getter(name="stopAt")
    def stop_at(self) -> pulumi.Output[str]:
        """
        When lab user virtual machines will be stopped. Timestamp offsets will be ignored and timeZoneId is used instead.
        """
        return pulumi.get(self, "stop_at")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the schedule.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="timeZoneId")
    def time_zone_id(self) -> pulumi.Output[str]:
        """
        The IANA timezone id for the schedule.
        """
        return pulumi.get(self, "time_zone_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

