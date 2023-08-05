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
    'NetworkProfileArgs',
    'OpenShiftManagedClusterAADIdentityProviderArgs',
    'OpenShiftManagedClusterAgentPoolProfileArgs',
    'OpenShiftManagedClusterAuthProfileArgs',
    'OpenShiftManagedClusterIdentityProviderArgs',
    'OpenShiftManagedClusterMasterPoolProfileArgs',
    'OpenShiftRouterProfileArgs',
    'PurchasePlanArgs',
]

@pulumi.input_type
class NetworkProfileArgs:
    def __init__(__self__, *,
                 peer_vnet_id: Optional[pulumi.Input[str]] = None,
                 vnet_cidr: Optional[pulumi.Input[str]] = None):
        """
        Represents the OpenShift networking configuration
        :param pulumi.Input[str] peer_vnet_id: CIDR of the Vnet to peer.
        :param pulumi.Input[str] vnet_cidr: CIDR for the OpenShift Vnet.
        """
        if peer_vnet_id is not None:
            pulumi.set(__self__, "peer_vnet_id", peer_vnet_id)
        if vnet_cidr is None:
            vnet_cidr = '10.0.0.0/8'
        if vnet_cidr is not None:
            pulumi.set(__self__, "vnet_cidr", vnet_cidr)

    @property
    @pulumi.getter(name="peerVnetId")
    def peer_vnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        CIDR of the Vnet to peer.
        """
        return pulumi.get(self, "peer_vnet_id")

    @peer_vnet_id.setter
    def peer_vnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peer_vnet_id", value)

    @property
    @pulumi.getter(name="vnetCidr")
    def vnet_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        CIDR for the OpenShift Vnet.
        """
        return pulumi.get(self, "vnet_cidr")

    @vnet_cidr.setter
    def vnet_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vnet_cidr", value)


@pulumi.input_type
class OpenShiftManagedClusterAADIdentityProviderArgs:
    def __init__(__self__, *,
                 kind: pulumi.Input[str],
                 client_id: Optional[pulumi.Input[str]] = None,
                 customer_admin_group_id: Optional[pulumi.Input[str]] = None,
                 secret: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        Defines the Identity provider for MS AAD.
        :param pulumi.Input[str] kind: The kind of the provider.
               Expected value is 'AADIdentityProvider'.
        :param pulumi.Input[str] client_id: The clientId password associated with the provider.
        :param pulumi.Input[str] customer_admin_group_id: The groupId to be granted cluster admin role.
        :param pulumi.Input[str] secret: The secret password associated with the provider.
        :param pulumi.Input[str] tenant_id: The tenantId associated with the provider.
        """
        pulumi.set(__self__, "kind", 'AADIdentityProvider')
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if customer_admin_group_id is not None:
            pulumi.set(__self__, "customer_admin_group_id", customer_admin_group_id)
        if secret is not None:
            pulumi.set(__self__, "secret", secret)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of the provider.
        Expected value is 'AADIdentityProvider'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The clientId password associated with the provider.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="customerAdminGroupId")
    def customer_admin_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The groupId to be granted cluster admin role.
        """
        return pulumi.get(self, "customer_admin_group_id")

    @customer_admin_group_id.setter
    def customer_admin_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "customer_admin_group_id", value)

    @property
    @pulumi.getter
    def secret(self) -> Optional[pulumi.Input[str]]:
        """
        The secret password associated with the provider.
        """
        return pulumi.get(self, "secret")

    @secret.setter
    def secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The tenantId associated with the provider.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


@pulumi.input_type
class OpenShiftManagedClusterAgentPoolProfileArgs:
    def __init__(__self__, *,
                 count: pulumi.Input[int],
                 name: pulumi.Input[str],
                 vm_size: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']],
                 os_type: Optional[pulumi.Input[Union[str, 'OSType']]] = None,
                 role: Optional[pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']]] = None,
                 subnet_cidr: Optional[pulumi.Input[str]] = None):
        """
        Defines the configuration of the OpenShift cluster VMs.
        :param pulumi.Input[int] count: Number of agents (VMs) to host docker containers.
        :param pulumi.Input[str] name: Unique name of the pool profile in the context of the subscription and resource group.
        :param pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']] vm_size: Size of agent VMs.
        :param pulumi.Input[Union[str, 'OSType']] os_type: OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        :param pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']] role: Define the role of the AgentPoolProfile.
        :param pulumi.Input[str] subnet_cidr: Subnet CIDR for the peering.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "vm_size", vm_size)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if role is not None:
            pulumi.set(__self__, "role", role)
        if subnet_cidr is None:
            subnet_cidr = '10.0.0.0/24'
        if subnet_cidr is not None:
            pulumi.set(__self__, "subnet_cidr", subnet_cidr)

    @property
    @pulumi.getter
    def count(self) -> pulumi.Input[int]:
        """
        Number of agents (VMs) to host docker containers.
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: pulumi.Input[int]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name of the pool profile in the context of the subscription and resource group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]):
        pulumi.set(self, "vm_size", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[Union[str, 'OSType']]]:
        """
        OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[Union[str, 'OSType']]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']]]:
        """
        Define the role of the AgentPoolProfile.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter(name="subnetCidr")
    def subnet_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        Subnet CIDR for the peering.
        """
        return pulumi.get(self, "subnet_cidr")

    @subnet_cidr.setter
    def subnet_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_cidr", value)


@pulumi.input_type
class OpenShiftManagedClusterAuthProfileArgs:
    def __init__(__self__, *,
                 identity_providers: Optional[pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]]] = None):
        """
        Defines all possible authentication profiles for the OpenShift cluster.
        :param pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]] identity_providers: Type of authentication profile to use.
        """
        if identity_providers is not None:
            pulumi.set(__self__, "identity_providers", identity_providers)

    @property
    @pulumi.getter(name="identityProviders")
    def identity_providers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]]]:
        """
        Type of authentication profile to use.
        """
        return pulumi.get(self, "identity_providers")

    @identity_providers.setter
    def identity_providers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]]]):
        pulumi.set(self, "identity_providers", value)


@pulumi.input_type
class OpenShiftManagedClusterIdentityProviderArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 provider: Optional[pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs']] = None):
        """
        Defines the configuration of the identity providers to be used in the OpenShift cluster.
        :param pulumi.Input[str] name: Name of the provider.
        :param pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs'] provider: Configuration of the provider.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if provider is not None:
            pulumi.set(__self__, "provider", provider)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the provider.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def provider(self) -> Optional[pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs']]:
        """
        Configuration of the provider.
        """
        return pulumi.get(self, "provider")

    @provider.setter
    def provider(self, value: Optional[pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs']]):
        pulumi.set(self, "provider", value)


@pulumi.input_type
class OpenShiftManagedClusterMasterPoolProfileArgs:
    def __init__(__self__, *,
                 count: pulumi.Input[int],
                 vm_size: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']],
                 name: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OSType']]] = None,
                 subnet_cidr: Optional[pulumi.Input[str]] = None):
        """
        OpenShiftManagedClusterMaterPoolProfile contains configuration for OpenShift master VMs.
        :param pulumi.Input[int] count: Number of masters (VMs) to host docker containers. The default value is 3.
        :param pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']] vm_size: Size of agent VMs.
        :param pulumi.Input[str] name: Unique name of the master pool profile in the context of the subscription and resource group.
        :param pulumi.Input[Union[str, 'OSType']] os_type: OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        :param pulumi.Input[str] subnet_cidr: Subnet CIDR for the peering.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "vm_size", vm_size)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if subnet_cidr is not None:
            pulumi.set(__self__, "subnet_cidr", subnet_cidr)

    @property
    @pulumi.getter
    def count(self) -> pulumi.Input[int]:
        """
        Number of masters (VMs) to host docker containers. The default value is 3.
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: pulumi.Input[int]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]):
        pulumi.set(self, "vm_size", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique name of the master pool profile in the context of the subscription and resource group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[Union[str, 'OSType']]]:
        """
        OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[Union[str, 'OSType']]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="subnetCidr")
    def subnet_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        Subnet CIDR for the peering.
        """
        return pulumi.get(self, "subnet_cidr")

    @subnet_cidr.setter
    def subnet_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_cidr", value)


@pulumi.input_type
class OpenShiftRouterProfileArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 public_subdomain: Optional[pulumi.Input[str]] = None):
        """
        Represents an OpenShift router
        :param pulumi.Input[str] name: Name of the router profile.
        :param pulumi.Input[str] public_subdomain: DNS subdomain for OpenShift router.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if public_subdomain is not None:
            pulumi.set(__self__, "public_subdomain", public_subdomain)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the router profile.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="publicSubdomain")
    def public_subdomain(self) -> Optional[pulumi.Input[str]]:
        """
        DNS subdomain for OpenShift router.
        """
        return pulumi.get(self, "public_subdomain")

    @public_subdomain.setter
    def public_subdomain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_subdomain", value)


@pulumi.input_type
class PurchasePlanArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 product: Optional[pulumi.Input[str]] = None,
                 promotion_code: Optional[pulumi.Input[str]] = None,
                 publisher: Optional[pulumi.Input[str]] = None):
        """
        Used for establishing the purchase context of any 3rd Party artifact through MarketPlace.
        :param pulumi.Input[str] name: The plan ID.
        :param pulumi.Input[str] product: Specifies the product of the image from the marketplace. This is the same value as Offer under the imageReference element.
        :param pulumi.Input[str] promotion_code: The promotion code.
        :param pulumi.Input[str] publisher: The plan ID.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if product is not None:
            pulumi.set(__self__, "product", product)
        if promotion_code is not None:
            pulumi.set(__self__, "promotion_code", promotion_code)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The plan ID.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def product(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the product of the image from the marketplace. This is the same value as Offer under the imageReference element.
        """
        return pulumi.get(self, "product")

    @product.setter
    def product(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "product", value)

    @property
    @pulumi.getter(name="promotionCode")
    def promotion_code(self) -> Optional[pulumi.Input[str]]:
        """
        The promotion code.
        """
        return pulumi.get(self, "promotion_code")

    @promotion_code.setter
    def promotion_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "promotion_code", value)

    @property
    @pulumi.getter
    def publisher(self) -> Optional[pulumi.Input[str]]:
        """
        The plan ID.
        """
        return pulumi.get(self, "publisher")

    @publisher.setter
    def publisher(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "publisher", value)


