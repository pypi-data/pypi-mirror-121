# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetApiManagementServiceSsoTokenResult',
    'AwaitableGetApiManagementServiceSsoTokenResult',
    'get_api_management_service_sso_token',
]

@pulumi.output_type
class GetApiManagementServiceSsoTokenResult:
    """
    The response of the GetSsoToken operation.
    """
    def __init__(__self__, redirect_uri=None):
        if redirect_uri and not isinstance(redirect_uri, str):
            raise TypeError("Expected argument 'redirect_uri' to be a str")
        pulumi.set(__self__, "redirect_uri", redirect_uri)

    @property
    @pulumi.getter(name="redirectUri")
    def redirect_uri(self) -> Optional[str]:
        """
        Redirect URL to the Publisher Portal containing the SSO token.
        """
        return pulumi.get(self, "redirect_uri")


class AwaitableGetApiManagementServiceSsoTokenResult(GetApiManagementServiceSsoTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApiManagementServiceSsoTokenResult(
            redirect_uri=self.redirect_uri)


def get_api_management_service_sso_token(resource_group_name: Optional[str] = None,
                                         service_name: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApiManagementServiceSsoTokenResult:
    """
    The response of the GetSsoToken operation.


    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20210401preview:getApiManagementServiceSsoToken', __args__, opts=opts, typ=GetApiManagementServiceSsoTokenResult).value

    return AwaitableGetApiManagementServiceSsoTokenResult(
        redirect_uri=__ret__.redirect_uri)
