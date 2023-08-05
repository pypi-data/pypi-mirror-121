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
    'DomainSecuritySettingsArgs',
    'LdapsSettingsArgs',
    'NotificationSettingsArgs',
]

@pulumi.input_type
class DomainSecuritySettingsArgs:
    def __init__(__self__, *,
                 ntlm_v1: Optional[pulumi.Input[Union[str, 'NtlmV1']]] = None,
                 sync_ntlm_passwords: Optional[pulumi.Input[Union[str, 'SyncNtlmPasswords']]] = None,
                 tls_v1: Optional[pulumi.Input[Union[str, 'TlsV1']]] = None):
        """
        Domain Security Settings
        :param pulumi.Input[Union[str, 'NtlmV1']] ntlm_v1: A flag to determine whether or not NtlmV1 is enabled or disabled.
        :param pulumi.Input[Union[str, 'SyncNtlmPasswords']] sync_ntlm_passwords: A flag to determine whether or not SyncNtlmPasswords is enabled or disabled.
        :param pulumi.Input[Union[str, 'TlsV1']] tls_v1: A flag to determine whether or not TlsV1 is enabled or disabled.
        """
        if ntlm_v1 is not None:
            pulumi.set(__self__, "ntlm_v1", ntlm_v1)
        if sync_ntlm_passwords is not None:
            pulumi.set(__self__, "sync_ntlm_passwords", sync_ntlm_passwords)
        if tls_v1 is not None:
            pulumi.set(__self__, "tls_v1", tls_v1)

    @property
    @pulumi.getter(name="ntlmV1")
    def ntlm_v1(self) -> Optional[pulumi.Input[Union[str, 'NtlmV1']]]:
        """
        A flag to determine whether or not NtlmV1 is enabled or disabled.
        """
        return pulumi.get(self, "ntlm_v1")

    @ntlm_v1.setter
    def ntlm_v1(self, value: Optional[pulumi.Input[Union[str, 'NtlmV1']]]):
        pulumi.set(self, "ntlm_v1", value)

    @property
    @pulumi.getter(name="syncNtlmPasswords")
    def sync_ntlm_passwords(self) -> Optional[pulumi.Input[Union[str, 'SyncNtlmPasswords']]]:
        """
        A flag to determine whether or not SyncNtlmPasswords is enabled or disabled.
        """
        return pulumi.get(self, "sync_ntlm_passwords")

    @sync_ntlm_passwords.setter
    def sync_ntlm_passwords(self, value: Optional[pulumi.Input[Union[str, 'SyncNtlmPasswords']]]):
        pulumi.set(self, "sync_ntlm_passwords", value)

    @property
    @pulumi.getter(name="tlsV1")
    def tls_v1(self) -> Optional[pulumi.Input[Union[str, 'TlsV1']]]:
        """
        A flag to determine whether or not TlsV1 is enabled or disabled.
        """
        return pulumi.get(self, "tls_v1")

    @tls_v1.setter
    def tls_v1(self, value: Optional[pulumi.Input[Union[str, 'TlsV1']]]):
        pulumi.set(self, "tls_v1", value)


@pulumi.input_type
class LdapsSettingsArgs:
    def __init__(__self__, *,
                 external_access: Optional[pulumi.Input[Union[str, 'ExternalAccess']]] = None,
                 ldaps: Optional[pulumi.Input[Union[str, 'Ldaps']]] = None,
                 pfx_certificate: Optional[pulumi.Input[str]] = None,
                 pfx_certificate_password: Optional[pulumi.Input[str]] = None):
        """
        Secure LDAP Settings
        :param pulumi.Input[Union[str, 'ExternalAccess']] external_access: A flag to determine whether or not Secure LDAP access over the internet is enabled or disabled.
        :param pulumi.Input[Union[str, 'Ldaps']] ldaps: A flag to determine whether or not Secure LDAP is enabled or disabled.
        :param pulumi.Input[str] pfx_certificate: The certificate required to configure Secure LDAP. The parameter passed here should be a base64encoded representation of the certificate pfx file.
        :param pulumi.Input[str] pfx_certificate_password: The password to decrypt the provided Secure LDAP certificate pfx file.
        """
        if external_access is not None:
            pulumi.set(__self__, "external_access", external_access)
        if ldaps is not None:
            pulumi.set(__self__, "ldaps", ldaps)
        if pfx_certificate is not None:
            pulumi.set(__self__, "pfx_certificate", pfx_certificate)
        if pfx_certificate_password is not None:
            pulumi.set(__self__, "pfx_certificate_password", pfx_certificate_password)

    @property
    @pulumi.getter(name="externalAccess")
    def external_access(self) -> Optional[pulumi.Input[Union[str, 'ExternalAccess']]]:
        """
        A flag to determine whether or not Secure LDAP access over the internet is enabled or disabled.
        """
        return pulumi.get(self, "external_access")

    @external_access.setter
    def external_access(self, value: Optional[pulumi.Input[Union[str, 'ExternalAccess']]]):
        pulumi.set(self, "external_access", value)

    @property
    @pulumi.getter
    def ldaps(self) -> Optional[pulumi.Input[Union[str, 'Ldaps']]]:
        """
        A flag to determine whether or not Secure LDAP is enabled or disabled.
        """
        return pulumi.get(self, "ldaps")

    @ldaps.setter
    def ldaps(self, value: Optional[pulumi.Input[Union[str, 'Ldaps']]]):
        pulumi.set(self, "ldaps", value)

    @property
    @pulumi.getter(name="pfxCertificate")
    def pfx_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate required to configure Secure LDAP. The parameter passed here should be a base64encoded representation of the certificate pfx file.
        """
        return pulumi.get(self, "pfx_certificate")

    @pfx_certificate.setter
    def pfx_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pfx_certificate", value)

    @property
    @pulumi.getter(name="pfxCertificatePassword")
    def pfx_certificate_password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to decrypt the provided Secure LDAP certificate pfx file.
        """
        return pulumi.get(self, "pfx_certificate_password")

    @pfx_certificate_password.setter
    def pfx_certificate_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pfx_certificate_password", value)


@pulumi.input_type
class NotificationSettingsArgs:
    def __init__(__self__, *,
                 additional_recipients: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notify_dc_admins: Optional[pulumi.Input[Union[str, 'NotifyDcAdmins']]] = None,
                 notify_global_admins: Optional[pulumi.Input[Union[str, 'NotifyGlobalAdmins']]] = None):
        """
        Settings for notification
        :param pulumi.Input[Sequence[pulumi.Input[str]]] additional_recipients: The list of additional recipients
        :param pulumi.Input[Union[str, 'NotifyDcAdmins']] notify_dc_admins: Should domain controller admins be notified
        :param pulumi.Input[Union[str, 'NotifyGlobalAdmins']] notify_global_admins: Should global admins be notified
        """
        if additional_recipients is not None:
            pulumi.set(__self__, "additional_recipients", additional_recipients)
        if notify_dc_admins is not None:
            pulumi.set(__self__, "notify_dc_admins", notify_dc_admins)
        if notify_global_admins is not None:
            pulumi.set(__self__, "notify_global_admins", notify_global_admins)

    @property
    @pulumi.getter(name="additionalRecipients")
    def additional_recipients(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of additional recipients
        """
        return pulumi.get(self, "additional_recipients")

    @additional_recipients.setter
    def additional_recipients(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "additional_recipients", value)

    @property
    @pulumi.getter(name="notifyDcAdmins")
    def notify_dc_admins(self) -> Optional[pulumi.Input[Union[str, 'NotifyDcAdmins']]]:
        """
        Should domain controller admins be notified
        """
        return pulumi.get(self, "notify_dc_admins")

    @notify_dc_admins.setter
    def notify_dc_admins(self, value: Optional[pulumi.Input[Union[str, 'NotifyDcAdmins']]]):
        pulumi.set(self, "notify_dc_admins", value)

    @property
    @pulumi.getter(name="notifyGlobalAdmins")
    def notify_global_admins(self) -> Optional[pulumi.Input[Union[str, 'NotifyGlobalAdmins']]]:
        """
        Should global admins be notified
        """
        return pulumi.get(self, "notify_global_admins")

    @notify_global_admins.setter
    def notify_global_admins(self, value: Optional[pulumi.Input[Union[str, 'NotifyGlobalAdmins']]]):
        pulumi.set(self, "notify_global_admins", value)


