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

__all__ = [
    'CustomRuleListResponse',
    'CustomRuleResponse',
    'FrontDoorManagedRuleGroupOverrideResponse',
    'FrontDoorManagedRuleOverrideResponse',
    'FrontDoorManagedRuleSetResponse',
    'FrontDoorMatchConditionResponse',
    'FrontDoorPolicySettingsResponse',
    'FrontendEndpointLinkResponse',
    'ManagedRuleExclusionResponse',
    'ManagedRuleSetListResponse',
]

@pulumi.output_type
class CustomRuleListResponse(dict):
    """
    Defines contents of custom rules
    """
    def __init__(__self__, *,
                 rules: Optional[Sequence['outputs.CustomRuleResponse']] = None):
        """
        Defines contents of custom rules
        :param Sequence['CustomRuleResponse'] rules: List of rules
        """
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.CustomRuleResponse']]:
        """
        List of rules
        """
        return pulumi.get(self, "rules")


@pulumi.output_type
class CustomRuleResponse(dict):
    """
    Defines contents of a web application rule
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "matchConditions":
            suggest = "match_conditions"
        elif key == "ruleType":
            suggest = "rule_type"
        elif key == "enabledState":
            suggest = "enabled_state"
        elif key == "rateLimitDurationInMinutes":
            suggest = "rate_limit_duration_in_minutes"
        elif key == "rateLimitThreshold":
            suggest = "rate_limit_threshold"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomRuleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomRuleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomRuleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action: str,
                 match_conditions: Sequence['outputs.FrontDoorMatchConditionResponse'],
                 priority: int,
                 rule_type: str,
                 enabled_state: Optional[str] = None,
                 name: Optional[str] = None,
                 rate_limit_duration_in_minutes: Optional[int] = None,
                 rate_limit_threshold: Optional[int] = None):
        """
        Defines contents of a web application rule
        :param str action: Describes what action to be applied when rule matches.
        :param Sequence['FrontDoorMatchConditionResponse'] match_conditions: List of match conditions.
        :param int priority: Describes priority of the rule. Rules with a lower value will be evaluated before rules with a higher value.
        :param str rule_type: Describes type of rule.
        :param str enabled_state: Describes if the custom rule is in enabled or disabled state. Defaults to Enabled if not specified.
        :param str name: Describes the name of the rule.
        :param int rate_limit_duration_in_minutes: Time window for resetting the rate limit count. Default is 1 minute.
        :param int rate_limit_threshold: Number of allowed requests per client within the time window.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "match_conditions", match_conditions)
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "rule_type", rule_type)
        if enabled_state is not None:
            pulumi.set(__self__, "enabled_state", enabled_state)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rate_limit_duration_in_minutes is not None:
            pulumi.set(__self__, "rate_limit_duration_in_minutes", rate_limit_duration_in_minutes)
        if rate_limit_threshold is not None:
            pulumi.set(__self__, "rate_limit_threshold", rate_limit_threshold)

    @property
    @pulumi.getter
    def action(self) -> str:
        """
        Describes what action to be applied when rule matches.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="matchConditions")
    def match_conditions(self) -> Sequence['outputs.FrontDoorMatchConditionResponse']:
        """
        List of match conditions.
        """
        return pulumi.get(self, "match_conditions")

    @property
    @pulumi.getter
    def priority(self) -> int:
        """
        Describes priority of the rule. Rules with a lower value will be evaluated before rules with a higher value.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="ruleType")
    def rule_type(self) -> str:
        """
        Describes type of rule.
        """
        return pulumi.get(self, "rule_type")

    @property
    @pulumi.getter(name="enabledState")
    def enabled_state(self) -> Optional[str]:
        """
        Describes if the custom rule is in enabled or disabled state. Defaults to Enabled if not specified.
        """
        return pulumi.get(self, "enabled_state")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Describes the name of the rule.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="rateLimitDurationInMinutes")
    def rate_limit_duration_in_minutes(self) -> Optional[int]:
        """
        Time window for resetting the rate limit count. Default is 1 minute.
        """
        return pulumi.get(self, "rate_limit_duration_in_minutes")

    @property
    @pulumi.getter(name="rateLimitThreshold")
    def rate_limit_threshold(self) -> Optional[int]:
        """
        Number of allowed requests per client within the time window.
        """
        return pulumi.get(self, "rate_limit_threshold")


@pulumi.output_type
class FrontDoorManagedRuleGroupOverrideResponse(dict):
    """
    Defines a managed rule group override setting.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ruleGroupName":
            suggest = "rule_group_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FrontDoorManagedRuleGroupOverrideResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FrontDoorManagedRuleGroupOverrideResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FrontDoorManagedRuleGroupOverrideResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 rule_group_name: str,
                 exclusions: Optional[Sequence['outputs.ManagedRuleExclusionResponse']] = None,
                 rules: Optional[Sequence['outputs.FrontDoorManagedRuleOverrideResponse']] = None):
        """
        Defines a managed rule group override setting.
        :param str rule_group_name: Describes the managed rule group to override.
        :param Sequence['ManagedRuleExclusionResponse'] exclusions: Describes the exclusions that are applied to all rules in the group.
        :param Sequence['FrontDoorManagedRuleOverrideResponse'] rules: List of rules that will be disabled. If none specified, all rules in the group will be disabled.
        """
        pulumi.set(__self__, "rule_group_name", rule_group_name)
        if exclusions is not None:
            pulumi.set(__self__, "exclusions", exclusions)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter(name="ruleGroupName")
    def rule_group_name(self) -> str:
        """
        Describes the managed rule group to override.
        """
        return pulumi.get(self, "rule_group_name")

    @property
    @pulumi.getter
    def exclusions(self) -> Optional[Sequence['outputs.ManagedRuleExclusionResponse']]:
        """
        Describes the exclusions that are applied to all rules in the group.
        """
        return pulumi.get(self, "exclusions")

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.FrontDoorManagedRuleOverrideResponse']]:
        """
        List of rules that will be disabled. If none specified, all rules in the group will be disabled.
        """
        return pulumi.get(self, "rules")


@pulumi.output_type
class FrontDoorManagedRuleOverrideResponse(dict):
    """
    Defines a managed rule group override setting.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ruleId":
            suggest = "rule_id"
        elif key == "enabledState":
            suggest = "enabled_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FrontDoorManagedRuleOverrideResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FrontDoorManagedRuleOverrideResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FrontDoorManagedRuleOverrideResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 rule_id: str,
                 action: Optional[str] = None,
                 enabled_state: Optional[str] = None,
                 exclusions: Optional[Sequence['outputs.ManagedRuleExclusionResponse']] = None):
        """
        Defines a managed rule group override setting.
        :param str rule_id: Identifier for the managed rule.
        :param str action: Describes the override action to be applied when rule matches.
        :param str enabled_state: Describes if the managed rule is in enabled or disabled state. Defaults to Disabled if not specified.
        :param Sequence['ManagedRuleExclusionResponse'] exclusions: Describes the exclusions that are applied to this specific rule.
        """
        pulumi.set(__self__, "rule_id", rule_id)
        if action is not None:
            pulumi.set(__self__, "action", action)
        if enabled_state is not None:
            pulumi.set(__self__, "enabled_state", enabled_state)
        if exclusions is not None:
            pulumi.set(__self__, "exclusions", exclusions)

    @property
    @pulumi.getter(name="ruleId")
    def rule_id(self) -> str:
        """
        Identifier for the managed rule.
        """
        return pulumi.get(self, "rule_id")

    @property
    @pulumi.getter
    def action(self) -> Optional[str]:
        """
        Describes the override action to be applied when rule matches.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="enabledState")
    def enabled_state(self) -> Optional[str]:
        """
        Describes if the managed rule is in enabled or disabled state. Defaults to Disabled if not specified.
        """
        return pulumi.get(self, "enabled_state")

    @property
    @pulumi.getter
    def exclusions(self) -> Optional[Sequence['outputs.ManagedRuleExclusionResponse']]:
        """
        Describes the exclusions that are applied to this specific rule.
        """
        return pulumi.get(self, "exclusions")


@pulumi.output_type
class FrontDoorManagedRuleSetResponse(dict):
    """
    Defines a managed rule set.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ruleSetType":
            suggest = "rule_set_type"
        elif key == "ruleSetVersion":
            suggest = "rule_set_version"
        elif key == "ruleGroupOverrides":
            suggest = "rule_group_overrides"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FrontDoorManagedRuleSetResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FrontDoorManagedRuleSetResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FrontDoorManagedRuleSetResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 rule_set_type: str,
                 rule_set_version: str,
                 exclusions: Optional[Sequence['outputs.ManagedRuleExclusionResponse']] = None,
                 rule_group_overrides: Optional[Sequence['outputs.FrontDoorManagedRuleGroupOverrideResponse']] = None):
        """
        Defines a managed rule set.
        :param str rule_set_type: Defines the rule set type to use.
        :param str rule_set_version: Defines the version of the rule set to use.
        :param Sequence['ManagedRuleExclusionResponse'] exclusions: Describes the exclusions that are applied to all rules in the set.
        :param Sequence['FrontDoorManagedRuleGroupOverrideResponse'] rule_group_overrides: Defines the rule group overrides to apply to the rule set.
        """
        pulumi.set(__self__, "rule_set_type", rule_set_type)
        pulumi.set(__self__, "rule_set_version", rule_set_version)
        if exclusions is not None:
            pulumi.set(__self__, "exclusions", exclusions)
        if rule_group_overrides is not None:
            pulumi.set(__self__, "rule_group_overrides", rule_group_overrides)

    @property
    @pulumi.getter(name="ruleSetType")
    def rule_set_type(self) -> str:
        """
        Defines the rule set type to use.
        """
        return pulumi.get(self, "rule_set_type")

    @property
    @pulumi.getter(name="ruleSetVersion")
    def rule_set_version(self) -> str:
        """
        Defines the version of the rule set to use.
        """
        return pulumi.get(self, "rule_set_version")

    @property
    @pulumi.getter
    def exclusions(self) -> Optional[Sequence['outputs.ManagedRuleExclusionResponse']]:
        """
        Describes the exclusions that are applied to all rules in the set.
        """
        return pulumi.get(self, "exclusions")

    @property
    @pulumi.getter(name="ruleGroupOverrides")
    def rule_group_overrides(self) -> Optional[Sequence['outputs.FrontDoorManagedRuleGroupOverrideResponse']]:
        """
        Defines the rule group overrides to apply to the rule set.
        """
        return pulumi.get(self, "rule_group_overrides")


@pulumi.output_type
class FrontDoorMatchConditionResponse(dict):
    """
    Define a match condition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "matchValue":
            suggest = "match_value"
        elif key == "matchVariable":
            suggest = "match_variable"
        elif key == "negateCondition":
            suggest = "negate_condition"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FrontDoorMatchConditionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FrontDoorMatchConditionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FrontDoorMatchConditionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 match_value: Sequence[str],
                 match_variable: str,
                 operator: str,
                 negate_condition: Optional[bool] = None,
                 selector: Optional[str] = None,
                 transforms: Optional[Sequence[str]] = None):
        """
        Define a match condition.
        :param Sequence[str] match_value: List of possible match values.
        :param str match_variable: Request variable to compare with.
        :param str operator: Comparison type to use for matching with the variable value.
        :param bool negate_condition: Describes if the result of this condition should be negated.
        :param str selector: Match against a specific key from the QueryString, PostArgs, RequestHeader or Cookies variables. Default is null.
        :param Sequence[str] transforms: List of transforms.
        """
        pulumi.set(__self__, "match_value", match_value)
        pulumi.set(__self__, "match_variable", match_variable)
        pulumi.set(__self__, "operator", operator)
        if negate_condition is not None:
            pulumi.set(__self__, "negate_condition", negate_condition)
        if selector is not None:
            pulumi.set(__self__, "selector", selector)
        if transforms is not None:
            pulumi.set(__self__, "transforms", transforms)

    @property
    @pulumi.getter(name="matchValue")
    def match_value(self) -> Sequence[str]:
        """
        List of possible match values.
        """
        return pulumi.get(self, "match_value")

    @property
    @pulumi.getter(name="matchVariable")
    def match_variable(self) -> str:
        """
        Request variable to compare with.
        """
        return pulumi.get(self, "match_variable")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        Comparison type to use for matching with the variable value.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter(name="negateCondition")
    def negate_condition(self) -> Optional[bool]:
        """
        Describes if the result of this condition should be negated.
        """
        return pulumi.get(self, "negate_condition")

    @property
    @pulumi.getter
    def selector(self) -> Optional[str]:
        """
        Match against a specific key from the QueryString, PostArgs, RequestHeader or Cookies variables. Default is null.
        """
        return pulumi.get(self, "selector")

    @property
    @pulumi.getter
    def transforms(self) -> Optional[Sequence[str]]:
        """
        List of transforms.
        """
        return pulumi.get(self, "transforms")


@pulumi.output_type
class FrontDoorPolicySettingsResponse(dict):
    """
    Defines top-level WebApplicationFirewallPolicy configuration settings.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customBlockResponseBody":
            suggest = "custom_block_response_body"
        elif key == "customBlockResponseStatusCode":
            suggest = "custom_block_response_status_code"
        elif key == "enabledState":
            suggest = "enabled_state"
        elif key == "redirectUrl":
            suggest = "redirect_url"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FrontDoorPolicySettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FrontDoorPolicySettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FrontDoorPolicySettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 custom_block_response_body: Optional[str] = None,
                 custom_block_response_status_code: Optional[int] = None,
                 enabled_state: Optional[str] = None,
                 mode: Optional[str] = None,
                 redirect_url: Optional[str] = None):
        """
        Defines top-level WebApplicationFirewallPolicy configuration settings.
        :param str custom_block_response_body: If the action type is block, customer can override the response body. The body must be specified in base64 encoding.
        :param int custom_block_response_status_code: If the action type is block, customer can override the response status code.
        :param str enabled_state: Describes if the policy is in enabled or disabled state. Defaults to Enabled if not specified.
        :param str mode: Describes if it is in detection mode or prevention mode at policy level.
        :param str redirect_url: If action type is redirect, this field represents redirect URL for the client.
        """
        if custom_block_response_body is not None:
            pulumi.set(__self__, "custom_block_response_body", custom_block_response_body)
        if custom_block_response_status_code is not None:
            pulumi.set(__self__, "custom_block_response_status_code", custom_block_response_status_code)
        if enabled_state is not None:
            pulumi.set(__self__, "enabled_state", enabled_state)
        if mode is not None:
            pulumi.set(__self__, "mode", mode)
        if redirect_url is not None:
            pulumi.set(__self__, "redirect_url", redirect_url)

    @property
    @pulumi.getter(name="customBlockResponseBody")
    def custom_block_response_body(self) -> Optional[str]:
        """
        If the action type is block, customer can override the response body. The body must be specified in base64 encoding.
        """
        return pulumi.get(self, "custom_block_response_body")

    @property
    @pulumi.getter(name="customBlockResponseStatusCode")
    def custom_block_response_status_code(self) -> Optional[int]:
        """
        If the action type is block, customer can override the response status code.
        """
        return pulumi.get(self, "custom_block_response_status_code")

    @property
    @pulumi.getter(name="enabledState")
    def enabled_state(self) -> Optional[str]:
        """
        Describes if the policy is in enabled or disabled state. Defaults to Enabled if not specified.
        """
        return pulumi.get(self, "enabled_state")

    @property
    @pulumi.getter
    def mode(self) -> Optional[str]:
        """
        Describes if it is in detection mode or prevention mode at policy level.
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter(name="redirectUrl")
    def redirect_url(self) -> Optional[str]:
        """
        If action type is redirect, this field represents redirect URL for the client.
        """
        return pulumi.get(self, "redirect_url")


@pulumi.output_type
class FrontendEndpointLinkResponse(dict):
    """
    Defines the Resource ID for a Frontend Endpoint.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Defines the Resource ID for a Frontend Endpoint.
        :param str id: Resource ID.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class ManagedRuleExclusionResponse(dict):
    """
    Exclude variables from managed rule evaluation.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "matchVariable":
            suggest = "match_variable"
        elif key == "selectorMatchOperator":
            suggest = "selector_match_operator"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedRuleExclusionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedRuleExclusionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedRuleExclusionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 match_variable: str,
                 selector: str,
                 selector_match_operator: str):
        """
        Exclude variables from managed rule evaluation.
        :param str match_variable: The variable type to be excluded.
        :param str selector: Selector value for which elements in the collection this exclusion applies to.
        :param str selector_match_operator: Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to.
        """
        pulumi.set(__self__, "match_variable", match_variable)
        pulumi.set(__self__, "selector", selector)
        pulumi.set(__self__, "selector_match_operator", selector_match_operator)

    @property
    @pulumi.getter(name="matchVariable")
    def match_variable(self) -> str:
        """
        The variable type to be excluded.
        """
        return pulumi.get(self, "match_variable")

    @property
    @pulumi.getter
    def selector(self) -> str:
        """
        Selector value for which elements in the collection this exclusion applies to.
        """
        return pulumi.get(self, "selector")

    @property
    @pulumi.getter(name="selectorMatchOperator")
    def selector_match_operator(self) -> str:
        """
        Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to.
        """
        return pulumi.get(self, "selector_match_operator")


@pulumi.output_type
class ManagedRuleSetListResponse(dict):
    """
    Defines the list of managed rule sets for the policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "managedRuleSets":
            suggest = "managed_rule_sets"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedRuleSetListResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedRuleSetListResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedRuleSetListResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 managed_rule_sets: Optional[Sequence['outputs.FrontDoorManagedRuleSetResponse']] = None):
        """
        Defines the list of managed rule sets for the policy.
        :param Sequence['FrontDoorManagedRuleSetResponse'] managed_rule_sets: List of rule sets.
        """
        if managed_rule_sets is not None:
            pulumi.set(__self__, "managed_rule_sets", managed_rule_sets)

    @property
    @pulumi.getter(name="managedRuleSets")
    def managed_rule_sets(self) -> Optional[Sequence['outputs.FrontDoorManagedRuleSetResponse']]:
        """
        List of rule sets.
        """
        return pulumi.get(self, "managed_rule_sets")


