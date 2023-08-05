# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetServerSecurityAlertPolicyResult',
    'AwaitableGetServerSecurityAlertPolicyResult',
    'get_server_security_alert_policy',
]

@pulumi.output_type
class GetServerSecurityAlertPolicyResult:
    """
    A server security alert policy.
    """
    def __init__(__self__, disabled_alerts=None, email_account_admins=None, email_addresses=None, id=None, name=None, retention_days=None, state=None, storage_account_access_key=None, storage_endpoint=None, type=None):
        if disabled_alerts and not isinstance(disabled_alerts, list):
            raise TypeError("Expected argument 'disabled_alerts' to be a list")
        pulumi.set(__self__, "disabled_alerts", disabled_alerts)
        if email_account_admins and not isinstance(email_account_admins, bool):
            raise TypeError("Expected argument 'email_account_admins' to be a bool")
        pulumi.set(__self__, "email_account_admins", email_account_admins)
        if email_addresses and not isinstance(email_addresses, list):
            raise TypeError("Expected argument 'email_addresses' to be a list")
        pulumi.set(__self__, "email_addresses", email_addresses)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if retention_days and not isinstance(retention_days, int):
            raise TypeError("Expected argument 'retention_days' to be a int")
        pulumi.set(__self__, "retention_days", retention_days)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if storage_account_access_key and not isinstance(storage_account_access_key, str):
            raise TypeError("Expected argument 'storage_account_access_key' to be a str")
        pulumi.set(__self__, "storage_account_access_key", storage_account_access_key)
        if storage_endpoint and not isinstance(storage_endpoint, str):
            raise TypeError("Expected argument 'storage_endpoint' to be a str")
        pulumi.set(__self__, "storage_endpoint", storage_endpoint)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="disabledAlerts")
    def disabled_alerts(self) -> Optional[Sequence[str]]:
        """
        Specifies an array of alerts that are disabled. Allowed values are: Sql_Injection, Sql_Injection_Vulnerability, Access_Anomaly
        """
        return pulumi.get(self, "disabled_alerts")

    @property
    @pulumi.getter(name="emailAccountAdmins")
    def email_account_admins(self) -> Optional[bool]:
        """
        Specifies that the alert is sent to the account administrators.
        """
        return pulumi.get(self, "email_account_admins")

    @property
    @pulumi.getter(name="emailAddresses")
    def email_addresses(self) -> Optional[Sequence[str]]:
        """
        Specifies an array of e-mail addresses to which the alert is sent.
        """
        return pulumi.get(self, "email_addresses")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="retentionDays")
    def retention_days(self) -> Optional[int]:
        """
        Specifies the number of days to keep in the Threat Detection audit logs.
        """
        return pulumi.get(self, "retention_days")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Specifies the state of the policy, whether it is enabled or disabled.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageAccountAccessKey")
    def storage_account_access_key(self) -> Optional[str]:
        """
        Specifies the identifier key of the Threat Detection audit storage account.
        """
        return pulumi.get(self, "storage_account_access_key")

    @property
    @pulumi.getter(name="storageEndpoint")
    def storage_endpoint(self) -> Optional[str]:
        """
        Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net). This blob storage will hold all Threat Detection audit logs.
        """
        return pulumi.get(self, "storage_endpoint")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetServerSecurityAlertPolicyResult(GetServerSecurityAlertPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerSecurityAlertPolicyResult(
            disabled_alerts=self.disabled_alerts,
            email_account_admins=self.email_account_admins,
            email_addresses=self.email_addresses,
            id=self.id,
            name=self.name,
            retention_days=self.retention_days,
            state=self.state,
            storage_account_access_key=self.storage_account_access_key,
            storage_endpoint=self.storage_endpoint,
            type=self.type)


def get_server_security_alert_policy(resource_group_name: Optional[str] = None,
                                     security_alert_policy_name: Optional[str] = None,
                                     server_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerSecurityAlertPolicyResult:
    """
    A server security alert policy.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str security_alert_policy_name: The name of the security alert policy.
    :param str server_name: The name of the server.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['securityAlertPolicyName'] = security_alert_policy_name
    __args__['serverName'] = server_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:dbforpostgresql/v20171201:getServerSecurityAlertPolicy', __args__, opts=opts, typ=GetServerSecurityAlertPolicyResult).value

    return AwaitableGetServerSecurityAlertPolicyResult(
        disabled_alerts=__ret__.disabled_alerts,
        email_account_admins=__ret__.email_account_admins,
        email_addresses=__ret__.email_addresses,
        id=__ret__.id,
        name=__ret__.name,
        retention_days=__ret__.retention_days,
        state=__ret__.state,
        storage_account_access_key=__ret__.storage_account_access_key,
        storage_endpoint=__ret__.storage_endpoint,
        type=__ret__.type)
