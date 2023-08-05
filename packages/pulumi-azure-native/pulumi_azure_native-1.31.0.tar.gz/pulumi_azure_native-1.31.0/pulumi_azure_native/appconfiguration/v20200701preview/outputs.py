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
    'ApiKeyResponse',
    'EncryptionPropertiesResponse',
    'KeyVaultPropertiesResponse',
    'PrivateEndpointConnectionReferenceResponse',
    'PrivateEndpointResponse',
    'PrivateLinkServiceConnectionStateResponse',
    'ResourceIdentityResponse',
    'SkuResponse',
    'UserIdentityResponse',
]

@pulumi.output_type
class ApiKeyResponse(dict):
    """
    An API key used for authenticating with a configuration store endpoint.
    """
    def __init__(__self__, *,
                 connection_string: str,
                 id: str,
                 last_modified: str,
                 name: str,
                 read_only: bool,
                 value: str):
        """
        An API key used for authenticating with a configuration store endpoint.
        :param str connection_string: A connection string that can be used by supporting clients for authentication.
        :param str id: The key ID.
        :param str last_modified: The last time any of the key's properties were modified.
        :param str name: A name for the key describing its usage.
        :param bool read_only: Whether this key can only be used for read operations.
        :param str value: The value of the key that is used for authentication purposes.
        """
        pulumi.set(__self__, "connection_string", connection_string)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "last_modified", last_modified)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "read_only", read_only)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> str:
        """
        A connection string that can be used by supporting clients for authentication.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The key ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        The last time any of the key's properties were modified.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A name for the key describing its usage.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="readOnly")
    def read_only(self) -> bool:
        """
        Whether this key can only be used for read operations.
        """
        return pulumi.get(self, "read_only")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the key that is used for authentication purposes.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class EncryptionPropertiesResponse(dict):
    """
    The encryption settings for a configuration store.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyVaultProperties":
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
                 key_vault_properties: Optional['outputs.KeyVaultPropertiesResponse'] = None):
        """
        The encryption settings for a configuration store.
        :param 'KeyVaultPropertiesResponse' key_vault_properties: Key vault properties.
        """
        if key_vault_properties is not None:
            pulumi.set(__self__, "key_vault_properties", key_vault_properties)

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional['outputs.KeyVaultPropertiesResponse']:
        """
        Key vault properties.
        """
        return pulumi.get(self, "key_vault_properties")


@pulumi.output_type
class KeyVaultPropertiesResponse(dict):
    """
    Settings concerning key vault encryption for a configuration store.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "identityClientId":
            suggest = "identity_client_id"
        elif key == "keyIdentifier":
            suggest = "key_identifier"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyVaultPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyVaultPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyVaultPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 identity_client_id: Optional[str] = None,
                 key_identifier: Optional[str] = None):
        """
        Settings concerning key vault encryption for a configuration store.
        :param str identity_client_id: The client id of the identity which will be used to access key vault.
        :param str key_identifier: The URI of the key vault key used to encrypt data.
        """
        if identity_client_id is not None:
            pulumi.set(__self__, "identity_client_id", identity_client_id)
        if key_identifier is not None:
            pulumi.set(__self__, "key_identifier", key_identifier)

    @property
    @pulumi.getter(name="identityClientId")
    def identity_client_id(self) -> Optional[str]:
        """
        The client id of the identity which will be used to access key vault.
        """
        return pulumi.get(self, "identity_client_id")

    @property
    @pulumi.getter(name="keyIdentifier")
    def key_identifier(self) -> Optional[str]:
        """
        The URI of the key vault key used to encrypt data.
        """
        return pulumi.get(self, "key_identifier")


@pulumi.output_type
class PrivateEndpointConnectionReferenceResponse(dict):
    """
    A reference to a related private endpoint connection.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateLinkServiceConnectionState":
            suggest = "private_link_service_connection_state"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "privateEndpoint":
            suggest = "private_endpoint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateEndpointConnectionReferenceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateEndpointConnectionReferenceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateEndpointConnectionReferenceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 name: str,
                 private_link_service_connection_state: 'outputs.PrivateLinkServiceConnectionStateResponse',
                 provisioning_state: str,
                 type: str,
                 private_endpoint: Optional['outputs.PrivateEndpointResponse'] = None):
        """
        A reference to a related private endpoint connection.
        :param str id: The resource ID.
        :param str name: The name of the resource.
        :param 'PrivateLinkServiceConnectionStateResponse' private_link_service_connection_state: A collection of information about the state of the connection between service consumer and provider.
        :param str provisioning_state: The provisioning status of the private endpoint connection.
        :param str type: The type of the resource.
        :param 'PrivateEndpointResponse' private_endpoint: The resource of private endpoint.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "type", type)
        if private_endpoint is not None:
            pulumi.set(__self__, "private_endpoint", private_endpoint)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> 'outputs.PrivateLinkServiceConnectionStateResponse':
        """
        A collection of information about the state of the connection between service consumer and provider.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning status of the private endpoint connection.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        The resource of private endpoint.
        """
        return pulumi.get(self, "private_endpoint")


@pulumi.output_type
class PrivateEndpointResponse(dict):
    """
    Private endpoint which a connection belongs to.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Private endpoint which a connection belongs to.
        :param str id: The resource Id for private endpoint
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The resource Id for private endpoint
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class PrivateLinkServiceConnectionStateResponse(dict):
    """
    The state of a private link service connection.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionsRequired":
            suggest = "actions_required"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkServiceConnectionStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkServiceConnectionStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkServiceConnectionStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 actions_required: str,
                 description: Optional[str] = None,
                 status: Optional[str] = None):
        """
        The state of a private link service connection.
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
class ResourceIdentityResponse(dict):
    """
    An identity that can be associated with a resource.
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
            pulumi.log.warn(f"Key '{key}' not found in ResourceIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResourceIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResourceIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.UserIdentityResponse']] = None):
        """
        An identity that can be associated with a resource.
        :param str principal_id: The principal id of the identity. This property will only be provided for a system-assigned identity.
        :param str tenant_id: The tenant id associated with the resource's identity. This property will only be provided for a system-assigned identity.
        :param str type: The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
        :param Mapping[str, 'UserIdentityResponse'] user_assigned_identities: The list of user-assigned identities associated with the resource. The user-assigned identity dictionary keys will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
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
        The principal id of the identity. This property will only be provided for a system-assigned identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant id associated with the resource's identity. This property will only be provided for a system-assigned identity.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserIdentityResponse']]:
        """
        The list of user-assigned identities associated with the resource. The user-assigned identity dictionary keys will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class SkuResponse(dict):
    """
    Describes a configuration store SKU.
    """
    def __init__(__self__, *,
                 name: str):
        """
        Describes a configuration store SKU.
        :param str name: The SKU name of the configuration store.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The SKU name of the configuration store.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class UserIdentityResponse(dict):
    """
    A resource identity that is managed by the user of the service.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "principalId":
            suggest = "principal_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        A resource identity that is managed by the user of the service.
        :param str client_id: The client ID of the user-assigned identity.
        :param str principal_id: The principal ID of the user-assigned identity.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client ID of the user-assigned identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of the user-assigned identity.
        """
        return pulumi.get(self, "principal_id")


