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
    'GetManagementGroupDiagnosticSettingResult',
    'AwaitableGetManagementGroupDiagnosticSettingResult',
    'get_management_group_diagnostic_setting',
]

@pulumi.output_type
class GetManagementGroupDiagnosticSettingResult:
    """
    The management group diagnostic setting resource.
    """
    def __init__(__self__, event_hub_authorization_rule_id=None, event_hub_name=None, id=None, logs=None, marketplace_partner_id=None, name=None, service_bus_rule_id=None, storage_account_id=None, system_data=None, type=None, workspace_id=None):
        if event_hub_authorization_rule_id and not isinstance(event_hub_authorization_rule_id, str):
            raise TypeError("Expected argument 'event_hub_authorization_rule_id' to be a str")
        pulumi.set(__self__, "event_hub_authorization_rule_id", event_hub_authorization_rule_id)
        if event_hub_name and not isinstance(event_hub_name, str):
            raise TypeError("Expected argument 'event_hub_name' to be a str")
        pulumi.set(__self__, "event_hub_name", event_hub_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if logs and not isinstance(logs, list):
            raise TypeError("Expected argument 'logs' to be a list")
        pulumi.set(__self__, "logs", logs)
        if marketplace_partner_id and not isinstance(marketplace_partner_id, str):
            raise TypeError("Expected argument 'marketplace_partner_id' to be a str")
        pulumi.set(__self__, "marketplace_partner_id", marketplace_partner_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if service_bus_rule_id and not isinstance(service_bus_rule_id, str):
            raise TypeError("Expected argument 'service_bus_rule_id' to be a str")
        pulumi.set(__self__, "service_bus_rule_id", service_bus_rule_id)
        if storage_account_id and not isinstance(storage_account_id, str):
            raise TypeError("Expected argument 'storage_account_id' to be a str")
        pulumi.set(__self__, "storage_account_id", storage_account_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="eventHubAuthorizationRuleId")
    def event_hub_authorization_rule_id(self) -> Optional[str]:
        """
        The resource Id for the event hub authorization rule.
        """
        return pulumi.get(self, "event_hub_authorization_rule_id")

    @property
    @pulumi.getter(name="eventHubName")
    def event_hub_name(self) -> Optional[str]:
        """
        The name of the event hub. If none is specified, the default event hub will be selected.
        """
        return pulumi.get(self, "event_hub_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def logs(self) -> Optional[Sequence['outputs.ManagementGroupLogSettingsResponse']]:
        """
        The list of logs settings.
        """
        return pulumi.get(self, "logs")

    @property
    @pulumi.getter(name="marketplacePartnerId")
    def marketplace_partner_id(self) -> Optional[str]:
        """
        The full ARM resource ID of the Marketplace resource to which you would like to send Diagnostic Logs.
        """
        return pulumi.get(self, "marketplace_partner_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceBusRuleId")
    def service_bus_rule_id(self) -> Optional[str]:
        """
        The service bus rule Id of the diagnostic setting. This is here to maintain backwards compatibility.
        """
        return pulumi.get(self, "service_bus_rule_id")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[str]:
        """
        The resource ID of the storage account to which you would like to send Diagnostic Logs.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata related to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[str]:
        """
        The full ARM resource ID of the Log Analytics workspace to which you would like to send Diagnostic Logs. Example: /subscriptions/4b9e8510-67ab-4e9a-95a9-e2f1e570ea9c/resourceGroups/insights-integration/providers/Microsoft.OperationalInsights/workspaces/viruela2
        """
        return pulumi.get(self, "workspace_id")


class AwaitableGetManagementGroupDiagnosticSettingResult(GetManagementGroupDiagnosticSettingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagementGroupDiagnosticSettingResult(
            event_hub_authorization_rule_id=self.event_hub_authorization_rule_id,
            event_hub_name=self.event_hub_name,
            id=self.id,
            logs=self.logs,
            marketplace_partner_id=self.marketplace_partner_id,
            name=self.name,
            service_bus_rule_id=self.service_bus_rule_id,
            storage_account_id=self.storage_account_id,
            system_data=self.system_data,
            type=self.type,
            workspace_id=self.workspace_id)


def get_management_group_diagnostic_setting(management_group_id: Optional[str] = None,
                                            name: Optional[str] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagementGroupDiagnosticSettingResult:
    """
    The management group diagnostic setting resource.


    :param str management_group_id: The management group id.
    :param str name: The name of the diagnostic setting.
    """
    __args__ = dict()
    __args__['managementGroupId'] = management_group_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:insights/v20210501preview:getManagementGroupDiagnosticSetting', __args__, opts=opts, typ=GetManagementGroupDiagnosticSettingResult).value

    return AwaitableGetManagementGroupDiagnosticSettingResult(
        event_hub_authorization_rule_id=__ret__.event_hub_authorization_rule_id,
        event_hub_name=__ret__.event_hub_name,
        id=__ret__.id,
        logs=__ret__.logs,
        marketplace_partner_id=__ret__.marketplace_partner_id,
        name=__ret__.name,
        service_bus_rule_id=__ret__.service_bus_rule_id,
        storage_account_id=__ret__.storage_account_id,
        system_data=__ret__.system_data,
        type=__ret__.type,
        workspace_id=__ret__.workspace_id)
