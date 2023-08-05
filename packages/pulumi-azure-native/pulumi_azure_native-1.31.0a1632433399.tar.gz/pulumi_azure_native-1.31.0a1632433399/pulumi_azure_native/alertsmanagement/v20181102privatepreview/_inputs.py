# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'ActionRulePropertiesArgs',
    'ConditionsArgs',
    'ConditionArgs',
    'ScopeArgs',
    'SuppressionConfigArgs',
    'SuppressionScheduleArgs',
]

@pulumi.input_type
class ActionRulePropertiesArgs:
    def __init__(__self__, *,
                 conditions: Optional[pulumi.Input['ConditionsArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input['ScopeArgs']] = None,
                 status: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]] = None,
                 suppression_config: Optional[pulumi.Input['SuppressionConfigArgs']] = None):
        """
        Action rule properties defining scope, conditions, suppression logic for action rule
        :param pulumi.Input['ConditionsArgs'] conditions: Conditions in alert instance to be matched for a given action rule. Default value is all. Multiple values could be provided with comma separation.
        :param pulumi.Input[str] description: Description of action rule
        :param pulumi.Input['ScopeArgs'] scope: Target scope for a given action rule. By default scope will be the subscription. User can also provide list of resource groups or list of resources from the scope subscription as well.
        :param pulumi.Input[Union[str, 'ActionRuleStatus']] status: Indicates if the given action rule is enabled or disabled
        :param pulumi.Input['SuppressionConfigArgs'] suppression_config: Suppression logic for a given action rule
        """
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if suppression_config is not None:
            pulumi.set(__self__, "suppression_config", suppression_config)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input['ConditionsArgs']]:
        """
        Conditions in alert instance to be matched for a given action rule. Default value is all. Multiple values could be provided with comma separation.
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input['ConditionsArgs']]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of action rule
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input['ScopeArgs']]:
        """
        Target scope for a given action rule. By default scope will be the subscription. User can also provide list of resource groups or list of resources from the scope subscription as well.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input['ScopeArgs']]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]:
        """
        Indicates if the given action rule is enabled or disabled
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="suppressionConfig")
    def suppression_config(self) -> Optional[pulumi.Input['SuppressionConfigArgs']]:
        """
        Suppression logic for a given action rule
        """
        return pulumi.get(self, "suppression_config")

    @suppression_config.setter
    def suppression_config(self, value: Optional[pulumi.Input['SuppressionConfigArgs']]):
        pulumi.set(self, "suppression_config", value)


@pulumi.input_type
class ConditionsArgs:
    def __init__(__self__, *,
                 alert_rule_id: Optional[pulumi.Input['ConditionArgs']] = None,
                 application_insights_search_results: Optional[pulumi.Input['ConditionArgs']] = None,
                 description: Optional[pulumi.Input['ConditionArgs']] = None,
                 log_analytics_search_results: Optional[pulumi.Input['ConditionArgs']] = None,
                 monitor_condition: Optional[pulumi.Input['ConditionArgs']] = None,
                 monitor_service: Optional[pulumi.Input['ConditionArgs']] = None,
                 severity: Optional[pulumi.Input['ConditionArgs']] = None,
                 signal_type: Optional[pulumi.Input['ConditionArgs']] = None,
                 target_resource: Optional[pulumi.Input['ConditionArgs']] = None,
                 target_resource_group: Optional[pulumi.Input['ConditionArgs']] = None,
                 target_resource_type: Optional[pulumi.Input['ConditionArgs']] = None):
        """
        Conditions in alert instance to be matched for a given action rule. Default value is all. Multiple values could be provided with comma separation.
        :param pulumi.Input['ConditionArgs'] alert_rule_id: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] application_insights_search_results: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] description: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] log_analytics_search_results: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] monitor_condition: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] monitor_service: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] severity: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] signal_type: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] target_resource: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] target_resource_group: condition to trigger an action rule
        :param pulumi.Input['ConditionArgs'] target_resource_type: condition to trigger an action rule
        """
        if alert_rule_id is not None:
            pulumi.set(__self__, "alert_rule_id", alert_rule_id)
        if application_insights_search_results is not None:
            pulumi.set(__self__, "application_insights_search_results", application_insights_search_results)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if log_analytics_search_results is not None:
            pulumi.set(__self__, "log_analytics_search_results", log_analytics_search_results)
        if monitor_condition is not None:
            pulumi.set(__self__, "monitor_condition", monitor_condition)
        if monitor_service is not None:
            pulumi.set(__self__, "monitor_service", monitor_service)
        if severity is not None:
            pulumi.set(__self__, "severity", severity)
        if signal_type is not None:
            pulumi.set(__self__, "signal_type", signal_type)
        if target_resource is not None:
            pulumi.set(__self__, "target_resource", target_resource)
        if target_resource_group is not None:
            pulumi.set(__self__, "target_resource_group", target_resource_group)
        if target_resource_type is not None:
            pulumi.set(__self__, "target_resource_type", target_resource_type)

    @property
    @pulumi.getter(name="alertRuleId")
    def alert_rule_id(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "alert_rule_id")

    @alert_rule_id.setter
    def alert_rule_id(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "alert_rule_id", value)

    @property
    @pulumi.getter(name="applicationInsightsSearchResults")
    def application_insights_search_results(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "application_insights_search_results")

    @application_insights_search_results.setter
    def application_insights_search_results(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "application_insights_search_results", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="logAnalyticsSearchResults")
    def log_analytics_search_results(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "log_analytics_search_results")

    @log_analytics_search_results.setter
    def log_analytics_search_results(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "log_analytics_search_results", value)

    @property
    @pulumi.getter(name="monitorCondition")
    def monitor_condition(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "monitor_condition")

    @monitor_condition.setter
    def monitor_condition(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "monitor_condition", value)

    @property
    @pulumi.getter(name="monitorService")
    def monitor_service(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "monitor_service")

    @monitor_service.setter
    def monitor_service(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "monitor_service", value)

    @property
    @pulumi.getter
    def severity(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter(name="signalType")
    def signal_type(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "signal_type")

    @signal_type.setter
    def signal_type(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "signal_type", value)

    @property
    @pulumi.getter(name="targetResource")
    def target_resource(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "target_resource")

    @target_resource.setter
    def target_resource(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "target_resource", value)

    @property
    @pulumi.getter(name="targetResourceGroup")
    def target_resource_group(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "target_resource_group")

    @target_resource_group.setter
    def target_resource_group(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "target_resource_group", value)

    @property
    @pulumi.getter(name="targetResourceType")
    def target_resource_type(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        condition to trigger an action rule
        """
        return pulumi.get(self, "target_resource_type")

    @target_resource_type.setter
    def target_resource_type(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "target_resource_type", value)


@pulumi.input_type
class ConditionArgs:
    def __init__(__self__, *,
                 operator: Optional[pulumi.Input[Union[str, 'ScopeType']]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        condition to trigger an action rule
        :param pulumi.Input[Union[str, 'ScopeType']] operator: operator for a given condition
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: list of values to match for a given condition.
        """
        if operator is not None:
            pulumi.set(__self__, "operator", operator)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def operator(self) -> Optional[pulumi.Input[Union[str, 'ScopeType']]]:
        """
        operator for a given condition
        """
        return pulumi.get(self, "operator")

    @operator.setter
    def operator(self, value: Optional[pulumi.Input[Union[str, 'ScopeType']]]):
        pulumi.set(self, "operator", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        list of values to match for a given condition.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class ScopeArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input[Union[str, 'ScopeType']]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Target scope for a given action rule. By default scope will be the subscription. User can also provide list of resource groups or list of resources from the scope subscription as well.
        :param pulumi.Input[Union[str, 'ScopeType']] type: type of target scope
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: list of ARM IDs of the given scope type which will be the target of the given action rule.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ScopeType']]]:
        """
        type of target scope
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ScopeType']]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        list of ARM IDs of the given scope type which will be the target of the given action rule.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class SuppressionConfigArgs:
    def __init__(__self__, *,
                 recurrence_type: pulumi.Input[Union[str, 'SuppressionType']],
                 schedule: Optional[pulumi.Input['SuppressionScheduleArgs']] = None):
        """
        Suppression logic for a given action rule
        :param pulumi.Input[Union[str, 'SuppressionType']] recurrence_type: Specifies when the suppression should be applied
        :param pulumi.Input['SuppressionScheduleArgs'] schedule: Schedule for a given suppression configuration.
        """
        pulumi.set(__self__, "recurrence_type", recurrence_type)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)

    @property
    @pulumi.getter(name="recurrenceType")
    def recurrence_type(self) -> pulumi.Input[Union[str, 'SuppressionType']]:
        """
        Specifies when the suppression should be applied
        """
        return pulumi.get(self, "recurrence_type")

    @recurrence_type.setter
    def recurrence_type(self, value: pulumi.Input[Union[str, 'SuppressionType']]):
        pulumi.set(self, "recurrence_type", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input['SuppressionScheduleArgs']]:
        """
        Schedule for a given suppression configuration.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input['SuppressionScheduleArgs']]):
        pulumi.set(self, "schedule", value)


@pulumi.input_type
class SuppressionScheduleArgs:
    def __init__(__self__, *,
                 end_date: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 recurrence_values: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 start_date: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None):
        """
        Schedule for a given suppression configuration.
        :param pulumi.Input[str] end_date: End date for suppression
        :param pulumi.Input[str] end_time: End date for suppression
        :param pulumi.Input[Sequence[pulumi.Input[int]]] recurrence_values: Specifies the values for recurrence pattern
        :param pulumi.Input[str] start_date: Start date for suppression
        :param pulumi.Input[str] start_time: Start time for suppression
        """
        if end_date is not None:
            pulumi.set(__self__, "end_date", end_date)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if recurrence_values is not None:
            pulumi.set(__self__, "recurrence_values", recurrence_values)
        if start_date is not None:
            pulumi.set(__self__, "start_date", start_date)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endDate")
    def end_date(self) -> Optional[pulumi.Input[str]]:
        """
        End date for suppression
        """
        return pulumi.get(self, "end_date")

    @end_date.setter
    def end_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_date", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        End date for suppression
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter(name="recurrenceValues")
    def recurrence_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        Specifies the values for recurrence pattern
        """
        return pulumi.get(self, "recurrence_values")

    @recurrence_values.setter
    def recurrence_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "recurrence_values", value)

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> Optional[pulumi.Input[str]]:
        """
        Start date for suppression
        """
        return pulumi.get(self, "start_date")

    @start_date.setter
    def start_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_date", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Start time for suppression
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)


