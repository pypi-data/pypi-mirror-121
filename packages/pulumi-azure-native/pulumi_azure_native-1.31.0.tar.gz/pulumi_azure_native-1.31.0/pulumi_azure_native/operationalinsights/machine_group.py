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

__all__ = ['MachineGroupArgs', 'MachineGroup']

@pulumi.input_type
class MachineGroupArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 kind: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 count: Optional[pulumi.Input[int]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 group_type: Optional[pulumi.Input[Union[str, 'MachineGroupType']]] = None,
                 machine_group_name: Optional[pulumi.Input[str]] = None,
                 machines: Optional[pulumi.Input[Sequence[pulumi.Input['MachineReferenceWithHintsArgs']]]] = None):
        """
        The set of arguments for constructing a MachineGroup resource.
        :param pulumi.Input[str] display_name: User defined name for the group
        :param pulumi.Input[str] kind: Additional resource type qualifier.
               Expected value is 'machineGroup'.
        :param pulumi.Input[str] resource_group_name: Resource group name within the specified subscriptionId.
        :param pulumi.Input[str] workspace_name: OMS workspace containing the resources of interest.
        :param pulumi.Input[int] count: Count of machines in this group. The value of count may be bigger than the number of machines in case of the group has been truncated due to exceeding the max number of machines a group can handle.
        :param pulumi.Input[str] etag: Resource ETAG.
        :param pulumi.Input[Union[str, 'MachineGroupType']] group_type: Type of the machine group
        :param pulumi.Input[str] machine_group_name: Machine Group resource name.
        :param pulumi.Input[Sequence[pulumi.Input['MachineReferenceWithHintsArgs']]] machines: References of the machines in this group. The hints within each reference do not represent the current value of the corresponding fields. They are a snapshot created during the last time the machine group was updated.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "kind", 'machineGroup')
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if count is not None:
            pulumi.set(__self__, "count", count)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if group_type is not None:
            pulumi.set(__self__, "group_type", group_type)
        if machine_group_name is not None:
            pulumi.set(__self__, "machine_group_name", machine_group_name)
        if machines is not None:
            pulumi.set(__self__, "machines", machines)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        User defined name for the group
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        Additional resource type qualifier.
        Expected value is 'machineGroup'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Resource group name within the specified subscriptionId.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        OMS workspace containing the resources of interest.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        """
        Count of machines in this group. The value of count may be bigger than the number of machines in case of the group has been truncated due to exceeding the max number of machines a group can handle.
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ETAG.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter(name="groupType")
    def group_type(self) -> Optional[pulumi.Input[Union[str, 'MachineGroupType']]]:
        """
        Type of the machine group
        """
        return pulumi.get(self, "group_type")

    @group_type.setter
    def group_type(self, value: Optional[pulumi.Input[Union[str, 'MachineGroupType']]]):
        pulumi.set(self, "group_type", value)

    @property
    @pulumi.getter(name="machineGroupName")
    def machine_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Machine Group resource name.
        """
        return pulumi.get(self, "machine_group_name")

    @machine_group_name.setter
    def machine_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "machine_group_name", value)

    @property
    @pulumi.getter
    def machines(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MachineReferenceWithHintsArgs']]]]:
        """
        References of the machines in this group. The hints within each reference do not represent the current value of the corresponding fields. They are a snapshot created during the last time the machine group was updated.
        """
        return pulumi.get(self, "machines")

    @machines.setter
    def machines(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MachineReferenceWithHintsArgs']]]]):
        pulumi.set(self, "machines", value)


class MachineGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 count: Optional[pulumi.Input[int]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 group_type: Optional[pulumi.Input[Union[str, 'MachineGroupType']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 machine_group_name: Optional[pulumi.Input[str]] = None,
                 machines: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MachineReferenceWithHintsArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A user-defined logical grouping of machines.
        API Version: 2015-11-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] count: Count of machines in this group. The value of count may be bigger than the number of machines in case of the group has been truncated due to exceeding the max number of machines a group can handle.
        :param pulumi.Input[str] display_name: User defined name for the group
        :param pulumi.Input[str] etag: Resource ETAG.
        :param pulumi.Input[Union[str, 'MachineGroupType']] group_type: Type of the machine group
        :param pulumi.Input[str] kind: Additional resource type qualifier.
               Expected value is 'machineGroup'.
        :param pulumi.Input[str] machine_group_name: Machine Group resource name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MachineReferenceWithHintsArgs']]]] machines: References of the machines in this group. The hints within each reference do not represent the current value of the corresponding fields. They are a snapshot created during the last time the machine group was updated.
        :param pulumi.Input[str] resource_group_name: Resource group name within the specified subscriptionId.
        :param pulumi.Input[str] workspace_name: OMS workspace containing the resources of interest.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MachineGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A user-defined logical grouping of machines.
        API Version: 2015-11-01-preview.

        :param str resource_name: The name of the resource.
        :param MachineGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MachineGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 count: Optional[pulumi.Input[int]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 group_type: Optional[pulumi.Input[Union[str, 'MachineGroupType']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 machine_group_name: Optional[pulumi.Input[str]] = None,
                 machines: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MachineReferenceWithHintsArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = MachineGroupArgs.__new__(MachineGroupArgs)

            __props__.__dict__["count"] = count
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["etag"] = etag
            __props__.__dict__["group_type"] = group_type
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'machineGroup'
            __props__.__dict__["machine_group_name"] = machine_group_name
            __props__.__dict__["machines"] = machines
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:operationalinsights:MachineGroup"), pulumi.Alias(type_="azure-native:operationalinsights/v20151101preview:MachineGroup"), pulumi.Alias(type_="azure-nextgen:operationalinsights/v20151101preview:MachineGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MachineGroup, __self__).__init__(
            'azure-native:operationalinsights:MachineGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MachineGroup':
        """
        Get an existing MachineGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MachineGroupArgs.__new__(MachineGroupArgs)

        __props__.__dict__["count"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["group_type"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["machines"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return MachineGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def count(self) -> pulumi.Output[Optional[int]]:
        """
        Count of machines in this group. The value of count may be bigger than the number of machines in case of the group has been truncated due to exceeding the max number of machines a group can handle.
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        User defined name for the group
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Resource ETAG.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="groupType")
    def group_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of the machine group
        """
        return pulumi.get(self, "group_type")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Additional resource type qualifier.
        Expected value is 'machineGroup'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def machines(self) -> pulumi.Output[Optional[Sequence['outputs.MachineReferenceWithHintsResponse']]]:
        """
        References of the machines in this group. The hints within each reference do not represent the current value of the corresponding fields. They are a snapshot created during the last time the machine group was updated.
        """
        return pulumi.get(self, "machines")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

