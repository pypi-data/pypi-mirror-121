# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult',
    'AwaitableGetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult',
    'get_p2s_vpn_gateway_p2s_vpn_connection_health_detailed',
]

@pulumi.output_type
class GetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult:
    """
    P2S Vpn connection detailed health written to sas url.
    """
    def __init__(__self__, sas_url=None):
        if sas_url and not isinstance(sas_url, str):
            raise TypeError("Expected argument 'sas_url' to be a str")
        pulumi.set(__self__, "sas_url", sas_url)

    @property
    @pulumi.getter(name="sasUrl")
    def sas_url(self) -> Optional[str]:
        """
        Returned sas url of the blob to which the p2s vpn connection detailed health will be written.
        """
        return pulumi.get(self, "sas_url")


class AwaitableGetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult(GetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult(
            sas_url=self.sas_url)


def get_p2s_vpn_gateway_p2s_vpn_connection_health_detailed(gateway_name: Optional[str] = None,
                                                           output_blob_sas_url: Optional[str] = None,
                                                           resource_group_name: Optional[str] = None,
                                                           vpn_user_names_filter: Optional[Sequence[str]] = None,
                                                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult:
    """
    P2S Vpn connection detailed health written to sas url.


    :param str gateway_name: The name of the P2SVpnGateway.
    :param str output_blob_sas_url: The sas-url to download the P2S Vpn connection health detail.
    :param str resource_group_name: The name of the resource group.
    :param Sequence[str] vpn_user_names_filter: The list of p2s vpn user names whose p2s vpn connection detailed health to retrieve for.
    """
    __args__ = dict()
    __args__['gatewayName'] = gateway_name
    __args__['outputBlobSasUrl'] = output_blob_sas_url
    __args__['resourceGroupName'] = resource_group_name
    __args__['vpnUserNamesFilter'] = vpn_user_names_filter
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200301:getP2sVpnGatewayP2sVpnConnectionHealthDetailed', __args__, opts=opts, typ=GetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult).value

    return AwaitableGetP2sVpnGatewayP2sVpnConnectionHealthDetailedResult(
        sas_url=__ret__.sas_url)
