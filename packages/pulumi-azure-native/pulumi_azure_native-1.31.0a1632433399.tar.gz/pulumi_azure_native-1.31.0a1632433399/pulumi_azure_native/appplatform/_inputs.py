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
    'AppResourcePropertiesArgs',
    'BindingResourcePropertiesArgs',
    'CertificatePropertiesArgs',
    'ClusterResourcePropertiesArgs',
    'CustomDomainPropertiesArgs',
    'DeploymentResourcePropertiesArgs',
    'DeploymentSettingsArgs',
    'ManagedIdentityPropertiesArgs',
    'NetworkProfileArgs',
    'PersistentDiskArgs',
    'SkuArgs',
    'TemporaryDiskArgs',
    'UserSourceInfoArgs',
]

@pulumi.input_type
class AppResourcePropertiesArgs:
    def __init__(__self__, *,
                 active_deployment_name: Optional[pulumi.Input[str]] = None,
                 fqdn: Optional[pulumi.Input[str]] = None,
                 https_only: Optional[pulumi.Input[bool]] = None,
                 persistent_disk: Optional[pulumi.Input['PersistentDiskArgs']] = None,
                 public: Optional[pulumi.Input[bool]] = None,
                 temporary_disk: Optional[pulumi.Input['TemporaryDiskArgs']] = None):
        """
        App resource properties payload
        :param pulumi.Input[str] active_deployment_name: Name of the active deployment of the App
        :param pulumi.Input[str] fqdn: Fully qualified dns Name.
        :param pulumi.Input[bool] https_only: Indicate if only https is allowed.
        :param pulumi.Input['PersistentDiskArgs'] persistent_disk: Persistent disk settings
        :param pulumi.Input[bool] public: Indicates whether the App exposes public endpoint
        :param pulumi.Input['TemporaryDiskArgs'] temporary_disk: Temporary disk settings
        """
        if active_deployment_name is not None:
            pulumi.set(__self__, "active_deployment_name", active_deployment_name)
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if https_only is None:
            https_only = False
        if https_only is not None:
            pulumi.set(__self__, "https_only", https_only)
        if persistent_disk is not None:
            pulumi.set(__self__, "persistent_disk", persistent_disk)
        if public is not None:
            pulumi.set(__self__, "public", public)
        if temporary_disk is not None:
            pulumi.set(__self__, "temporary_disk", temporary_disk)

    @property
    @pulumi.getter(name="activeDeploymentName")
    def active_deployment_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the active deployment of the App
        """
        return pulumi.get(self, "active_deployment_name")

    @active_deployment_name.setter
    def active_deployment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "active_deployment_name", value)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        Fully qualified dns Name.
        """
        return pulumi.get(self, "fqdn")

    @fqdn.setter
    def fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fqdn", value)

    @property
    @pulumi.getter(name="httpsOnly")
    def https_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicate if only https is allowed.
        """
        return pulumi.get(self, "https_only")

    @https_only.setter
    def https_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "https_only", value)

    @property
    @pulumi.getter(name="persistentDisk")
    def persistent_disk(self) -> Optional[pulumi.Input['PersistentDiskArgs']]:
        """
        Persistent disk settings
        """
        return pulumi.get(self, "persistent_disk")

    @persistent_disk.setter
    def persistent_disk(self, value: Optional[pulumi.Input['PersistentDiskArgs']]):
        pulumi.set(self, "persistent_disk", value)

    @property
    @pulumi.getter
    def public(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the App exposes public endpoint
        """
        return pulumi.get(self, "public")

    @public.setter
    def public(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "public", value)

    @property
    @pulumi.getter(name="temporaryDisk")
    def temporary_disk(self) -> Optional[pulumi.Input['TemporaryDiskArgs']]:
        """
        Temporary disk settings
        """
        return pulumi.get(self, "temporary_disk")

    @temporary_disk.setter
    def temporary_disk(self, value: Optional[pulumi.Input['TemporaryDiskArgs']]):
        pulumi.set(self, "temporary_disk", value)


@pulumi.input_type
class BindingResourcePropertiesArgs:
    def __init__(__self__, *,
                 binding_parameters: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        Binding resource properties payload
        :param pulumi.Input[Mapping[str, Any]] binding_parameters: Binding parameters of the Binding resource
        :param pulumi.Input[str] key: The key of the bound resource
        :param pulumi.Input[str] resource_id: The Azure resource id of the bound resource
        """
        if binding_parameters is not None:
            pulumi.set(__self__, "binding_parameters", binding_parameters)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="bindingParameters")
    def binding_parameters(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Binding parameters of the Binding resource
        """
        return pulumi.get(self, "binding_parameters")

    @binding_parameters.setter
    def binding_parameters(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "binding_parameters", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        The key of the bound resource
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure resource id of the bound resource
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class CertificatePropertiesArgs:
    def __init__(__self__, *,
                 key_vault_cert_name: pulumi.Input[str],
                 vault_uri: pulumi.Input[str],
                 cert_version: Optional[pulumi.Input[str]] = None):
        """
        Certificate resource payload.
        :param pulumi.Input[str] key_vault_cert_name: The certificate name of key vault.
        :param pulumi.Input[str] vault_uri: The vault uri of user key vault.
        :param pulumi.Input[str] cert_version: The certificate version of key vault.
        """
        pulumi.set(__self__, "key_vault_cert_name", key_vault_cert_name)
        pulumi.set(__self__, "vault_uri", vault_uri)
        if cert_version is not None:
            pulumi.set(__self__, "cert_version", cert_version)

    @property
    @pulumi.getter(name="keyVaultCertName")
    def key_vault_cert_name(self) -> pulumi.Input[str]:
        """
        The certificate name of key vault.
        """
        return pulumi.get(self, "key_vault_cert_name")

    @key_vault_cert_name.setter
    def key_vault_cert_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_vault_cert_name", value)

    @property
    @pulumi.getter(name="vaultUri")
    def vault_uri(self) -> pulumi.Input[str]:
        """
        The vault uri of user key vault.
        """
        return pulumi.get(self, "vault_uri")

    @vault_uri.setter
    def vault_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_uri", value)

    @property
    @pulumi.getter(name="certVersion")
    def cert_version(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate version of key vault.
        """
        return pulumi.get(self, "cert_version")

    @cert_version.setter
    def cert_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cert_version", value)


@pulumi.input_type
class ClusterResourcePropertiesArgs:
    def __init__(__self__, *,
                 network_profile: Optional[pulumi.Input['NetworkProfileArgs']] = None):
        """
        Service properties payload
        :param pulumi.Input['NetworkProfileArgs'] network_profile: Network profile of the Service
        """
        if network_profile is not None:
            pulumi.set(__self__, "network_profile", network_profile)

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> Optional[pulumi.Input['NetworkProfileArgs']]:
        """
        Network profile of the Service
        """
        return pulumi.get(self, "network_profile")

    @network_profile.setter
    def network_profile(self, value: Optional[pulumi.Input['NetworkProfileArgs']]):
        pulumi.set(self, "network_profile", value)


@pulumi.input_type
class CustomDomainPropertiesArgs:
    def __init__(__self__, *,
                 cert_name: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None):
        """
        Custom domain of app resource payload.
        :param pulumi.Input[str] cert_name: The bound certificate name of domain.
        :param pulumi.Input[str] thumbprint: The thumbprint of bound certificate.
        """
        if cert_name is not None:
            pulumi.set(__self__, "cert_name", cert_name)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)

    @property
    @pulumi.getter(name="certName")
    def cert_name(self) -> Optional[pulumi.Input[str]]:
        """
        The bound certificate name of domain.
        """
        return pulumi.get(self, "cert_name")

    @cert_name.setter
    def cert_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cert_name", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        The thumbprint of bound certificate.
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint", value)


@pulumi.input_type
class DeploymentResourcePropertiesArgs:
    def __init__(__self__, *,
                 deployment_settings: Optional[pulumi.Input['DeploymentSettingsArgs']] = None,
                 source: Optional[pulumi.Input['UserSourceInfoArgs']] = None):
        """
        Deployment resource properties payload
        :param pulumi.Input['DeploymentSettingsArgs'] deployment_settings: Deployment settings of the Deployment
        :param pulumi.Input['UserSourceInfoArgs'] source: Uploaded source information of the deployment.
        """
        if deployment_settings is not None:
            pulumi.set(__self__, "deployment_settings", deployment_settings)
        if source is not None:
            pulumi.set(__self__, "source", source)

    @property
    @pulumi.getter(name="deploymentSettings")
    def deployment_settings(self) -> Optional[pulumi.Input['DeploymentSettingsArgs']]:
        """
        Deployment settings of the Deployment
        """
        return pulumi.get(self, "deployment_settings")

    @deployment_settings.setter
    def deployment_settings(self, value: Optional[pulumi.Input['DeploymentSettingsArgs']]):
        pulumi.set(self, "deployment_settings", value)

    @property
    @pulumi.getter
    def source(self) -> Optional[pulumi.Input['UserSourceInfoArgs']]:
        """
        Uploaded source information of the deployment.
        """
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: Optional[pulumi.Input['UserSourceInfoArgs']]):
        pulumi.set(self, "source", value)


@pulumi.input_type
class DeploymentSettingsArgs:
    def __init__(__self__, *,
                 cpu: Optional[pulumi.Input[int]] = None,
                 environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 jvm_options: Optional[pulumi.Input[str]] = None,
                 memory_in_gb: Optional[pulumi.Input[int]] = None,
                 net_core_main_entry_path: Optional[pulumi.Input[str]] = None,
                 runtime_version: Optional[pulumi.Input[Union[str, 'RuntimeVersion']]] = None):
        """
        Deployment settings payload
        :param pulumi.Input[int] cpu: Required CPU, basic tier should be 1, standard tier should be in range (1, 4)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment_variables: Collection of environment variables
        :param pulumi.Input[str] jvm_options: JVM parameter
        :param pulumi.Input[int] memory_in_gb: Required Memory size in GB, basic tier should be in range (1, 2), standard tier should be in range (1, 8)
        :param pulumi.Input[str] net_core_main_entry_path: The path to the .NET executable relative to zip root
        :param pulumi.Input[Union[str, 'RuntimeVersion']] runtime_version: Runtime version
        """
        if cpu is None:
            cpu = 1
        if cpu is not None:
            pulumi.set(__self__, "cpu", cpu)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if jvm_options is not None:
            pulumi.set(__self__, "jvm_options", jvm_options)
        if memory_in_gb is None:
            memory_in_gb = 1
        if memory_in_gb is not None:
            pulumi.set(__self__, "memory_in_gb", memory_in_gb)
        if net_core_main_entry_path is not None:
            pulumi.set(__self__, "net_core_main_entry_path", net_core_main_entry_path)
        if runtime_version is None:
            runtime_version = 'Java_8'
        if runtime_version is not None:
            pulumi.set(__self__, "runtime_version", runtime_version)

    @property
    @pulumi.getter
    def cpu(self) -> Optional[pulumi.Input[int]]:
        """
        Required CPU, basic tier should be 1, standard tier should be in range (1, 4)
        """
        return pulumi.get(self, "cpu")

    @cpu.setter
    def cpu(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cpu", value)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Collection of environment variables
        """
        return pulumi.get(self, "environment_variables")

    @environment_variables.setter
    def environment_variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "environment_variables", value)

    @property
    @pulumi.getter(name="jvmOptions")
    def jvm_options(self) -> Optional[pulumi.Input[str]]:
        """
        JVM parameter
        """
        return pulumi.get(self, "jvm_options")

    @jvm_options.setter
    def jvm_options(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "jvm_options", value)

    @property
    @pulumi.getter(name="memoryInGB")
    def memory_in_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Required Memory size in GB, basic tier should be in range (1, 2), standard tier should be in range (1, 8)
        """
        return pulumi.get(self, "memory_in_gb")

    @memory_in_gb.setter
    def memory_in_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "memory_in_gb", value)

    @property
    @pulumi.getter(name="netCoreMainEntryPath")
    def net_core_main_entry_path(self) -> Optional[pulumi.Input[str]]:
        """
        The path to the .NET executable relative to zip root
        """
        return pulumi.get(self, "net_core_main_entry_path")

    @net_core_main_entry_path.setter
    def net_core_main_entry_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "net_core_main_entry_path", value)

    @property
    @pulumi.getter(name="runtimeVersion")
    def runtime_version(self) -> Optional[pulumi.Input[Union[str, 'RuntimeVersion']]]:
        """
        Runtime version
        """
        return pulumi.get(self, "runtime_version")

    @runtime_version.setter
    def runtime_version(self, value: Optional[pulumi.Input[Union[str, 'RuntimeVersion']]]):
        pulumi.set(self, "runtime_version", value)


@pulumi.input_type
class ManagedIdentityPropertiesArgs:
    def __init__(__self__, *,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[Union[str, 'ManagedIdentityType']]] = None):
        """
        Managed identity properties retrieved from ARM request headers.
        :param pulumi.Input[str] principal_id: Principal Id
        :param pulumi.Input[str] tenant_id: Tenant Id
        :param pulumi.Input[Union[str, 'ManagedIdentityType']] type: Type of the managed identity
        """
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        Principal Id
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        Tenant Id
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ManagedIdentityType']]]:
        """
        Type of the managed identity
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ManagedIdentityType']]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class NetworkProfileArgs:
    def __init__(__self__, *,
                 app_network_resource_group: Optional[pulumi.Input[str]] = None,
                 app_subnet_id: Optional[pulumi.Input[str]] = None,
                 service_cidr: Optional[pulumi.Input[str]] = None,
                 service_runtime_network_resource_group: Optional[pulumi.Input[str]] = None,
                 service_runtime_subnet_id: Optional[pulumi.Input[str]] = None):
        """
        Service network profile payload
        :param pulumi.Input[str] app_network_resource_group: Name of the resource group containing network resources of Azure Spring Cloud Apps
        :param pulumi.Input[str] app_subnet_id: Fully qualified resource Id of the subnet to host Azure Spring Cloud Apps
        :param pulumi.Input[str] service_cidr: Azure Spring Cloud service reserved CIDR
        :param pulumi.Input[str] service_runtime_network_resource_group: Name of the resource group containing network resources of Azure Spring Cloud Service Runtime
        :param pulumi.Input[str] service_runtime_subnet_id: Fully qualified resource Id of the subnet to host Azure Spring Cloud Service Runtime
        """
        if app_network_resource_group is not None:
            pulumi.set(__self__, "app_network_resource_group", app_network_resource_group)
        if app_subnet_id is not None:
            pulumi.set(__self__, "app_subnet_id", app_subnet_id)
        if service_cidr is not None:
            pulumi.set(__self__, "service_cidr", service_cidr)
        if service_runtime_network_resource_group is not None:
            pulumi.set(__self__, "service_runtime_network_resource_group", service_runtime_network_resource_group)
        if service_runtime_subnet_id is not None:
            pulumi.set(__self__, "service_runtime_subnet_id", service_runtime_subnet_id)

    @property
    @pulumi.getter(name="appNetworkResourceGroup")
    def app_network_resource_group(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource group containing network resources of Azure Spring Cloud Apps
        """
        return pulumi.get(self, "app_network_resource_group")

    @app_network_resource_group.setter
    def app_network_resource_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_network_resource_group", value)

    @property
    @pulumi.getter(name="appSubnetId")
    def app_subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        Fully qualified resource Id of the subnet to host Azure Spring Cloud Apps
        """
        return pulumi.get(self, "app_subnet_id")

    @app_subnet_id.setter
    def app_subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_subnet_id", value)

    @property
    @pulumi.getter(name="serviceCidr")
    def service_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        Azure Spring Cloud service reserved CIDR
        """
        return pulumi.get(self, "service_cidr")

    @service_cidr.setter
    def service_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_cidr", value)

    @property
    @pulumi.getter(name="serviceRuntimeNetworkResourceGroup")
    def service_runtime_network_resource_group(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource group containing network resources of Azure Spring Cloud Service Runtime
        """
        return pulumi.get(self, "service_runtime_network_resource_group")

    @service_runtime_network_resource_group.setter
    def service_runtime_network_resource_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_runtime_network_resource_group", value)

    @property
    @pulumi.getter(name="serviceRuntimeSubnetId")
    def service_runtime_subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        Fully qualified resource Id of the subnet to host Azure Spring Cloud Service Runtime
        """
        return pulumi.get(self, "service_runtime_subnet_id")

    @service_runtime_subnet_id.setter
    def service_runtime_subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_runtime_subnet_id", value)


@pulumi.input_type
class PersistentDiskArgs:
    def __init__(__self__, *,
                 mount_path: Optional[pulumi.Input[str]] = None,
                 size_in_gb: Optional[pulumi.Input[int]] = None):
        """
        Persistent disk payload
        :param pulumi.Input[str] mount_path: Mount path of the persistent disk
        :param pulumi.Input[int] size_in_gb: Size of the persistent disk in GB
        """
        if mount_path is not None:
            pulumi.set(__self__, "mount_path", mount_path)
        if size_in_gb is not None:
            pulumi.set(__self__, "size_in_gb", size_in_gb)

    @property
    @pulumi.getter(name="mountPath")
    def mount_path(self) -> Optional[pulumi.Input[str]]:
        """
        Mount path of the persistent disk
        """
        return pulumi.get(self, "mount_path")

    @mount_path.setter
    def mount_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mount_path", value)

    @property
    @pulumi.getter(name="sizeInGB")
    def size_in_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Size of the persistent disk in GB
        """
        return pulumi.get(self, "size_in_gb")

    @size_in_gb.setter
    def size_in_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size_in_gb", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 capacity: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[str]] = None):
        """
        Sku of Azure Spring Cloud
        :param pulumi.Input[int] capacity: Current capacity of the target resource
        :param pulumi.Input[str] name: Name of the Sku
        :param pulumi.Input[str] tier: Tier of the Sku
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        Current capacity of the target resource
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Sku
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[str]]:
        """
        Tier of the Sku
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class TemporaryDiskArgs:
    def __init__(__self__, *,
                 mount_path: Optional[pulumi.Input[str]] = None,
                 size_in_gb: Optional[pulumi.Input[int]] = None):
        """
        Temporary disk payload
        :param pulumi.Input[str] mount_path: Mount path of the temporary disk
        :param pulumi.Input[int] size_in_gb: Size of the temporary disk in GB
        """
        if mount_path is None:
            mount_path = '/tmp'
        if mount_path is not None:
            pulumi.set(__self__, "mount_path", mount_path)
        if size_in_gb is not None:
            pulumi.set(__self__, "size_in_gb", size_in_gb)

    @property
    @pulumi.getter(name="mountPath")
    def mount_path(self) -> Optional[pulumi.Input[str]]:
        """
        Mount path of the temporary disk
        """
        return pulumi.get(self, "mount_path")

    @mount_path.setter
    def mount_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mount_path", value)

    @property
    @pulumi.getter(name="sizeInGB")
    def size_in_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Size of the temporary disk in GB
        """
        return pulumi.get(self, "size_in_gb")

    @size_in_gb.setter
    def size_in_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size_in_gb", value)


@pulumi.input_type
class UserSourceInfoArgs:
    def __init__(__self__, *,
                 artifact_selector: Optional[pulumi.Input[str]] = None,
                 relative_path: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[Union[str, 'UserSourceType']]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Source information for a deployment
        :param pulumi.Input[str] artifact_selector: Selector for the artifact to be used for the deployment for multi-module projects. This should be
               the relative path to the target module/project.
        :param pulumi.Input[str] relative_path: Relative path of the storage which stores the source
        :param pulumi.Input[Union[str, 'UserSourceType']] type: Type of the source uploaded
        :param pulumi.Input[str] version: Version of the source
        """
        if artifact_selector is not None:
            pulumi.set(__self__, "artifact_selector", artifact_selector)
        if relative_path is not None:
            pulumi.set(__self__, "relative_path", relative_path)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="artifactSelector")
    def artifact_selector(self) -> Optional[pulumi.Input[str]]:
        """
        Selector for the artifact to be used for the deployment for multi-module projects. This should be
        the relative path to the target module/project.
        """
        return pulumi.get(self, "artifact_selector")

    @artifact_selector.setter
    def artifact_selector(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_selector", value)

    @property
    @pulumi.getter(name="relativePath")
    def relative_path(self) -> Optional[pulumi.Input[str]]:
        """
        Relative path of the storage which stores the source
        """
        return pulumi.get(self, "relative_path")

    @relative_path.setter
    def relative_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "relative_path", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'UserSourceType']]]:
        """
        Type of the source uploaded
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'UserSourceType']]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the source
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


