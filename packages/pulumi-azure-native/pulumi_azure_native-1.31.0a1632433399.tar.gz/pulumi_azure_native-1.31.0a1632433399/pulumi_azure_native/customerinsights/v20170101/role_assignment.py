# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['RoleAssignmentArgs', 'RoleAssignment']

@pulumi.input_type
class RoleAssignmentArgs:
    def __init__(__self__, *,
                 hub_name: pulumi.Input[str],
                 principals: pulumi.Input[Sequence[pulumi.Input['AssignmentPrincipalArgs']]],
                 resource_group_name: pulumi.Input[str],
                 role: pulumi.Input['RoleTypes'],
                 assignment_name: Optional[pulumi.Input[str]] = None,
                 conflation_policies: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 connectors: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 description: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 interactions: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 kpis: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 links: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 profiles: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 relationship_links: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 relationships: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 role_assignments: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 sas_policies: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 segments: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 views: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None,
                 widget_types: Optional[pulumi.Input['ResourceSetDescriptionArgs']] = None):
        """
        The set of arguments for constructing a RoleAssignment resource.
        :param pulumi.Input[str] hub_name: The name of the hub.
        :param pulumi.Input[Sequence[pulumi.Input['AssignmentPrincipalArgs']]] principals: The principals being assigned to.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['RoleTypes'] role: Type of roles.
        :param pulumi.Input[str] assignment_name: The assignment name
        :param pulumi.Input['ResourceSetDescriptionArgs'] conflation_policies: Widget types set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] connectors: Connectors set for the assignment.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] description: Localized description for the metadata.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] display_name: Localized display names for the metadata.
        :param pulumi.Input['ResourceSetDescriptionArgs'] interactions: Interactions set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] kpis: Kpis set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] links: Links set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] profiles: Profiles set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] relationship_links: The Role assignments set for the relationship links.
        :param pulumi.Input['ResourceSetDescriptionArgs'] relationships: The Role assignments set for the relationships.
        :param pulumi.Input['ResourceSetDescriptionArgs'] role_assignments: The Role assignments set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] sas_policies: Sas Policies set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] segments: The Role assignments set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] views: Views set for the assignment.
        :param pulumi.Input['ResourceSetDescriptionArgs'] widget_types: Widget types set for the assignment.
        """
        pulumi.set(__self__, "hub_name", hub_name)
        pulumi.set(__self__, "principals", principals)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "role", role)
        if assignment_name is not None:
            pulumi.set(__self__, "assignment_name", assignment_name)
        if conflation_policies is not None:
            pulumi.set(__self__, "conflation_policies", conflation_policies)
        if connectors is not None:
            pulumi.set(__self__, "connectors", connectors)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if interactions is not None:
            pulumi.set(__self__, "interactions", interactions)
        if kpis is not None:
            pulumi.set(__self__, "kpis", kpis)
        if links is not None:
            pulumi.set(__self__, "links", links)
        if profiles is not None:
            pulumi.set(__self__, "profiles", profiles)
        if relationship_links is not None:
            pulumi.set(__self__, "relationship_links", relationship_links)
        if relationships is not None:
            pulumi.set(__self__, "relationships", relationships)
        if role_assignments is not None:
            pulumi.set(__self__, "role_assignments", role_assignments)
        if sas_policies is not None:
            pulumi.set(__self__, "sas_policies", sas_policies)
        if segments is not None:
            pulumi.set(__self__, "segments", segments)
        if views is not None:
            pulumi.set(__self__, "views", views)
        if widget_types is not None:
            pulumi.set(__self__, "widget_types", widget_types)

    @property
    @pulumi.getter(name="hubName")
    def hub_name(self) -> pulumi.Input[str]:
        """
        The name of the hub.
        """
        return pulumi.get(self, "hub_name")

    @hub_name.setter
    def hub_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "hub_name", value)

    @property
    @pulumi.getter
    def principals(self) -> pulumi.Input[Sequence[pulumi.Input['AssignmentPrincipalArgs']]]:
        """
        The principals being assigned to.
        """
        return pulumi.get(self, "principals")

    @principals.setter
    def principals(self, value: pulumi.Input[Sequence[pulumi.Input['AssignmentPrincipalArgs']]]):
        pulumi.set(self, "principals", value)

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
    def role(self) -> pulumi.Input['RoleTypes']:
        """
        Type of roles.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input['RoleTypes']):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter(name="assignmentName")
    def assignment_name(self) -> Optional[pulumi.Input[str]]:
        """
        The assignment name
        """
        return pulumi.get(self, "assignment_name")

    @assignment_name.setter
    def assignment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "assignment_name", value)

    @property
    @pulumi.getter(name="conflationPolicies")
    def conflation_policies(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Widget types set for the assignment.
        """
        return pulumi.get(self, "conflation_policies")

    @conflation_policies.setter
    def conflation_policies(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "conflation_policies", value)

    @property
    @pulumi.getter
    def connectors(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Connectors set for the assignment.
        """
        return pulumi.get(self, "connectors")

    @connectors.setter
    def connectors(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "connectors", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Localized description for the metadata.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Localized display names for the metadata.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def interactions(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Interactions set for the assignment.
        """
        return pulumi.get(self, "interactions")

    @interactions.setter
    def interactions(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "interactions", value)

    @property
    @pulumi.getter
    def kpis(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Kpis set for the assignment.
        """
        return pulumi.get(self, "kpis")

    @kpis.setter
    def kpis(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "kpis", value)

    @property
    @pulumi.getter
    def links(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Links set for the assignment.
        """
        return pulumi.get(self, "links")

    @links.setter
    def links(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "links", value)

    @property
    @pulumi.getter
    def profiles(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Profiles set for the assignment.
        """
        return pulumi.get(self, "profiles")

    @profiles.setter
    def profiles(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "profiles", value)

    @property
    @pulumi.getter(name="relationshipLinks")
    def relationship_links(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        The Role assignments set for the relationship links.
        """
        return pulumi.get(self, "relationship_links")

    @relationship_links.setter
    def relationship_links(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "relationship_links", value)

    @property
    @pulumi.getter
    def relationships(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        The Role assignments set for the relationships.
        """
        return pulumi.get(self, "relationships")

    @relationships.setter
    def relationships(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "relationships", value)

    @property
    @pulumi.getter(name="roleAssignments")
    def role_assignments(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        The Role assignments set for the assignment.
        """
        return pulumi.get(self, "role_assignments")

    @role_assignments.setter
    def role_assignments(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "role_assignments", value)

    @property
    @pulumi.getter(name="sasPolicies")
    def sas_policies(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Sas Policies set for the assignment.
        """
        return pulumi.get(self, "sas_policies")

    @sas_policies.setter
    def sas_policies(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "sas_policies", value)

    @property
    @pulumi.getter
    def segments(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        The Role assignments set for the assignment.
        """
        return pulumi.get(self, "segments")

    @segments.setter
    def segments(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "segments", value)

    @property
    @pulumi.getter
    def views(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Views set for the assignment.
        """
        return pulumi.get(self, "views")

    @views.setter
    def views(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "views", value)

    @property
    @pulumi.getter(name="widgetTypes")
    def widget_types(self) -> Optional[pulumi.Input['ResourceSetDescriptionArgs']]:
        """
        Widget types set for the assignment.
        """
        return pulumi.get(self, "widget_types")

    @widget_types.setter
    def widget_types(self, value: Optional[pulumi.Input['ResourceSetDescriptionArgs']]):
        pulumi.set(self, "widget_types", value)


class RoleAssignment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assignment_name: Optional[pulumi.Input[str]] = None,
                 conflation_policies: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 connectors: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 description: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 hub_name: Optional[pulumi.Input[str]] = None,
                 interactions: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 kpis: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 links: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AssignmentPrincipalArgs']]]]] = None,
                 profiles: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 relationship_links: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 relationships: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input['RoleTypes']] = None,
                 role_assignments: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 sas_policies: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 segments: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 views: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 widget_types: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 __props__=None):
        """
        The Role Assignment resource format.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] assignment_name: The assignment name
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] conflation_policies: Widget types set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] connectors: Connectors set for the assignment.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] description: Localized description for the metadata.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] display_name: Localized display names for the metadata.
        :param pulumi.Input[str] hub_name: The name of the hub.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] interactions: Interactions set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] kpis: Kpis set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] links: Links set for the assignment.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AssignmentPrincipalArgs']]]] principals: The principals being assigned to.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] profiles: Profiles set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] relationship_links: The Role assignments set for the relationship links.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] relationships: The Role assignments set for the relationships.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['RoleTypes'] role: Type of roles.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] role_assignments: The Role assignments set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] sas_policies: Sas Policies set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] segments: The Role assignments set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] views: Views set for the assignment.
        :param pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']] widget_types: Widget types set for the assignment.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RoleAssignmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Role Assignment resource format.

        :param str resource_name: The name of the resource.
        :param RoleAssignmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RoleAssignmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assignment_name: Optional[pulumi.Input[str]] = None,
                 conflation_policies: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 connectors: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 description: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 hub_name: Optional[pulumi.Input[str]] = None,
                 interactions: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 kpis: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 links: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AssignmentPrincipalArgs']]]]] = None,
                 profiles: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 relationship_links: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 relationships: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input['RoleTypes']] = None,
                 role_assignments: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 sas_policies: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 segments: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 views: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
                 widget_types: Optional[pulumi.Input[pulumi.InputType['ResourceSetDescriptionArgs']]] = None,
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
            __props__ = RoleAssignmentArgs.__new__(RoleAssignmentArgs)

            __props__.__dict__["assignment_name"] = assignment_name
            __props__.__dict__["conflation_policies"] = conflation_policies
            __props__.__dict__["connectors"] = connectors
            __props__.__dict__["description"] = description
            __props__.__dict__["display_name"] = display_name
            if hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'hub_name'")
            __props__.__dict__["hub_name"] = hub_name
            __props__.__dict__["interactions"] = interactions
            __props__.__dict__["kpis"] = kpis
            __props__.__dict__["links"] = links
            if principals is None and not opts.urn:
                raise TypeError("Missing required property 'principals'")
            __props__.__dict__["principals"] = principals
            __props__.__dict__["profiles"] = profiles
            __props__.__dict__["relationship_links"] = relationship_links
            __props__.__dict__["relationships"] = relationships
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["role_assignments"] = role_assignments
            __props__.__dict__["sas_policies"] = sas_policies
            __props__.__dict__["segments"] = segments
            __props__.__dict__["views"] = views
            __props__.__dict__["widget_types"] = widget_types
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["tenant_id"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:customerinsights/v20170101:RoleAssignment"), pulumi.Alias(type_="azure-native:customerinsights:RoleAssignment"), pulumi.Alias(type_="azure-nextgen:customerinsights:RoleAssignment"), pulumi.Alias(type_="azure-native:customerinsights/v20170426:RoleAssignment"), pulumi.Alias(type_="azure-nextgen:customerinsights/v20170426:RoleAssignment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(RoleAssignment, __self__).__init__(
            'azure-native:customerinsights/v20170101:RoleAssignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RoleAssignment':
        """
        Get an existing RoleAssignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RoleAssignmentArgs.__new__(RoleAssignmentArgs)

        __props__.__dict__["assignment_name"] = None
        __props__.__dict__["conflation_policies"] = None
        __props__.__dict__["connectors"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["interactions"] = None
        __props__.__dict__["kpis"] = None
        __props__.__dict__["links"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["principals"] = None
        __props__.__dict__["profiles"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["relationship_links"] = None
        __props__.__dict__["relationships"] = None
        __props__.__dict__["role"] = None
        __props__.__dict__["role_assignments"] = None
        __props__.__dict__["sas_policies"] = None
        __props__.__dict__["segments"] = None
        __props__.__dict__["tenant_id"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["views"] = None
        __props__.__dict__["widget_types"] = None
        return RoleAssignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="assignmentName")
    def assignment_name(self) -> pulumi.Output[str]:
        """
        The name of the metadata object.
        """
        return pulumi.get(self, "assignment_name")

    @property
    @pulumi.getter(name="conflationPolicies")
    def conflation_policies(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Widget types set for the assignment.
        """
        return pulumi.get(self, "conflation_policies")

    @property
    @pulumi.getter
    def connectors(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Connectors set for the assignment.
        """
        return pulumi.get(self, "connectors")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Localized description for the metadata.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Localized display names for the metadata.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def interactions(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Interactions set for the assignment.
        """
        return pulumi.get(self, "interactions")

    @property
    @pulumi.getter
    def kpis(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Kpis set for the assignment.
        """
        return pulumi.get(self, "kpis")

    @property
    @pulumi.getter
    def links(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Links set for the assignment.
        """
        return pulumi.get(self, "links")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def principals(self) -> pulumi.Output[Sequence['outputs.AssignmentPrincipalResponse']]:
        """
        The principals being assigned to.
        """
        return pulumi.get(self, "principals")

    @property
    @pulumi.getter
    def profiles(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Profiles set for the assignment.
        """
        return pulumi.get(self, "profiles")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="relationshipLinks")
    def relationship_links(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        The Role assignments set for the relationship links.
        """
        return pulumi.get(self, "relationship_links")

    @property
    @pulumi.getter
    def relationships(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        The Role assignments set for the relationships.
        """
        return pulumi.get(self, "relationships")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        Type of roles.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter(name="roleAssignments")
    def role_assignments(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        The Role assignments set for the assignment.
        """
        return pulumi.get(self, "role_assignments")

    @property
    @pulumi.getter(name="sasPolicies")
    def sas_policies(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Sas Policies set for the assignment.
        """
        return pulumi.get(self, "sas_policies")

    @property
    @pulumi.getter
    def segments(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        The Role assignments set for the assignment.
        """
        return pulumi.get(self, "segments")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        The hub name.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def views(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Views set for the assignment.
        """
        return pulumi.get(self, "views")

    @property
    @pulumi.getter(name="widgetTypes")
    def widget_types(self) -> pulumi.Output[Optional['outputs.ResourceSetDescriptionResponse']]:
        """
        Widget types set for the assignment.
        """
        return pulumi.get(self, "widget_types")

