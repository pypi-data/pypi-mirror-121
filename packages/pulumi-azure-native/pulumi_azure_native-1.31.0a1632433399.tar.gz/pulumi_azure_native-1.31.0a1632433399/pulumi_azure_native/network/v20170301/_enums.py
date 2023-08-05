# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'Access',
    'ApplicationGatewayCookieBasedAffinity',
    'ApplicationGatewayFirewallMode',
    'ApplicationGatewayProtocol',
    'ApplicationGatewayRequestRoutingRuleType',
    'ApplicationGatewaySkuName',
    'ApplicationGatewaySslProtocol',
    'ApplicationGatewayTier',
    'AuthorizationUseStatus',
    'DhGroup',
    'ExpressRouteCircuitPeeringAdvertisedPublicPrefixState',
    'ExpressRouteCircuitPeeringState',
    'ExpressRouteCircuitPeeringType',
    'ExpressRouteCircuitSkuFamily',
    'ExpressRouteCircuitSkuTier',
    'IPAllocationMethod',
    'IPVersion',
    'IkeEncryption',
    'IkeIntegrity',
    'IpsecEncryption',
    'IpsecIntegrity',
    'LoadDistribution',
    'PcProtocol',
    'PfsGroup',
    'ProbeProtocol',
    'RouteFilterRuleType',
    'RouteNextHopType',
    'SecurityRuleAccess',
    'SecurityRuleDirection',
    'SecurityRuleProtocol',
    'ServiceProviderProvisioningState',
    'TransportProtocol',
    'VirtualNetworkGatewayConnectionType',
    'VirtualNetworkGatewaySkuName',
    'VirtualNetworkGatewaySkuTier',
    'VirtualNetworkGatewayType',
    'VirtualNetworkPeeringState',
    'VpnType',
]


class Access(str, Enum):
    """
    The access type of the rule. Valid values are: 'Allow', 'Deny'
    """
    ALLOW = "Allow"
    DENY = "Deny"


class ApplicationGatewayCookieBasedAffinity(str, Enum):
    """
    Cookie based affinity.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ApplicationGatewayFirewallMode(str, Enum):
    """
    Web application firewall mode.
    """
    DETECTION = "Detection"
    PREVENTION = "Prevention"


class ApplicationGatewayProtocol(str, Enum):
    """
    Protocol.
    """
    HTTP = "Http"
    HTTPS = "Https"


class ApplicationGatewayRequestRoutingRuleType(str, Enum):
    """
    Rule type.
    """
    BASIC = "Basic"
    PATH_BASED_ROUTING = "PathBasedRouting"


class ApplicationGatewaySkuName(str, Enum):
    """
    Name of an application gateway SKU.
    """
    STANDARD_SMALL = "Standard_Small"
    STANDARD_MEDIUM = "Standard_Medium"
    STANDARD_LARGE = "Standard_Large"
    WA_F_MEDIUM = "WAF_Medium"
    WA_F_LARGE = "WAF_Large"


class ApplicationGatewaySslProtocol(str, Enum):
    TL_SV1_0 = "TLSv1_0"
    TL_SV1_1 = "TLSv1_1"
    TL_SV1_2 = "TLSv1_2"


class ApplicationGatewayTier(str, Enum):
    """
    Tier of an application gateway.
    """
    STANDARD = "Standard"
    WAF = "WAF"


class AuthorizationUseStatus(str, Enum):
    """
    AuthorizationUseStatus. Possible values are: 'Available' and 'InUse'.
    """
    AVAILABLE = "Available"
    IN_USE = "InUse"


class DhGroup(str, Enum):
    """
    The DH Groups used in IKE Phase 1 for initial SA.
    """
    NONE = "None"
    DH_GROUP1 = "DHGroup1"
    DH_GROUP2 = "DHGroup2"
    DH_GROUP14 = "DHGroup14"
    DH_GROUP2048 = "DHGroup2048"
    ECP256 = "ECP256"
    ECP384 = "ECP384"
    DH_GROUP24 = "DHGroup24"


class ExpressRouteCircuitPeeringAdvertisedPublicPrefixState(str, Enum):
    """
    AdvertisedPublicPrefixState of the Peering resource. Possible values are 'NotConfigured', 'Configuring', 'Configured', and 'ValidationNeeded'.
    """
    NOT_CONFIGURED = "NotConfigured"
    CONFIGURING = "Configuring"
    CONFIGURED = "Configured"
    VALIDATION_NEEDED = "ValidationNeeded"


class ExpressRouteCircuitPeeringState(str, Enum):
    """
    The state of peering. Possible values are: 'Disabled' and 'Enabled'
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class ExpressRouteCircuitPeeringType(str, Enum):
    """
    The PeeringType. Possible values are: 'AzurePublicPeering', 'AzurePrivatePeering', and 'MicrosoftPeering'.
    """
    AZURE_PUBLIC_PEERING = "AzurePublicPeering"
    AZURE_PRIVATE_PEERING = "AzurePrivatePeering"
    MICROSOFT_PEERING = "MicrosoftPeering"


class ExpressRouteCircuitSkuFamily(str, Enum):
    """
    The family of the SKU. Possible values are: 'UnlimitedData' and 'MeteredData'.
    """
    UNLIMITED_DATA = "UnlimitedData"
    METERED_DATA = "MeteredData"


class ExpressRouteCircuitSkuTier(str, Enum):
    """
    The tier of the SKU. Possible values are 'Standard' and 'Premium'.
    """
    STANDARD = "Standard"
    PREMIUM = "Premium"


class IPAllocationMethod(str, Enum):
    """
    The private IP allocation method. Possible values are: 'Static' and 'Dynamic'.
    """
    STATIC = "Static"
    DYNAMIC = "Dynamic"


class IPVersion(str, Enum):
    """
    The public IP address version. Possible values are: 'IPv4' and 'IPv6'.
    """
    I_PV4 = "IPv4"
    I_PV6 = "IPv6"


class IkeEncryption(str, Enum):
    """
    The IKE encryption algorithm (IKE phase 2).
    """
    DES = "DES"
    DES3 = "DES3"
    AES128 = "AES128"
    AES192 = "AES192"
    AES256 = "AES256"


class IkeIntegrity(str, Enum):
    """
    The IKE integrity algorithm (IKE phase 2).
    """
    MD5 = "MD5"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA384 = "SHA384"


class IpsecEncryption(str, Enum):
    """
    The IPSec encryption algorithm (IKE phase 1).
    """
    NONE = "None"
    DES = "DES"
    DES3 = "DES3"
    AES128 = "AES128"
    AES192 = "AES192"
    AES256 = "AES256"
    GCMAES128 = "GCMAES128"
    GCMAES192 = "GCMAES192"
    GCMAES256 = "GCMAES256"


class IpsecIntegrity(str, Enum):
    """
    The IPSec integrity algorithm (IKE phase 1).
    """
    MD5 = "MD5"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    GCMAES128 = "GCMAES128"
    GCMAES192 = "GCMAES192"
    GCMAES256 = "GCMAES256"


class LoadDistribution(str, Enum):
    """
    The load distribution policy for this rule. Possible values are 'Default', 'SourceIP', and 'SourceIPProtocol'.
    """
    DEFAULT = "Default"
    SOURCE_IP = "SourceIP"
    SOURCE_IP_PROTOCOL = "SourceIPProtocol"


class PcProtocol(str, Enum):
    """
    Protocol to be filtered on.
    """
    TCP = "TCP"
    UDP = "UDP"
    ANY = "Any"


class PfsGroup(str, Enum):
    """
    The DH Groups used in IKE Phase 2 for new child SA.
    """
    NONE = "None"
    PFS1 = "PFS1"
    PFS2 = "PFS2"
    PFS2048 = "PFS2048"
    ECP256 = "ECP256"
    ECP384 = "ECP384"
    PFS24 = "PFS24"


class ProbeProtocol(str, Enum):
    """
    The protocol of the end point. Possible values are: 'Http' or 'Tcp'. If 'Tcp' is specified, a received ACK is required for the probe to be successful. If 'Http' is specified, a 200 OK response from the specifies URI is required for the probe to be successful.
    """
    HTTP = "Http"
    TCP = "Tcp"


class RouteFilterRuleType(str, Enum):
    """
    The rule type of the rule. Valid value is: 'Community'
    """
    COMMUNITY = "Community"


class RouteNextHopType(str, Enum):
    """
    The type of Azure hop the packet should be sent to. Possible values are: 'VirtualNetworkGateway', 'VnetLocal', 'Internet', 'VirtualAppliance', and 'None'
    """
    VIRTUAL_NETWORK_GATEWAY = "VirtualNetworkGateway"
    VNET_LOCAL = "VnetLocal"
    INTERNET = "Internet"
    VIRTUAL_APPLIANCE = "VirtualAppliance"
    NONE = "None"


class SecurityRuleAccess(str, Enum):
    """
    The network traffic is allowed or denied. Possible values are: 'Allow' and 'Deny'.
    """
    ALLOW = "Allow"
    DENY = "Deny"


class SecurityRuleDirection(str, Enum):
    """
    The direction of the rule. The direction specifies if rule will be evaluated on incoming or outgoing traffic. Possible values are: 'Inbound' and 'Outbound'.
    """
    INBOUND = "Inbound"
    OUTBOUND = "Outbound"


class SecurityRuleProtocol(str, Enum):
    """
    Network protocol this rule applies to. Possible values are 'Tcp', 'Udp', and '*'.
    """
    TCP = "Tcp"
    UDP = "Udp"
    ASTERISK = "*"


class ServiceProviderProvisioningState(str, Enum):
    """
    The ServiceProviderProvisioningState state of the resource. Possible values are 'NotProvisioned', 'Provisioning', 'Provisioned', and 'Deprovisioning'.
    """
    NOT_PROVISIONED = "NotProvisioned"
    PROVISIONING = "Provisioning"
    PROVISIONED = "Provisioned"
    DEPROVISIONING = "Deprovisioning"


class TransportProtocol(str, Enum):
    """
    The transport protocol for the endpoint. Possible values are: 'Udp' or 'Tcp'
    """
    UDP = "Udp"
    TCP = "Tcp"


class VirtualNetworkGatewayConnectionType(str, Enum):
    """
    Gateway connection type. Possible values are: 'IPsec','Vnet2Vnet','ExpressRoute', and 'VPNClient.
    """
    IPSEC = "IPsec"
    VNET2_VNET = "Vnet2Vnet"
    EXPRESS_ROUTE = "ExpressRoute"
    VPN_CLIENT = "VPNClient"


class VirtualNetworkGatewaySkuName(str, Enum):
    """
    Gateway SKU name.
    """
    BASIC = "Basic"
    HIGH_PERFORMANCE = "HighPerformance"
    STANDARD = "Standard"
    ULTRA_PERFORMANCE = "UltraPerformance"
    VPN_GW1 = "VpnGw1"
    VPN_GW2 = "VpnGw2"
    VPN_GW3 = "VpnGw3"


class VirtualNetworkGatewaySkuTier(str, Enum):
    """
    Gateway SKU tier.
    """
    BASIC = "Basic"
    HIGH_PERFORMANCE = "HighPerformance"
    STANDARD = "Standard"
    ULTRA_PERFORMANCE = "UltraPerformance"
    VPN_GW1 = "VpnGw1"
    VPN_GW2 = "VpnGw2"
    VPN_GW3 = "VpnGw3"


class VirtualNetworkGatewayType(str, Enum):
    """
    The type of this virtual network gateway. Possible values are: 'Vpn' and 'ExpressRoute'.
    """
    VPN = "Vpn"
    EXPRESS_ROUTE = "ExpressRoute"


class VirtualNetworkPeeringState(str, Enum):
    """
    The status of the virtual network peering. Possible values are 'Initiated', 'Connected', and 'Disconnected'.
    """
    INITIATED = "Initiated"
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"


class VpnType(str, Enum):
    """
    The type of this virtual network gateway. Possible values are: 'PolicyBased' and 'RouteBased'.
    """
    POLICY_BASED = "PolicyBased"
    ROUTE_BASED = "RouteBased"
