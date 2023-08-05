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
    'GetApplicationGatewayResult',
    'AwaitableGetApplicationGatewayResult',
    'get_application_gateway',
]

@pulumi.output_type
class GetApplicationGatewayResult:
    """
    ApplicationGateways resource
    """
    def __init__(__self__, authentication_certificates=None, backend_address_pools=None, backend_http_settings_collection=None, etag=None, frontend_ip_configurations=None, frontend_ports=None, gateway_ip_configurations=None, http_listeners=None, id=None, location=None, name=None, operational_state=None, probes=None, provisioning_state=None, request_routing_rules=None, resource_guid=None, sku=None, ssl_certificates=None, ssl_policy=None, tags=None, type=None, url_path_maps=None):
        if authentication_certificates and not isinstance(authentication_certificates, list):
            raise TypeError("Expected argument 'authentication_certificates' to be a list")
        pulumi.set(__self__, "authentication_certificates", authentication_certificates)
        if backend_address_pools and not isinstance(backend_address_pools, list):
            raise TypeError("Expected argument 'backend_address_pools' to be a list")
        pulumi.set(__self__, "backend_address_pools", backend_address_pools)
        if backend_http_settings_collection and not isinstance(backend_http_settings_collection, list):
            raise TypeError("Expected argument 'backend_http_settings_collection' to be a list")
        pulumi.set(__self__, "backend_http_settings_collection", backend_http_settings_collection)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if frontend_ip_configurations and not isinstance(frontend_ip_configurations, list):
            raise TypeError("Expected argument 'frontend_ip_configurations' to be a list")
        pulumi.set(__self__, "frontend_ip_configurations", frontend_ip_configurations)
        if frontend_ports and not isinstance(frontend_ports, list):
            raise TypeError("Expected argument 'frontend_ports' to be a list")
        pulumi.set(__self__, "frontend_ports", frontend_ports)
        if gateway_ip_configurations and not isinstance(gateway_ip_configurations, list):
            raise TypeError("Expected argument 'gateway_ip_configurations' to be a list")
        pulumi.set(__self__, "gateway_ip_configurations", gateway_ip_configurations)
        if http_listeners and not isinstance(http_listeners, list):
            raise TypeError("Expected argument 'http_listeners' to be a list")
        pulumi.set(__self__, "http_listeners", http_listeners)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if operational_state and not isinstance(operational_state, str):
            raise TypeError("Expected argument 'operational_state' to be a str")
        pulumi.set(__self__, "operational_state", operational_state)
        if probes and not isinstance(probes, list):
            raise TypeError("Expected argument 'probes' to be a list")
        pulumi.set(__self__, "probes", probes)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if request_routing_rules and not isinstance(request_routing_rules, list):
            raise TypeError("Expected argument 'request_routing_rules' to be a list")
        pulumi.set(__self__, "request_routing_rules", request_routing_rules)
        if resource_guid and not isinstance(resource_guid, str):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, "resource_guid", resource_guid)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if ssl_certificates and not isinstance(ssl_certificates, list):
            raise TypeError("Expected argument 'ssl_certificates' to be a list")
        pulumi.set(__self__, "ssl_certificates", ssl_certificates)
        if ssl_policy and not isinstance(ssl_policy, dict):
            raise TypeError("Expected argument 'ssl_policy' to be a dict")
        pulumi.set(__self__, "ssl_policy", ssl_policy)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if url_path_maps and not isinstance(url_path_maps, list):
            raise TypeError("Expected argument 'url_path_maps' to be a list")
        pulumi.set(__self__, "url_path_maps", url_path_maps)

    @property
    @pulumi.getter(name="authenticationCertificates")
    def authentication_certificates(self) -> Optional[Sequence['outputs.ApplicationGatewayAuthenticationCertificateResponse']]:
        """
        Authentication certificates of application gateway resource
        """
        return pulumi.get(self, "authentication_certificates")

    @property
    @pulumi.getter(name="backendAddressPools")
    def backend_address_pools(self) -> Optional[Sequence['outputs.ApplicationGatewayBackendAddressPoolResponse']]:
        """
        Backend address pool of application gateway resource
        """
        return pulumi.get(self, "backend_address_pools")

    @property
    @pulumi.getter(name="backendHttpSettingsCollection")
    def backend_http_settings_collection(self) -> Optional[Sequence['outputs.ApplicationGatewayBackendHttpSettingsResponse']]:
        """
        Backend http settings of application gateway resource
        """
        return pulumi.get(self, "backend_http_settings_collection")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        A unique read-only string that changes whenever the resource is updated
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="frontendIPConfigurations")
    def frontend_ip_configurations(self) -> Optional[Sequence['outputs.ApplicationGatewayFrontendIPConfigurationResponse']]:
        """
        Frontend IP addresses of application gateway resource
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @property
    @pulumi.getter(name="frontendPorts")
    def frontend_ports(self) -> Optional[Sequence['outputs.ApplicationGatewayFrontendPortResponse']]:
        """
        Frontend ports of application gateway resource
        """
        return pulumi.get(self, "frontend_ports")

    @property
    @pulumi.getter(name="gatewayIPConfigurations")
    def gateway_ip_configurations(self) -> Optional[Sequence['outputs.ApplicationGatewayIPConfigurationResponse']]:
        """
        Subnets of application gateway resource
        """
        return pulumi.get(self, "gateway_ip_configurations")

    @property
    @pulumi.getter(name="httpListeners")
    def http_listeners(self) -> Optional[Sequence['outputs.ApplicationGatewayHttpListenerResponse']]:
        """
        HTTP listeners of application gateway resource
        """
        return pulumi.get(self, "http_listeners")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="operationalState")
    def operational_state(self) -> str:
        """
        Operational state of application gateway resource
        """
        return pulumi.get(self, "operational_state")

    @property
    @pulumi.getter
    def probes(self) -> Optional[Sequence['outputs.ApplicationGatewayProbeResponse']]:
        """
        Probes of application gateway resource
        """
        return pulumi.get(self, "probes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state of the ApplicationGateway resource Updating/Deleting/Failed
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="requestRoutingRules")
    def request_routing_rules(self) -> Optional[Sequence['outputs.ApplicationGatewayRequestRoutingRuleResponse']]:
        """
        Request routing rules of application gateway resource
        """
        return pulumi.get(self, "request_routing_rules")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> Optional[str]:
        """
        Resource guid property of the ApplicationGateway resource
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.ApplicationGatewaySkuResponse']:
        """
        Sku of application gateway resource
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="sslCertificates")
    def ssl_certificates(self) -> Optional[Sequence['outputs.ApplicationGatewaySslCertificateResponse']]:
        """
        SSL certificates of application gateway resource
        """
        return pulumi.get(self, "ssl_certificates")

    @property
    @pulumi.getter(name="sslPolicy")
    def ssl_policy(self) -> Optional['outputs.ApplicationGatewaySslPolicyResponse']:
        """
        SSL policy of application gateway resource
        """
        return pulumi.get(self, "ssl_policy")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="urlPathMaps")
    def url_path_maps(self) -> Optional[Sequence['outputs.ApplicationGatewayUrlPathMapResponse']]:
        """
        URL path map of application gateway resource
        """
        return pulumi.get(self, "url_path_maps")


class AwaitableGetApplicationGatewayResult(GetApplicationGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationGatewayResult(
            authentication_certificates=self.authentication_certificates,
            backend_address_pools=self.backend_address_pools,
            backend_http_settings_collection=self.backend_http_settings_collection,
            etag=self.etag,
            frontend_ip_configurations=self.frontend_ip_configurations,
            frontend_ports=self.frontend_ports,
            gateway_ip_configurations=self.gateway_ip_configurations,
            http_listeners=self.http_listeners,
            id=self.id,
            location=self.location,
            name=self.name,
            operational_state=self.operational_state,
            probes=self.probes,
            provisioning_state=self.provisioning_state,
            request_routing_rules=self.request_routing_rules,
            resource_guid=self.resource_guid,
            sku=self.sku,
            ssl_certificates=self.ssl_certificates,
            ssl_policy=self.ssl_policy,
            tags=self.tags,
            type=self.type,
            url_path_maps=self.url_path_maps)


def get_application_gateway(application_gateway_name: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationGatewayResult:
    """
    ApplicationGateways resource


    :param str application_gateway_name: The name of the application gateway.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['applicationGatewayName'] = application_gateway_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20160601:getApplicationGateway', __args__, opts=opts, typ=GetApplicationGatewayResult).value

    return AwaitableGetApplicationGatewayResult(
        authentication_certificates=__ret__.authentication_certificates,
        backend_address_pools=__ret__.backend_address_pools,
        backend_http_settings_collection=__ret__.backend_http_settings_collection,
        etag=__ret__.etag,
        frontend_ip_configurations=__ret__.frontend_ip_configurations,
        frontend_ports=__ret__.frontend_ports,
        gateway_ip_configurations=__ret__.gateway_ip_configurations,
        http_listeners=__ret__.http_listeners,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        operational_state=__ret__.operational_state,
        probes=__ret__.probes,
        provisioning_state=__ret__.provisioning_state,
        request_routing_rules=__ret__.request_routing_rules,
        resource_guid=__ret__.resource_guid,
        sku=__ret__.sku,
        ssl_certificates=__ret__.ssl_certificates,
        ssl_policy=__ret__.ssl_policy,
        tags=__ret__.tags,
        type=__ret__.type,
        url_path_maps=__ret__.url_path_maps)
