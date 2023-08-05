# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'EncryptionPropertiesResponse',
    'EncryptionPropertiesResponseIdentity',
    'HybridRunbookWorkerLegacyResponse',
    'IdentityResponse',
    'IdentityResponseUserAssignedIdentities',
    'KeyResponse',
    'KeyVaultPropertiesResponse',
    'PrivateEndpointConnectionResponse',
    'PrivateEndpointPropertyResponse',
    'PrivateLinkServiceConnectionStatePropertyResponse',
    'RunAsCredentialAssociationPropertyResponse',
    'SkuResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class EncryptionPropertiesResponse(dict):
    """
    The encryption settings for automation account
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keySource":
            suggest = "key_source"
        elif key == "keyVaultProperties":
            suggest = "key_vault_properties"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EncryptionPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 identity: Optional['outputs.EncryptionPropertiesResponseIdentity'] = None,
                 key_source: Optional[str] = None,
                 key_vault_properties: Optional['outputs.KeyVaultPropertiesResponse'] = None):
        """
        The encryption settings for automation account
        :param 'EncryptionPropertiesResponseIdentity' identity: User identity used for CMK.
        :param str key_source: Encryption Key Source
        :param 'KeyVaultPropertiesResponse' key_vault_properties: Key vault properties.
        """
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if key_source is not None:
            pulumi.set(__self__, "key_source", key_source)
        if key_vault_properties is not None:
            pulumi.set(__self__, "key_vault_properties", key_vault_properties)

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.EncryptionPropertiesResponseIdentity']:
        """
        User identity used for CMK.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="keySource")
    def key_source(self) -> Optional[str]:
        """
        Encryption Key Source
        """
        return pulumi.get(self, "key_source")

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional['outputs.KeyVaultPropertiesResponse']:
        """
        Key vault properties.
        """
        return pulumi.get(self, "key_vault_properties")


@pulumi.output_type
class EncryptionPropertiesResponseIdentity(dict):
    """
    User identity used for CMK.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "userAssignedIdentity":
            suggest = "user_assigned_identity"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionPropertiesResponseIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionPropertiesResponseIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EncryptionPropertiesResponseIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 user_assigned_identity: Optional[Any] = None):
        """
        User identity used for CMK.
        :param Any user_assigned_identity: The user identity used for CMK. It will be an ARM resource id in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        if user_assigned_identity is not None:
            pulumi.set(__self__, "user_assigned_identity", user_assigned_identity)

    @property
    @pulumi.getter(name="userAssignedIdentity")
    def user_assigned_identity(self) -> Optional[Any]:
        """
        The user identity used for CMK. It will be an ARM resource id in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identity")


@pulumi.output_type
class HybridRunbookWorkerLegacyResponse(dict):
    """
    Definition of hybrid runbook worker Legacy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastSeenDateTime":
            suggest = "last_seen_date_time"
        elif key == "registrationTime":
            suggest = "registration_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in HybridRunbookWorkerLegacyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        HybridRunbookWorkerLegacyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        HybridRunbookWorkerLegacyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip: Optional[str] = None,
                 last_seen_date_time: Optional[str] = None,
                 name: Optional[str] = None,
                 registration_time: Optional[str] = None):
        """
        Definition of hybrid runbook worker Legacy.
        :param str ip: Gets or sets the assigned machine IP address.
        :param str last_seen_date_time: Last Heartbeat from the Worker
        :param str name: Gets or sets the worker machine name.
        :param str registration_time: Gets or sets the registration time of the worker machine.
        """
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if last_seen_date_time is not None:
            pulumi.set(__self__, "last_seen_date_time", last_seen_date_time)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if registration_time is not None:
            pulumi.set(__self__, "registration_time", registration_time)

    @property
    @pulumi.getter
    def ip(self) -> Optional[str]:
        """
        Gets or sets the assigned machine IP address.
        """
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter(name="lastSeenDateTime")
    def last_seen_date_time(self) -> Optional[str]:
        """
        Last Heartbeat from the Worker
        """
        return pulumi.get(self, "last_seen_date_time")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets the worker machine name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="registrationTime")
    def registration_time(self) -> Optional[str]:
        """
        Gets or sets the registration time of the worker machine.
        """
        return pulumi.get(self, "registration_time")


@pulumi.output_type
class IdentityResponse(dict):
    """
    Identity for the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"
        elif key == "userAssignedIdentities":
            suggest = "user_assigned_identities"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.IdentityResponseUserAssignedIdentities']] = None):
        """
        Identity for the resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: The identity type.
        :param Mapping[str, 'IdentityResponseUserAssignedIdentities'] user_assigned_identities: The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.IdentityResponseUserAssignedIdentities']]:
        """
        The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class IdentityResponseUserAssignedIdentities(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "principalId":
            suggest = "principal_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityResponseUserAssignedIdentities. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityResponseUserAssignedIdentities.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityResponseUserAssignedIdentities.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        :param str client_id: The client id of user assigned identity.
        :param str principal_id: The principal id of user assigned identity.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client id of user assigned identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, "principal_id")


@pulumi.output_type
class KeyResponse(dict):
    """
    Automation key which is used to register a DSC Node
    """
    def __init__(__self__, *,
                 key_name: str,
                 permissions: str,
                 value: str):
        """
        Automation key which is used to register a DSC Node
        :param str key_name: Automation key name.
        :param str permissions: Automation key permissions.
        :param str value: Value of the Automation Key used for registration.
        """
        pulumi.set(__self__, "key_name", key_name)
        pulumi.set(__self__, "permissions", permissions)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> str:
        """
        Automation key name.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter
    def permissions(self) -> str:
        """
        Automation key permissions.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the Automation Key used for registration.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class KeyVaultPropertiesResponse(dict):
    """
    Settings concerning key vault encryption for a configuration store.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyName":
            suggest = "key_name"
        elif key == "keyVersion":
            suggest = "key_version"
        elif key == "keyvaultUri":
            suggest = "keyvault_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyVaultPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyVaultPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyVaultPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_name: Optional[str] = None,
                 key_version: Optional[str] = None,
                 keyvault_uri: Optional[str] = None):
        """
        Settings concerning key vault encryption for a configuration store.
        :param str key_name: The name of key used to encrypt data.
        :param str key_version: The key version of the key used to encrypt data.
        :param str keyvault_uri: The URI of the key vault key used to encrypt data.
        """
        if key_name is not None:
            pulumi.set(__self__, "key_name", key_name)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)
        if keyvault_uri is not None:
            pulumi.set(__self__, "keyvault_uri", keyvault_uri)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[str]:
        """
        The name of key used to encrypt data.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[str]:
        """
        The key version of the key used to encrypt data.
        """
        return pulumi.get(self, "key_version")

    @property
    @pulumi.getter(name="keyvaultUri")
    def keyvault_uri(self) -> Optional[str]:
        """
        The URI of the key vault key used to encrypt data.
        """
        return pulumi.get(self, "keyvault_uri")


@pulumi.output_type
class PrivateEndpointConnectionResponse(dict):
    """
    A private endpoint connection
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateEndpoint":
            suggest = "private_endpoint"
        elif key == "privateLinkServiceConnectionState":
            suggest = "private_link_service_connection_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateEndpointConnectionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateEndpointConnectionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateEndpointConnectionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 name: str,
                 type: str,
                 private_endpoint: Optional['outputs.PrivateEndpointPropertyResponse'] = None,
                 private_link_service_connection_state: Optional['outputs.PrivateLinkServiceConnectionStatePropertyResponse'] = None):
        """
        A private endpoint connection
        :param str id: Fully qualified resource Id for the resource
        :param str name: The name of the resource
        :param str type: The type of the resource.
        :param 'PrivateEndpointPropertyResponse' private_endpoint: Private endpoint which the connection belongs to.
        :param 'PrivateLinkServiceConnectionStatePropertyResponse' private_link_service_connection_state: Connection State of the Private Endpoint Connection.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        if private_endpoint is not None:
            pulumi.set(__self__, "private_endpoint", private_endpoint)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource
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
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointPropertyResponse']:
        """
        Private endpoint which the connection belongs to.
        """
        return pulumi.get(self, "private_endpoint")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> Optional['outputs.PrivateLinkServiceConnectionStatePropertyResponse']:
        """
        Connection State of the Private Endpoint Connection.
        """
        return pulumi.get(self, "private_link_service_connection_state")


@pulumi.output_type
class PrivateEndpointPropertyResponse(dict):
    """
    Private endpoint which the connection belongs to.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Private endpoint which the connection belongs to.
        :param str id: Resource id of the private endpoint.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource id of the private endpoint.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class PrivateLinkServiceConnectionStatePropertyResponse(dict):
    """
    Connection State of the Private Endpoint Connection.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionsRequired":
            suggest = "actions_required"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkServiceConnectionStatePropertyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkServiceConnectionStatePropertyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkServiceConnectionStatePropertyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 actions_required: str,
                 description: Optional[str] = None,
                 status: Optional[str] = None):
        """
        Connection State of the Private Endpoint Connection.
        :param str actions_required: Any action that is required beyond basic workflow (approve/ reject/ disconnect)
        :param str description: The private link service connection description.
        :param str status: The private link service connection status.
        """
        pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> str:
        """
        Any action that is required beyond basic workflow (approve/ reject/ disconnect)
        """
        return pulumi.get(self, "actions_required")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The private link service connection description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The private link service connection status.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class RunAsCredentialAssociationPropertyResponse(dict):
    """
    Definition of RunAs credential to use for hybrid worker.
    """
    def __init__(__self__, *,
                 name: Optional[str] = None):
        """
        Definition of RunAs credential to use for hybrid worker.
        :param str name: Gets or sets the name of the credential.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets the name of the credential.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class SkuResponse(dict):
    """
    The account SKU.
    """
    def __init__(__self__, *,
                 name: str,
                 capacity: Optional[int] = None,
                 family: Optional[str] = None):
        """
        The account SKU.
        :param str name: Gets or sets the SKU name of the account.
        :param int capacity: Gets or sets the SKU capacity.
        :param str family: Gets or sets the SKU family.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Gets or sets the SKU name of the account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        Gets or sets the SKU capacity.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def family(self) -> Optional[str]:
        """
        Gets or sets the SKU family.
        """
        return pulumi.get(self, "family")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


