# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'AdmCredentialArgs',
    'ApnsCredentialArgs',
    'BaiduCredentialArgs',
    'GcmCredentialArgs',
    'MpnsCredentialArgs',
    'SharedAccessAuthorizationRulePropertiesArgs',
    'SkuArgs',
    'WnsCredentialArgs',
]

@pulumi.input_type
class AdmCredentialArgs:
    def __init__(__self__, *,
                 auth_token_url: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None):
        """
        Description of a NotificationHub AdmCredential.
        :param pulumi.Input[str] auth_token_url: The URL of the authorization token.
        :param pulumi.Input[str] client_id: The client identifier.
        :param pulumi.Input[str] client_secret: The credential secret access key.
        """
        if auth_token_url is not None:
            pulumi.set(__self__, "auth_token_url", auth_token_url)
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)

    @property
    @pulumi.getter(name="authTokenUrl")
    def auth_token_url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the authorization token.
        """
        return pulumi.get(self, "auth_token_url")

    @auth_token_url.setter
    def auth_token_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auth_token_url", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The client identifier.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The credential secret access key.
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)


@pulumi.input_type
class ApnsCredentialArgs:
    def __init__(__self__, *,
                 apns_certificate: Optional[pulumi.Input[str]] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 app_name: Optional[pulumi.Input[str]] = None,
                 certificate_key: Optional[pulumi.Input[str]] = None,
                 endpoint: Optional[pulumi.Input[str]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None):
        """
        Description of a NotificationHub ApnsCredential.
        :param pulumi.Input[str] apns_certificate: The APNS certificate. Specify if using Certificate Authentication Mode.
        :param pulumi.Input[str] app_id: The issuer (iss) registered claim key. The value is a 10-character TeamId, obtained from your developer account. Specify if using Token Authentication Mode.
        :param pulumi.Input[str] app_name: The name of the application or BundleId. Specify if using Token Authentication Mode.
        :param pulumi.Input[str] certificate_key: The APNS certificate password if it exists.
        :param pulumi.Input[str] endpoint: The APNS endpoint of this credential. If using Certificate Authentication Mode and Sandbox specify 'gateway.sandbox.push.apple.com'. If using Certificate Authentication Mode and Production specify 'gateway.push.apple.com'. If using Token Authentication Mode and Sandbox specify 'https://api.development.push.apple.com:443/3/device'. If using Token Authentication Mode and Production specify 'https://api.push.apple.com:443/3/device'.
        :param pulumi.Input[str] key_id: A 10-character key identifier (kid) key, obtained from your developer account. Specify if using Token Authentication Mode.
        :param pulumi.Input[str] thumbprint: The APNS certificate thumbprint. Specify if using Certificate Authentication Mode.
        :param pulumi.Input[str] token: Provider Authentication Token, obtained through your developer account. Specify if using Token Authentication Mode.
        """
        if apns_certificate is not None:
            pulumi.set(__self__, "apns_certificate", apns_certificate)
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if app_name is not None:
            pulumi.set(__self__, "app_name", app_name)
        if certificate_key is not None:
            pulumi.set(__self__, "certificate_key", certificate_key)
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if key_id is not None:
            pulumi.set(__self__, "key_id", key_id)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)
        if token is not None:
            pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter(name="apnsCertificate")
    def apns_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The APNS certificate. Specify if using Certificate Authentication Mode.
        """
        return pulumi.get(self, "apns_certificate")

    @apns_certificate.setter
    def apns_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "apns_certificate", value)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[pulumi.Input[str]]:
        """
        The issuer (iss) registered claim key. The value is a 10-character TeamId, obtained from your developer account. Specify if using Token Authentication Mode.
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter(name="appName")
    def app_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application or BundleId. Specify if using Token Authentication Mode.
        """
        return pulumi.get(self, "app_name")

    @app_name.setter
    def app_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_name", value)

    @property
    @pulumi.getter(name="certificateKey")
    def certificate_key(self) -> Optional[pulumi.Input[str]]:
        """
        The APNS certificate password if it exists.
        """
        return pulumi.get(self, "certificate_key")

    @certificate_key.setter
    def certificate_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_key", value)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The APNS endpoint of this credential. If using Certificate Authentication Mode and Sandbox specify 'gateway.sandbox.push.apple.com'. If using Certificate Authentication Mode and Production specify 'gateway.push.apple.com'. If using Token Authentication Mode and Sandbox specify 'https://api.development.push.apple.com:443/3/device'. If using Token Authentication Mode and Production specify 'https://api.push.apple.com:443/3/device'.
        """
        return pulumi.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint", value)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> Optional[pulumi.Input[str]]:
        """
        A 10-character key identifier (kid) key, obtained from your developer account. Specify if using Token Authentication Mode.
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_id", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        The APNS certificate thumbprint. Specify if using Certificate Authentication Mode.
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        Provider Authentication Token, obtained through your developer account. Specify if using Token Authentication Mode.
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)


@pulumi.input_type
class BaiduCredentialArgs:
    def __init__(__self__, *,
                 baidu_api_key: Optional[pulumi.Input[str]] = None,
                 baidu_end_point: Optional[pulumi.Input[str]] = None,
                 baidu_secret_key: Optional[pulumi.Input[str]] = None):
        """
        Description of a NotificationHub BaiduCredential.
        :param pulumi.Input[str] baidu_api_key: Baidu Api Key.
        :param pulumi.Input[str] baidu_end_point: Baidu Endpoint.
        :param pulumi.Input[str] baidu_secret_key: Baidu Secret Key
        """
        if baidu_api_key is not None:
            pulumi.set(__self__, "baidu_api_key", baidu_api_key)
        if baidu_end_point is not None:
            pulumi.set(__self__, "baidu_end_point", baidu_end_point)
        if baidu_secret_key is not None:
            pulumi.set(__self__, "baidu_secret_key", baidu_secret_key)

    @property
    @pulumi.getter(name="baiduApiKey")
    def baidu_api_key(self) -> Optional[pulumi.Input[str]]:
        """
        Baidu Api Key.
        """
        return pulumi.get(self, "baidu_api_key")

    @baidu_api_key.setter
    def baidu_api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "baidu_api_key", value)

    @property
    @pulumi.getter(name="baiduEndPoint")
    def baidu_end_point(self) -> Optional[pulumi.Input[str]]:
        """
        Baidu Endpoint.
        """
        return pulumi.get(self, "baidu_end_point")

    @baidu_end_point.setter
    def baidu_end_point(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "baidu_end_point", value)

    @property
    @pulumi.getter(name="baiduSecretKey")
    def baidu_secret_key(self) -> Optional[pulumi.Input[str]]:
        """
        Baidu Secret Key
        """
        return pulumi.get(self, "baidu_secret_key")

    @baidu_secret_key.setter
    def baidu_secret_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "baidu_secret_key", value)


@pulumi.input_type
class GcmCredentialArgs:
    def __init__(__self__, *,
                 gcm_endpoint: Optional[pulumi.Input[str]] = None,
                 google_api_key: Optional[pulumi.Input[str]] = None):
        """
        Description of a NotificationHub GcmCredential.
        :param pulumi.Input[str] gcm_endpoint: The FCM legacy endpoint. Default value is 'https://fcm.googleapis.com/fcm/send'
        :param pulumi.Input[str] google_api_key: The Google API key.
        """
        if gcm_endpoint is not None:
            pulumi.set(__self__, "gcm_endpoint", gcm_endpoint)
        if google_api_key is not None:
            pulumi.set(__self__, "google_api_key", google_api_key)

    @property
    @pulumi.getter(name="gcmEndpoint")
    def gcm_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The FCM legacy endpoint. Default value is 'https://fcm.googleapis.com/fcm/send'
        """
        return pulumi.get(self, "gcm_endpoint")

    @gcm_endpoint.setter
    def gcm_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gcm_endpoint", value)

    @property
    @pulumi.getter(name="googleApiKey")
    def google_api_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Google API key.
        """
        return pulumi.get(self, "google_api_key")

    @google_api_key.setter
    def google_api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "google_api_key", value)


@pulumi.input_type
class MpnsCredentialArgs:
    def __init__(__self__, *,
                 certificate_key: Optional[pulumi.Input[str]] = None,
                 mpns_certificate: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None):
        """
        Description of a NotificationHub MpnsCredential.
        :param pulumi.Input[str] certificate_key: The certificate key for this credential.
        :param pulumi.Input[str] mpns_certificate: The MPNS certificate.
        :param pulumi.Input[str] thumbprint: The MPNS certificate Thumbprint
        """
        if certificate_key is not None:
            pulumi.set(__self__, "certificate_key", certificate_key)
        if mpns_certificate is not None:
            pulumi.set(__self__, "mpns_certificate", mpns_certificate)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)

    @property
    @pulumi.getter(name="certificateKey")
    def certificate_key(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate key for this credential.
        """
        return pulumi.get(self, "certificate_key")

    @certificate_key.setter
    def certificate_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_key", value)

    @property
    @pulumi.getter(name="mpnsCertificate")
    def mpns_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The MPNS certificate.
        """
        return pulumi.get(self, "mpns_certificate")

    @mpns_certificate.setter
    def mpns_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mpns_certificate", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        The MPNS certificate Thumbprint
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint", value)


@pulumi.input_type
class SharedAccessAuthorizationRulePropertiesArgs:
    def __init__(__self__, *,
                 rights: Optional[pulumi.Input[Sequence[pulumi.Input['AccessRights']]]] = None):
        """
        SharedAccessAuthorizationRule properties.
        :param pulumi.Input[Sequence[pulumi.Input['AccessRights']]] rights: The rights associated with the rule.
        """
        if rights is not None:
            pulumi.set(__self__, "rights", rights)

    @property
    @pulumi.getter
    def rights(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccessRights']]]]:
        """
        The rights associated with the rule.
        """
        return pulumi.get(self, "rights")

    @rights.setter
    def rights(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccessRights']]]]):
        pulumi.set(self, "rights", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'SkuName']],
                 capacity: Optional[pulumi.Input[int]] = None,
                 family: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[str]] = None):
        """
        The Sku description for a namespace
        :param pulumi.Input[Union[str, 'SkuName']] name: Name of the notification hub sku
        :param pulumi.Input[int] capacity: The capacity of the resource
        :param pulumi.Input[str] family: The Sku Family
        :param pulumi.Input[str] size: The Sku size
        :param pulumi.Input[str] tier: The tier of particular sku
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'SkuName']]:
        """
        Name of the notification hub sku
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'SkuName']]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The capacity of the resource
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def family(self) -> Optional[pulumi.Input[str]]:
        """
        The Sku Family
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        The Sku size
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[str]]:
        """
        The tier of particular sku
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class WnsCredentialArgs:
    def __init__(__self__, *,
                 package_sid: Optional[pulumi.Input[str]] = None,
                 secret_key: Optional[pulumi.Input[str]] = None,
                 windows_live_endpoint: Optional[pulumi.Input[str]] = None):
        """
        Description of a NotificationHub WnsCredential.
        :param pulumi.Input[str] package_sid: The package ID for this credential.
        :param pulumi.Input[str] secret_key: The secret key.
        :param pulumi.Input[str] windows_live_endpoint: The Windows Live endpoint.
        """
        if package_sid is not None:
            pulumi.set(__self__, "package_sid", package_sid)
        if secret_key is not None:
            pulumi.set(__self__, "secret_key", secret_key)
        if windows_live_endpoint is not None:
            pulumi.set(__self__, "windows_live_endpoint", windows_live_endpoint)

    @property
    @pulumi.getter(name="packageSid")
    def package_sid(self) -> Optional[pulumi.Input[str]]:
        """
        The package ID for this credential.
        """
        return pulumi.get(self, "package_sid")

    @package_sid.setter
    def package_sid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_sid", value)

    @property
    @pulumi.getter(name="secretKey")
    def secret_key(self) -> Optional[pulumi.Input[str]]:
        """
        The secret key.
        """
        return pulumi.get(self, "secret_key")

    @secret_key.setter
    def secret_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_key", value)

    @property
    @pulumi.getter(name="windowsLiveEndpoint")
    def windows_live_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The Windows Live endpoint.
        """
        return pulumi.get(self, "windows_live_endpoint")

    @windows_live_endpoint.setter
    def windows_live_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "windows_live_endpoint", value)


