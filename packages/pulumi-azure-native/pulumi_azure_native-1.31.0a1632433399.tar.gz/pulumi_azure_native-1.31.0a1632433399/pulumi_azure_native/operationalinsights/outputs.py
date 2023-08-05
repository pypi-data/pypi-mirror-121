# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'AssociatedWorkspaceResponse',
    'CapacityReservationPropertiesResponse',
    'ClusterSkuResponse',
    'IdentityResponse',
    'KeyVaultPropertiesResponse',
    'LogAnalyticsQueryPackQueryPropertiesResponseRelated',
    'MachineReferenceWithHintsResponse',
    'PrivateLinkScopedResourceResponse',
    'StorageAccountResponse',
    'StorageInsightStatusResponse',
    'SystemDataResponse',
    'TagResponse',
    'UserIdentityPropertiesResponse',
    'WorkspaceCappingResponse',
    'WorkspaceFeaturesResponse',
    'WorkspaceSkuResponse',
]

@pulumi.output_type
class AssociatedWorkspaceResponse(dict):
    """
    The list of Log Analytics workspaces associated with the cluster.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "associateDate":
            suggest = "associate_date"
        elif key == "resourceId":
            suggest = "resource_id"
        elif key == "workspaceId":
            suggest = "workspace_id"
        elif key == "workspaceName":
            suggest = "workspace_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssociatedWorkspaceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssociatedWorkspaceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssociatedWorkspaceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 associate_date: str,
                 resource_id: str,
                 workspace_id: str,
                 workspace_name: str):
        """
        The list of Log Analytics workspaces associated with the cluster.
        :param str associate_date: The time of workspace association.
        :param str resource_id: The ResourceId id the assigned workspace.
        :param str workspace_id: The id of the assigned workspace.
        :param str workspace_name: The name id the assigned workspace.
        """
        pulumi.set(__self__, "associate_date", associate_date)
        pulumi.set(__self__, "resource_id", resource_id)
        pulumi.set(__self__, "workspace_id", workspace_id)
        pulumi.set(__self__, "workspace_name", workspace_name)

    @property
    @pulumi.getter(name="associateDate")
    def associate_date(self) -> str:
        """
        The time of workspace association.
        """
        return pulumi.get(self, "associate_date")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        """
        The ResourceId id the assigned workspace.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        """
        The id of the assigned workspace.
        """
        return pulumi.get(self, "workspace_id")

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> str:
        """
        The name id the assigned workspace.
        """
        return pulumi.get(self, "workspace_name")


@pulumi.output_type
class CapacityReservationPropertiesResponse(dict):
    """
    The Capacity Reservation properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastSkuUpdate":
            suggest = "last_sku_update"
        elif key == "minCapacity":
            suggest = "min_capacity"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CapacityReservationPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CapacityReservationPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CapacityReservationPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 last_sku_update: str,
                 min_capacity: float):
        """
        The Capacity Reservation properties.
        :param str last_sku_update: The last time Sku was updated.
        :param float min_capacity: Minimum CapacityReservation value in GB.
        """
        pulumi.set(__self__, "last_sku_update", last_sku_update)
        pulumi.set(__self__, "min_capacity", min_capacity)

    @property
    @pulumi.getter(name="lastSkuUpdate")
    def last_sku_update(self) -> str:
        """
        The last time Sku was updated.
        """
        return pulumi.get(self, "last_sku_update")

    @property
    @pulumi.getter(name="minCapacity")
    def min_capacity(self) -> float:
        """
        Minimum CapacityReservation value in GB.
        """
        return pulumi.get(self, "min_capacity")


@pulumi.output_type
class ClusterSkuResponse(dict):
    """
    The cluster sku definition.
    """
    def __init__(__self__, *,
                 capacity: Optional[float] = None,
                 name: Optional[str] = None):
        """
        The cluster sku definition.
        :param float capacity: The capacity value
        :param str name: The name of the SKU.
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[float]:
        """
        The capacity value
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")


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
                 type: str,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.UserIdentityPropertiesResponse']] = None):
        """
        Identity for the resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: Type of managed service identity.
        :param Mapping[str, 'UserIdentityPropertiesResponse'] user_assigned_identities: The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
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
    def type(self) -> str:
        """
        Type of managed service identity.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserIdentityPropertiesResponse']]:
        """
        The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class KeyVaultPropertiesResponse(dict):
    """
    The key vault properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyName":
            suggest = "key_name"
        elif key == "keyRsaSize":
            suggest = "key_rsa_size"
        elif key == "keyVaultUri":
            suggest = "key_vault_uri"
        elif key == "keyVersion":
            suggest = "key_version"

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
                 key_rsa_size: Optional[int] = None,
                 key_vault_uri: Optional[str] = None,
                 key_version: Optional[str] = None):
        """
        The key vault properties.
        :param str key_name: The name of the key associated with the Log Analytics cluster.
        :param int key_rsa_size: Selected key minimum required size.
        :param str key_vault_uri: The Key Vault uri which holds they key associated with the Log Analytics cluster.
        :param str key_version: The version of the key associated with the Log Analytics cluster.
        """
        if key_name is not None:
            pulumi.set(__self__, "key_name", key_name)
        if key_rsa_size is not None:
            pulumi.set(__self__, "key_rsa_size", key_rsa_size)
        if key_vault_uri is not None:
            pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[str]:
        """
        The name of the key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="keyRsaSize")
    def key_rsa_size(self) -> Optional[int]:
        """
        Selected key minimum required size.
        """
        return pulumi.get(self, "key_rsa_size")

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> Optional[str]:
        """
        The Key Vault uri which holds they key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_vault_uri")

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[str]:
        """
        The version of the key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_version")


@pulumi.output_type
class LogAnalyticsQueryPackQueryPropertiesResponseRelated(dict):
    """
    The related metadata items for the function.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "resourceTypes":
            suggest = "resource_types"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LogAnalyticsQueryPackQueryPropertiesResponseRelated. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LogAnalyticsQueryPackQueryPropertiesResponseRelated.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LogAnalyticsQueryPackQueryPropertiesResponseRelated.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 categories: Optional[Sequence[str]] = None,
                 resource_types: Optional[Sequence[str]] = None,
                 solutions: Optional[Sequence[str]] = None):
        """
        The related metadata items for the function.
        :param Sequence[str] categories: The related categories for the function.
        :param Sequence[str] resource_types: The related resource types for the function.
        :param Sequence[str] solutions: The related Log Analytics solutions for the function.
        """
        if categories is not None:
            pulumi.set(__self__, "categories", categories)
        if resource_types is not None:
            pulumi.set(__self__, "resource_types", resource_types)
        if solutions is not None:
            pulumi.set(__self__, "solutions", solutions)

    @property
    @pulumi.getter
    def categories(self) -> Optional[Sequence[str]]:
        """
        The related categories for the function.
        """
        return pulumi.get(self, "categories")

    @property
    @pulumi.getter(name="resourceTypes")
    def resource_types(self) -> Optional[Sequence[str]]:
        """
        The related resource types for the function.
        """
        return pulumi.get(self, "resource_types")

    @property
    @pulumi.getter
    def solutions(self) -> Optional[Sequence[str]]:
        """
        The related Log Analytics solutions for the function.
        """
        return pulumi.get(self, "solutions")


@pulumi.output_type
class MachineReferenceWithHintsResponse(dict):
    """
    A machine reference with a hint of the machine's name and operating system.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayNameHint":
            suggest = "display_name_hint"
        elif key == "osFamilyHint":
            suggest = "os_family_hint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MachineReferenceWithHintsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MachineReferenceWithHintsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MachineReferenceWithHintsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 display_name_hint: str,
                 id: str,
                 kind: str,
                 name: str,
                 os_family_hint: str,
                 type: str):
        """
        A machine reference with a hint of the machine's name and operating system.
        :param str display_name_hint: Last known display name.
        :param str id: Resource URI.
        :param str kind: Specifies the sub-class of the reference.
               Expected value is 'ref:machinewithhints'.
        :param str name: Resource name.
        :param str os_family_hint: Last known operating system family.
        :param str type: Resource type qualifier.
        """
        pulumi.set(__self__, "display_name_hint", display_name_hint)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "kind", 'ref:machinewithhints')
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "os_family_hint", os_family_hint)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="displayNameHint")
    def display_name_hint(self) -> str:
        """
        Last known display name.
        """
        return pulumi.get(self, "display_name_hint")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource URI.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Specifies the sub-class of the reference.
        Expected value is 'ref:machinewithhints'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osFamilyHint")
    def os_family_hint(self) -> str:
        """
        Last known operating system family.
        """
        return pulumi.get(self, "os_family_hint")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type qualifier.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class PrivateLinkScopedResourceResponse(dict):
    """
    The private link scope resource reference.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "resourceId":
            suggest = "resource_id"
        elif key == "scopeId":
            suggest = "scope_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkScopedResourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkScopedResourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkScopedResourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 resource_id: Optional[str] = None,
                 scope_id: Optional[str] = None):
        """
        The private link scope resource reference.
        :param str resource_id: The full resource Id of the private link scope resource.
        :param str scope_id: The private link scope unique Identifier.
        """
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if scope_id is not None:
            pulumi.set(__self__, "scope_id", scope_id)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The full resource Id of the private link scope resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="scopeId")
    def scope_id(self) -> Optional[str]:
        """
        The private link scope unique Identifier.
        """
        return pulumi.get(self, "scope_id")


@pulumi.output_type
class StorageAccountResponse(dict):
    """
    Describes a storage account connection.
    """
    def __init__(__self__, *,
                 id: str,
                 key: str):
        """
        Describes a storage account connection.
        :param str id: The Azure Resource Manager ID of the storage account resource.
        :param str key: The storage account key.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The Azure Resource Manager ID of the storage account resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The storage account key.
        """
        return pulumi.get(self, "key")


@pulumi.output_type
class StorageInsightStatusResponse(dict):
    """
    The status of the storage insight.
    """
    def __init__(__self__, *,
                 state: str,
                 description: Optional[str] = None):
        """
        The status of the storage insight.
        :param str state: The state of the storage insight connection to the workspace
        :param str description: Description of the state of the storage insight.
        """
        pulumi.set(__self__, "state", state)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the storage insight connection to the workspace
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the state of the storage insight.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Read only system data
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
        Read only system data
        :param str created_at: The timestamp of resource creation (UTC)
        :param str created_by: An identifier for the identity that created the resource
        :param str created_by_type: The type of identity that created the resource
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: An identifier for the identity that last modified the resource
        :param str last_modified_by_type: The type of identity that last modified the resource
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
        The timestamp of resource creation (UTC)
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        An identifier for the identity that created the resource
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource
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
        An identifier for the identity that last modified the resource
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource
        """
        return pulumi.get(self, "last_modified_by_type")


@pulumi.output_type
class TagResponse(dict):
    """
    A tag of a saved search.
    """
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        A tag of a saved search.
        :param str name: The tag name.
        :param str value: The tag value.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The tag name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The tag value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class UserIdentityPropertiesResponse(dict):
    """
    User assigned identity properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "principalId":
            suggest = "principal_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserIdentityPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserIdentityPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserIdentityPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        User assigned identity properties.
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
class WorkspaceCappingResponse(dict):
    """
    The daily volume cap for ingestion.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataIngestionStatus":
            suggest = "data_ingestion_status"
        elif key == "quotaNextResetTime":
            suggest = "quota_next_reset_time"
        elif key == "dailyQuotaGb":
            suggest = "daily_quota_gb"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceCappingResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceCappingResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceCappingResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 data_ingestion_status: str,
                 quota_next_reset_time: str,
                 daily_quota_gb: Optional[float] = None):
        """
        The daily volume cap for ingestion.
        :param str data_ingestion_status: The status of data ingestion for this workspace.
        :param str quota_next_reset_time: The time when the quota will be rest.
        :param float daily_quota_gb: The workspace daily quota for ingestion.
        """
        pulumi.set(__self__, "data_ingestion_status", data_ingestion_status)
        pulumi.set(__self__, "quota_next_reset_time", quota_next_reset_time)
        if daily_quota_gb is not None:
            pulumi.set(__self__, "daily_quota_gb", daily_quota_gb)

    @property
    @pulumi.getter(name="dataIngestionStatus")
    def data_ingestion_status(self) -> str:
        """
        The status of data ingestion for this workspace.
        """
        return pulumi.get(self, "data_ingestion_status")

    @property
    @pulumi.getter(name="quotaNextResetTime")
    def quota_next_reset_time(self) -> str:
        """
        The time when the quota will be rest.
        """
        return pulumi.get(self, "quota_next_reset_time")

    @property
    @pulumi.getter(name="dailyQuotaGb")
    def daily_quota_gb(self) -> Optional[float]:
        """
        The workspace daily quota for ingestion.
        """
        return pulumi.get(self, "daily_quota_gb")


@pulumi.output_type
class WorkspaceFeaturesResponse(dict):
    """
    Workspace features.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clusterResourceId":
            suggest = "cluster_resource_id"
        elif key == "disableLocalAuth":
            suggest = "disable_local_auth"
        elif key == "enableDataExport":
            suggest = "enable_data_export"
        elif key == "enableLogAccessUsingOnlyResourcePermissions":
            suggest = "enable_log_access_using_only_resource_permissions"
        elif key == "immediatePurgeDataOn30Days":
            suggest = "immediate_purge_data_on30_days"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceFeaturesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceFeaturesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceFeaturesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cluster_resource_id: Optional[str] = None,
                 disable_local_auth: Optional[bool] = None,
                 enable_data_export: Optional[bool] = None,
                 enable_log_access_using_only_resource_permissions: Optional[bool] = None,
                 immediate_purge_data_on30_days: Optional[bool] = None):
        """
        Workspace features.
        :param str cluster_resource_id: Dedicated LA cluster resourceId that is linked to the workspaces.
        :param bool disable_local_auth: Disable Non-AAD based Auth.
        :param bool enable_data_export: Flag that indicate if data should be exported.
        :param bool enable_log_access_using_only_resource_permissions: Flag that indicate which permission to use - resource or workspace or both.
        :param bool immediate_purge_data_on30_days: Flag that describes if we want to remove the data after 30 days.
        """
        if cluster_resource_id is not None:
            pulumi.set(__self__, "cluster_resource_id", cluster_resource_id)
        if disable_local_auth is not None:
            pulumi.set(__self__, "disable_local_auth", disable_local_auth)
        if enable_data_export is not None:
            pulumi.set(__self__, "enable_data_export", enable_data_export)
        if enable_log_access_using_only_resource_permissions is not None:
            pulumi.set(__self__, "enable_log_access_using_only_resource_permissions", enable_log_access_using_only_resource_permissions)
        if immediate_purge_data_on30_days is not None:
            pulumi.set(__self__, "immediate_purge_data_on30_days", immediate_purge_data_on30_days)

    @property
    @pulumi.getter(name="clusterResourceId")
    def cluster_resource_id(self) -> Optional[str]:
        """
        Dedicated LA cluster resourceId that is linked to the workspaces.
        """
        return pulumi.get(self, "cluster_resource_id")

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> Optional[bool]:
        """
        Disable Non-AAD based Auth.
        """
        return pulumi.get(self, "disable_local_auth")

    @property
    @pulumi.getter(name="enableDataExport")
    def enable_data_export(self) -> Optional[bool]:
        """
        Flag that indicate if data should be exported.
        """
        return pulumi.get(self, "enable_data_export")

    @property
    @pulumi.getter(name="enableLogAccessUsingOnlyResourcePermissions")
    def enable_log_access_using_only_resource_permissions(self) -> Optional[bool]:
        """
        Flag that indicate which permission to use - resource or workspace or both.
        """
        return pulumi.get(self, "enable_log_access_using_only_resource_permissions")

    @property
    @pulumi.getter(name="immediatePurgeDataOn30Days")
    def immediate_purge_data_on30_days(self) -> Optional[bool]:
        """
        Flag that describes if we want to remove the data after 30 days.
        """
        return pulumi.get(self, "immediate_purge_data_on30_days")


@pulumi.output_type
class WorkspaceSkuResponse(dict):
    """
    The SKU (tier) of a workspace.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastSkuUpdate":
            suggest = "last_sku_update"
        elif key == "capacityReservationLevel":
            suggest = "capacity_reservation_level"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceSkuResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceSkuResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceSkuResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 last_sku_update: str,
                 name: str,
                 capacity_reservation_level: Optional[int] = None):
        """
        The SKU (tier) of a workspace.
        :param str last_sku_update: The last time when the sku was updated.
        :param str name: The name of the SKU.
        :param int capacity_reservation_level: The capacity reservation level for this workspace, when CapacityReservation sku is selected.
        """
        pulumi.set(__self__, "last_sku_update", last_sku_update)
        pulumi.set(__self__, "name", name)
        if capacity_reservation_level is not None:
            pulumi.set(__self__, "capacity_reservation_level", capacity_reservation_level)

    @property
    @pulumi.getter(name="lastSkuUpdate")
    def last_sku_update(self) -> str:
        """
        The last time when the sku was updated.
        """
        return pulumi.get(self, "last_sku_update")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="capacityReservationLevel")
    def capacity_reservation_level(self) -> Optional[int]:
        """
        The capacity reservation level for this workspace, when CapacityReservation sku is selected.
        """
        return pulumi.get(self, "capacity_reservation_level")


