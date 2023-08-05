# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetThreatIntelligenceAlertRuleResult',
    'AwaitableGetThreatIntelligenceAlertRuleResult',
    'get_threat_intelligence_alert_rule',
]

@pulumi.output_type
class GetThreatIntelligenceAlertRuleResult:
    """
    Represents Threat Intelligence alert rule.
    """
    def __init__(__self__, alert_rule_template_name=None, description=None, display_name=None, enabled=None, etag=None, id=None, kind=None, last_modified_utc=None, name=None, severity=None, system_data=None, tactics=None, type=None):
        if alert_rule_template_name and not isinstance(alert_rule_template_name, str):
            raise TypeError("Expected argument 'alert_rule_template_name' to be a str")
        pulumi.set(__self__, "alert_rule_template_name", alert_rule_template_name)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_modified_utc and not isinstance(last_modified_utc, str):
            raise TypeError("Expected argument 'last_modified_utc' to be a str")
        pulumi.set(__self__, "last_modified_utc", last_modified_utc)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if severity and not isinstance(severity, str):
            raise TypeError("Expected argument 'severity' to be a str")
        pulumi.set(__self__, "severity", severity)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tactics and not isinstance(tactics, list):
            raise TypeError("Expected argument 'tactics' to be a list")
        pulumi.set(__self__, "tactics", tactics)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="alertRuleTemplateName")
    def alert_rule_template_name(self) -> str:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, "alert_rule_template_name")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the alert rule
        Expected value is 'ThreatIntelligence'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastModifiedUtc")
    def last_modified_utc(self) -> str:
        """
        The last time that this alert has been modified.
        """
        return pulumi.get(self, "last_modified_utc")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        The severity for alerts created by this alert rule.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tactics(self) -> Sequence[str]:
        """
        The tactics of the alert rule
        """
        return pulumi.get(self, "tactics")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetThreatIntelligenceAlertRuleResult(GetThreatIntelligenceAlertRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetThreatIntelligenceAlertRuleResult(
            alert_rule_template_name=self.alert_rule_template_name,
            description=self.description,
            display_name=self.display_name,
            enabled=self.enabled,
            etag=self.etag,
            id=self.id,
            kind=self.kind,
            last_modified_utc=self.last_modified_utc,
            name=self.name,
            severity=self.severity,
            system_data=self.system_data,
            tactics=self.tactics,
            type=self.type)


def get_threat_intelligence_alert_rule(operational_insights_resource_provider: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       rule_id: Optional[str] = None,
                                       workspace_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetThreatIntelligenceAlertRuleResult:
    """
    Represents Threat Intelligence alert rule.


    :param str operational_insights_resource_provider: The namespace of workspaces resource provider- Microsoft.OperationalInsights.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['operationalInsightsResourceProvider'] = operational_insights_resource_provider
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleId'] = rule_id
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20210301preview:getThreatIntelligenceAlertRule', __args__, opts=opts, typ=GetThreatIntelligenceAlertRuleResult).value

    return AwaitableGetThreatIntelligenceAlertRuleResult(
        alert_rule_template_name=__ret__.alert_rule_template_name,
        description=__ret__.description,
        display_name=__ret__.display_name,
        enabled=__ret__.enabled,
        etag=__ret__.etag,
        id=__ret__.id,
        kind=__ret__.kind,
        last_modified_utc=__ret__.last_modified_utc,
        name=__ret__.name,
        severity=__ret__.severity,
        system_data=__ret__.system_data,
        tactics=__ret__.tactics,
        type=__ret__.type)
