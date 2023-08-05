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

__all__ = ['KpiArgs', 'Kpi']

@pulumi.input_type
class KpiArgs:
    def __init__(__self__, *,
                 calculation_window: pulumi.Input['CalculationWindowTypes'],
                 entity_type: pulumi.Input['EntityTypes'],
                 entity_type_name: pulumi.Input[str],
                 expression: pulumi.Input[str],
                 function: pulumi.Input['KpiFunctions'],
                 hub_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 aliases: Optional[pulumi.Input[Sequence[pulumi.Input['KpiAliasArgs']]]] = None,
                 calculation_window_field_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 extracts: Optional[pulumi.Input[Sequence[pulumi.Input['KpiExtractArgs']]]] = None,
                 filter: Optional[pulumi.Input[str]] = None,
                 group_by: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 kpi_name: Optional[pulumi.Input[str]] = None,
                 thres_holds: Optional[pulumi.Input['KpiThresholdsArgs']] = None,
                 unit: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Kpi resource.
        :param pulumi.Input['CalculationWindowTypes'] calculation_window: The calculation window.
        :param pulumi.Input['EntityTypes'] entity_type: The mapping entity type.
        :param pulumi.Input[str] entity_type_name: The mapping entity name.
        :param pulumi.Input[str] expression: The computation expression for the KPI.
        :param pulumi.Input['KpiFunctions'] function: The computation function for the KPI.
        :param pulumi.Input[str] hub_name: The name of the hub.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input['KpiAliasArgs']]] aliases: The aliases.
        :param pulumi.Input[str] calculation_window_field_name: Name of calculation window field.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] description: Localized description for the KPI.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] display_name: Localized display name for the KPI.
        :param pulumi.Input[Sequence[pulumi.Input['KpiExtractArgs']]] extracts: The KPI extracts.
        :param pulumi.Input[str] filter: The filter expression for the KPI.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_by: the group by properties for the KPI.
        :param pulumi.Input[str] kpi_name: The name of the KPI.
        :param pulumi.Input['KpiThresholdsArgs'] thres_holds: The KPI thresholds.
        :param pulumi.Input[str] unit: The unit of measurement for the KPI.
        """
        pulumi.set(__self__, "calculation_window", calculation_window)
        pulumi.set(__self__, "entity_type", entity_type)
        pulumi.set(__self__, "entity_type_name", entity_type_name)
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "function", function)
        pulumi.set(__self__, "hub_name", hub_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if aliases is not None:
            pulumi.set(__self__, "aliases", aliases)
        if calculation_window_field_name is not None:
            pulumi.set(__self__, "calculation_window_field_name", calculation_window_field_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if extracts is not None:
            pulumi.set(__self__, "extracts", extracts)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if group_by is not None:
            pulumi.set(__self__, "group_by", group_by)
        if kpi_name is not None:
            pulumi.set(__self__, "kpi_name", kpi_name)
        if thres_holds is not None:
            pulumi.set(__self__, "thres_holds", thres_holds)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter(name="calculationWindow")
    def calculation_window(self) -> pulumi.Input['CalculationWindowTypes']:
        """
        The calculation window.
        """
        return pulumi.get(self, "calculation_window")

    @calculation_window.setter
    def calculation_window(self, value: pulumi.Input['CalculationWindowTypes']):
        pulumi.set(self, "calculation_window", value)

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> pulumi.Input['EntityTypes']:
        """
        The mapping entity type.
        """
        return pulumi.get(self, "entity_type")

    @entity_type.setter
    def entity_type(self, value: pulumi.Input['EntityTypes']):
        pulumi.set(self, "entity_type", value)

    @property
    @pulumi.getter(name="entityTypeName")
    def entity_type_name(self) -> pulumi.Input[str]:
        """
        The mapping entity name.
        """
        return pulumi.get(self, "entity_type_name")

    @entity_type_name.setter
    def entity_type_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_type_name", value)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        """
        The computation expression for the KPI.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def function(self) -> pulumi.Input['KpiFunctions']:
        """
        The computation function for the KPI.
        """
        return pulumi.get(self, "function")

    @function.setter
    def function(self, value: pulumi.Input['KpiFunctions']):
        pulumi.set(self, "function", value)

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
    def aliases(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['KpiAliasArgs']]]]:
        """
        The aliases.
        """
        return pulumi.get(self, "aliases")

    @aliases.setter
    def aliases(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['KpiAliasArgs']]]]):
        pulumi.set(self, "aliases", value)

    @property
    @pulumi.getter(name="calculationWindowFieldName")
    def calculation_window_field_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of calculation window field.
        """
        return pulumi.get(self, "calculation_window_field_name")

    @calculation_window_field_name.setter
    def calculation_window_field_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "calculation_window_field_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Localized description for the KPI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Localized display name for the KPI.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def extracts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['KpiExtractArgs']]]]:
        """
        The KPI extracts.
        """
        return pulumi.get(self, "extracts")

    @extracts.setter
    def extracts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['KpiExtractArgs']]]]):
        pulumi.set(self, "extracts", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input[str]]:
        """
        The filter expression for the KPI.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter(name="groupBy")
    def group_by(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        the group by properties for the KPI.
        """
        return pulumi.get(self, "group_by")

    @group_by.setter
    def group_by(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "group_by", value)

    @property
    @pulumi.getter(name="kpiName")
    def kpi_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the KPI.
        """
        return pulumi.get(self, "kpi_name")

    @kpi_name.setter
    def kpi_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kpi_name", value)

    @property
    @pulumi.getter(name="thresHolds")
    def thres_holds(self) -> Optional[pulumi.Input['KpiThresholdsArgs']]:
        """
        The KPI thresholds.
        """
        return pulumi.get(self, "thres_holds")

    @thres_holds.setter
    def thres_holds(self, value: Optional[pulumi.Input['KpiThresholdsArgs']]):
        pulumi.set(self, "thres_holds", value)

    @property
    @pulumi.getter
    def unit(self) -> Optional[pulumi.Input[str]]:
        """
        The unit of measurement for the KPI.
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unit", value)


class Kpi(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aliases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KpiAliasArgs']]]]] = None,
                 calculation_window: Optional[pulumi.Input['CalculationWindowTypes']] = None,
                 calculation_window_field_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 entity_type: Optional[pulumi.Input['EntityTypes']] = None,
                 entity_type_name: Optional[pulumi.Input[str]] = None,
                 expression: Optional[pulumi.Input[str]] = None,
                 extracts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KpiExtractArgs']]]]] = None,
                 filter: Optional[pulumi.Input[str]] = None,
                 function: Optional[pulumi.Input['KpiFunctions']] = None,
                 group_by: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hub_name: Optional[pulumi.Input[str]] = None,
                 kpi_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 thres_holds: Optional[pulumi.Input[pulumi.InputType['KpiThresholdsArgs']]] = None,
                 unit: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The KPI resource format.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KpiAliasArgs']]]] aliases: The aliases.
        :param pulumi.Input['CalculationWindowTypes'] calculation_window: The calculation window.
        :param pulumi.Input[str] calculation_window_field_name: Name of calculation window field.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] description: Localized description for the KPI.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] display_name: Localized display name for the KPI.
        :param pulumi.Input['EntityTypes'] entity_type: The mapping entity type.
        :param pulumi.Input[str] entity_type_name: The mapping entity name.
        :param pulumi.Input[str] expression: The computation expression for the KPI.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KpiExtractArgs']]]] extracts: The KPI extracts.
        :param pulumi.Input[str] filter: The filter expression for the KPI.
        :param pulumi.Input['KpiFunctions'] function: The computation function for the KPI.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_by: the group by properties for the KPI.
        :param pulumi.Input[str] hub_name: The name of the hub.
        :param pulumi.Input[str] kpi_name: The name of the KPI.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['KpiThresholdsArgs']] thres_holds: The KPI thresholds.
        :param pulumi.Input[str] unit: The unit of measurement for the KPI.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KpiArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The KPI resource format.

        :param str resource_name: The name of the resource.
        :param KpiArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KpiArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aliases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KpiAliasArgs']]]]] = None,
                 calculation_window: Optional[pulumi.Input['CalculationWindowTypes']] = None,
                 calculation_window_field_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 entity_type: Optional[pulumi.Input['EntityTypes']] = None,
                 entity_type_name: Optional[pulumi.Input[str]] = None,
                 expression: Optional[pulumi.Input[str]] = None,
                 extracts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KpiExtractArgs']]]]] = None,
                 filter: Optional[pulumi.Input[str]] = None,
                 function: Optional[pulumi.Input['KpiFunctions']] = None,
                 group_by: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hub_name: Optional[pulumi.Input[str]] = None,
                 kpi_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 thres_holds: Optional[pulumi.Input[pulumi.InputType['KpiThresholdsArgs']]] = None,
                 unit: Optional[pulumi.Input[str]] = None,
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
            __props__ = KpiArgs.__new__(KpiArgs)

            __props__.__dict__["aliases"] = aliases
            if calculation_window is None and not opts.urn:
                raise TypeError("Missing required property 'calculation_window'")
            __props__.__dict__["calculation_window"] = calculation_window
            __props__.__dict__["calculation_window_field_name"] = calculation_window_field_name
            __props__.__dict__["description"] = description
            __props__.__dict__["display_name"] = display_name
            if entity_type is None and not opts.urn:
                raise TypeError("Missing required property 'entity_type'")
            __props__.__dict__["entity_type"] = entity_type
            if entity_type_name is None and not opts.urn:
                raise TypeError("Missing required property 'entity_type_name'")
            __props__.__dict__["entity_type_name"] = entity_type_name
            if expression is None and not opts.urn:
                raise TypeError("Missing required property 'expression'")
            __props__.__dict__["expression"] = expression
            __props__.__dict__["extracts"] = extracts
            __props__.__dict__["filter"] = filter
            if function is None and not opts.urn:
                raise TypeError("Missing required property 'function'")
            __props__.__dict__["function"] = function
            __props__.__dict__["group_by"] = group_by
            if hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'hub_name'")
            __props__.__dict__["hub_name"] = hub_name
            __props__.__dict__["kpi_name"] = kpi_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["thres_holds"] = thres_holds
            __props__.__dict__["unit"] = unit
            __props__.__dict__["group_by_metadata"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["participant_profiles_metadata"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["tenant_id"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:customerinsights/v20170426:Kpi"), pulumi.Alias(type_="azure-native:customerinsights:Kpi"), pulumi.Alias(type_="azure-nextgen:customerinsights:Kpi"), pulumi.Alias(type_="azure-native:customerinsights/v20170101:Kpi"), pulumi.Alias(type_="azure-nextgen:customerinsights/v20170101:Kpi")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Kpi, __self__).__init__(
            'azure-native:customerinsights/v20170426:Kpi',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Kpi':
        """
        Get an existing Kpi resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = KpiArgs.__new__(KpiArgs)

        __props__.__dict__["aliases"] = None
        __props__.__dict__["calculation_window"] = None
        __props__.__dict__["calculation_window_field_name"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["entity_type"] = None
        __props__.__dict__["entity_type_name"] = None
        __props__.__dict__["expression"] = None
        __props__.__dict__["extracts"] = None
        __props__.__dict__["filter"] = None
        __props__.__dict__["function"] = None
        __props__.__dict__["group_by"] = None
        __props__.__dict__["group_by_metadata"] = None
        __props__.__dict__["kpi_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["participant_profiles_metadata"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tenant_id"] = None
        __props__.__dict__["thres_holds"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["unit"] = None
        return Kpi(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def aliases(self) -> pulumi.Output[Optional[Sequence['outputs.KpiAliasResponse']]]:
        """
        The aliases.
        """
        return pulumi.get(self, "aliases")

    @property
    @pulumi.getter(name="calculationWindow")
    def calculation_window(self) -> pulumi.Output[str]:
        """
        The calculation window.
        """
        return pulumi.get(self, "calculation_window")

    @property
    @pulumi.getter(name="calculationWindowFieldName")
    def calculation_window_field_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of calculation window field.
        """
        return pulumi.get(self, "calculation_window_field_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Localized description for the KPI.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Localized display name for the KPI.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> pulumi.Output[str]:
        """
        The mapping entity type.
        """
        return pulumi.get(self, "entity_type")

    @property
    @pulumi.getter(name="entityTypeName")
    def entity_type_name(self) -> pulumi.Output[str]:
        """
        The mapping entity name.
        """
        return pulumi.get(self, "entity_type_name")

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Output[str]:
        """
        The computation expression for the KPI.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def extracts(self) -> pulumi.Output[Optional[Sequence['outputs.KpiExtractResponse']]]:
        """
        The KPI extracts.
        """
        return pulumi.get(self, "extracts")

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output[Optional[str]]:
        """
        The filter expression for the KPI.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def function(self) -> pulumi.Output[str]:
        """
        The computation function for the KPI.
        """
        return pulumi.get(self, "function")

    @property
    @pulumi.getter(name="groupBy")
    def group_by(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        the group by properties for the KPI.
        """
        return pulumi.get(self, "group_by")

    @property
    @pulumi.getter(name="groupByMetadata")
    def group_by_metadata(self) -> pulumi.Output[Sequence['outputs.KpiGroupByMetadataResponse']]:
        """
        The KPI GroupByMetadata.
        """
        return pulumi.get(self, "group_by_metadata")

    @property
    @pulumi.getter(name="kpiName")
    def kpi_name(self) -> pulumi.Output[str]:
        """
        The KPI name.
        """
        return pulumi.get(self, "kpi_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="participantProfilesMetadata")
    def participant_profiles_metadata(self) -> pulumi.Output[Sequence['outputs.KpiParticipantProfilesMetadataResponse']]:
        """
        The participant profiles.
        """
        return pulumi.get(self, "participant_profiles_metadata")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        The hub name.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter(name="thresHolds")
    def thres_holds(self) -> pulumi.Output[Optional['outputs.KpiThresholdsResponse']]:
        """
        The KPI thresholds.
        """
        return pulumi.get(self, "thres_holds")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def unit(self) -> pulumi.Output[Optional[str]]:
        """
        The unit of measurement for the KPI.
        """
        return pulumi.get(self, "unit")

