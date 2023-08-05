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
    'CreationDataResponse',
    'DiskSkuResponse',
    'EncryptionResponse',
    'EncryptionSetIdentityResponse',
    'EncryptionSettingsCollectionResponse',
    'EncryptionSettingsElementResponse',
    'ImageDiskReferenceResponse',
    'KeyVaultAndKeyReferenceResponse',
    'KeyVaultAndSecretReferenceResponse',
    'ShareInfoElementResponse',
    'SnapshotSkuResponse',
    'SourceVaultResponse',
]

@pulumi.output_type
class CreationDataResponse(dict):
    """
    Data used when creating a disk.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createOption":
            suggest = "create_option"
        elif key == "sourceUniqueId":
            suggest = "source_unique_id"
        elif key == "galleryImageReference":
            suggest = "gallery_image_reference"
        elif key == "imageReference":
            suggest = "image_reference"
        elif key == "sourceResourceId":
            suggest = "source_resource_id"
        elif key == "sourceUri":
            suggest = "source_uri"
        elif key == "storageAccountId":
            suggest = "storage_account_id"
        elif key == "uploadSizeBytes":
            suggest = "upload_size_bytes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CreationDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CreationDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CreationDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 create_option: str,
                 source_unique_id: str,
                 gallery_image_reference: Optional['outputs.ImageDiskReferenceResponse'] = None,
                 image_reference: Optional['outputs.ImageDiskReferenceResponse'] = None,
                 source_resource_id: Optional[str] = None,
                 source_uri: Optional[str] = None,
                 storage_account_id: Optional[str] = None,
                 upload_size_bytes: Optional[float] = None):
        """
        Data used when creating a disk.
        :param str create_option: This enumerates the possible sources of a disk's creation.
        :param str source_unique_id: If this field is set, this is the unique id identifying the source of this resource.
        :param 'ImageDiskReferenceResponse' gallery_image_reference: Required if creating from a Gallery Image. The id of the ImageDiskReference will be the ARM id of the shared galley image version from which to create a disk.
        :param 'ImageDiskReferenceResponse' image_reference: Disk source information.
        :param str source_resource_id: If createOption is Copy, this is the ARM id of the source snapshot or disk.
        :param str source_uri: If createOption is Import, this is the URI of a blob to be imported into a managed disk.
        :param str storage_account_id: Required if createOption is Import. The Azure Resource Manager identifier of the storage account containing the blob to import as a disk.
        :param float upload_size_bytes: If createOption is Upload, this is the size of the contents of the upload including the VHD footer. This value should be between 20972032 (20 MiB + 512 bytes for the VHD footer) and 35183298347520 bytes (32 TiB + 512 bytes for the VHD footer).
        """
        pulumi.set(__self__, "create_option", create_option)
        pulumi.set(__self__, "source_unique_id", source_unique_id)
        if gallery_image_reference is not None:
            pulumi.set(__self__, "gallery_image_reference", gallery_image_reference)
        if image_reference is not None:
            pulumi.set(__self__, "image_reference", image_reference)
        if source_resource_id is not None:
            pulumi.set(__self__, "source_resource_id", source_resource_id)
        if source_uri is not None:
            pulumi.set(__self__, "source_uri", source_uri)
        if storage_account_id is not None:
            pulumi.set(__self__, "storage_account_id", storage_account_id)
        if upload_size_bytes is not None:
            pulumi.set(__self__, "upload_size_bytes", upload_size_bytes)

    @property
    @pulumi.getter(name="createOption")
    def create_option(self) -> str:
        """
        This enumerates the possible sources of a disk's creation.
        """
        return pulumi.get(self, "create_option")

    @property
    @pulumi.getter(name="sourceUniqueId")
    def source_unique_id(self) -> str:
        """
        If this field is set, this is the unique id identifying the source of this resource.
        """
        return pulumi.get(self, "source_unique_id")

    @property
    @pulumi.getter(name="galleryImageReference")
    def gallery_image_reference(self) -> Optional['outputs.ImageDiskReferenceResponse']:
        """
        Required if creating from a Gallery Image. The id of the ImageDiskReference will be the ARM id of the shared galley image version from which to create a disk.
        """
        return pulumi.get(self, "gallery_image_reference")

    @property
    @pulumi.getter(name="imageReference")
    def image_reference(self) -> Optional['outputs.ImageDiskReferenceResponse']:
        """
        Disk source information.
        """
        return pulumi.get(self, "image_reference")

    @property
    @pulumi.getter(name="sourceResourceId")
    def source_resource_id(self) -> Optional[str]:
        """
        If createOption is Copy, this is the ARM id of the source snapshot or disk.
        """
        return pulumi.get(self, "source_resource_id")

    @property
    @pulumi.getter(name="sourceUri")
    def source_uri(self) -> Optional[str]:
        """
        If createOption is Import, this is the URI of a blob to be imported into a managed disk.
        """
        return pulumi.get(self, "source_uri")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[str]:
        """
        Required if createOption is Import. The Azure Resource Manager identifier of the storage account containing the blob to import as a disk.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter(name="uploadSizeBytes")
    def upload_size_bytes(self) -> Optional[float]:
        """
        If createOption is Upload, this is the size of the contents of the upload including the VHD footer. This value should be between 20972032 (20 MiB + 512 bytes for the VHD footer) and 35183298347520 bytes (32 TiB + 512 bytes for the VHD footer).
        """
        return pulumi.get(self, "upload_size_bytes")


@pulumi.output_type
class DiskSkuResponse(dict):
    """
    The disks sku name. Can be Standard_LRS, Premium_LRS, StandardSSD_LRS, or UltraSSD_LRS.
    """
    def __init__(__self__, *,
                 tier: str,
                 name: Optional[str] = None):
        """
        The disks sku name. Can be Standard_LRS, Premium_LRS, StandardSSD_LRS, or UltraSSD_LRS.
        :param str tier: The sku tier.
        :param str name: The sku name.
        """
        pulumi.set(__self__, "tier", tier)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def tier(self) -> str:
        """
        The sku tier.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The sku name.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class EncryptionResponse(dict):
    """
    Encryption at rest settings for disk or snapshot
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "diskEncryptionSetId":
            suggest = "disk_encryption_set_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EncryptionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 disk_encryption_set_id: Optional[str] = None,
                 type: Optional[str] = None):
        """
        Encryption at rest settings for disk or snapshot
        :param str disk_encryption_set_id: ResourceId of the disk encryption set to use for enabling encryption at rest.
        :param str type: The type of key used to encrypt the data of the disk.
        """
        if disk_encryption_set_id is not None:
            pulumi.set(__self__, "disk_encryption_set_id", disk_encryption_set_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> Optional[str]:
        """
        ResourceId of the disk encryption set to use for enabling encryption at rest.
        """
        return pulumi.get(self, "disk_encryption_set_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of key used to encrypt the data of the disk.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class EncryptionSetIdentityResponse(dict):
    """
    The managed identity for the disk encryption set. It should be given permission on the key vault before it can be used to encrypt disks.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionSetIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionSetIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EncryptionSetIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None):
        """
        The managed identity for the disk encryption set. It should be given permission on the key vault before it can be used to encrypt disks.
        :param str principal_id: The object id of the Managed Identity Resource. This will be sent to the RP from ARM via the x-ms-identity-principal-id header in the PUT request if the resource has a systemAssigned(implicit) identity
        :param str tenant_id: The tenant id of the Managed Identity Resource. This will be sent to the RP from ARM via the x-ms-client-tenant-id header in the PUT request if the resource has a systemAssigned(implicit) identity
        :param str type: The type of Managed Identity used by the DiskEncryptionSet. Only SystemAssigned is supported.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The object id of the Managed Identity Resource. This will be sent to the RP from ARM via the x-ms-identity-principal-id header in the PUT request if the resource has a systemAssigned(implicit) identity
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant id of the Managed Identity Resource. This will be sent to the RP from ARM via the x-ms-client-tenant-id header in the PUT request if the resource has a systemAssigned(implicit) identity
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of Managed Identity used by the DiskEncryptionSet. Only SystemAssigned is supported.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class EncryptionSettingsCollectionResponse(dict):
    """
    Encryption settings for disk or snapshot
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "encryptionSettings":
            suggest = "encryption_settings"
        elif key == "encryptionSettingsVersion":
            suggest = "encryption_settings_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionSettingsCollectionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionSettingsCollectionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EncryptionSettingsCollectionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: bool,
                 encryption_settings: Optional[Sequence['outputs.EncryptionSettingsElementResponse']] = None,
                 encryption_settings_version: Optional[str] = None):
        """
        Encryption settings for disk or snapshot
        :param bool enabled: Set this flag to true and provide DiskEncryptionKey and optional KeyEncryptionKey to enable encryption. Set this flag to false and remove DiskEncryptionKey and KeyEncryptionKey to disable encryption. If EncryptionSettings is null in the request object, the existing settings remain unchanged.
        :param Sequence['EncryptionSettingsElementResponse'] encryption_settings: A collection of encryption settings, one for each disk volume.
        :param str encryption_settings_version: Describes what type of encryption is used for the disks. Once this field is set, it cannot be overwritten. '1.0' corresponds to Azure Disk Encryption with AAD app.'1.1' corresponds to Azure Disk Encryption.
        """
        pulumi.set(__self__, "enabled", enabled)
        if encryption_settings is not None:
            pulumi.set(__self__, "encryption_settings", encryption_settings)
        if encryption_settings_version is not None:
            pulumi.set(__self__, "encryption_settings_version", encryption_settings_version)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Set this flag to true and provide DiskEncryptionKey and optional KeyEncryptionKey to enable encryption. Set this flag to false and remove DiskEncryptionKey and KeyEncryptionKey to disable encryption. If EncryptionSettings is null in the request object, the existing settings remain unchanged.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="encryptionSettings")
    def encryption_settings(self) -> Optional[Sequence['outputs.EncryptionSettingsElementResponse']]:
        """
        A collection of encryption settings, one for each disk volume.
        """
        return pulumi.get(self, "encryption_settings")

    @property
    @pulumi.getter(name="encryptionSettingsVersion")
    def encryption_settings_version(self) -> Optional[str]:
        """
        Describes what type of encryption is used for the disks. Once this field is set, it cannot be overwritten. '1.0' corresponds to Azure Disk Encryption with AAD app.'1.1' corresponds to Azure Disk Encryption.
        """
        return pulumi.get(self, "encryption_settings_version")


@pulumi.output_type
class EncryptionSettingsElementResponse(dict):
    """
    Encryption settings for one disk volume.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "diskEncryptionKey":
            suggest = "disk_encryption_key"
        elif key == "keyEncryptionKey":
            suggest = "key_encryption_key"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionSettingsElementResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionSettingsElementResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EncryptionSettingsElementResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 disk_encryption_key: Optional['outputs.KeyVaultAndSecretReferenceResponse'] = None,
                 key_encryption_key: Optional['outputs.KeyVaultAndKeyReferenceResponse'] = None):
        """
        Encryption settings for one disk volume.
        :param 'KeyVaultAndSecretReferenceResponse' disk_encryption_key: Key Vault Secret Url and vault id of the disk encryption key
        :param 'KeyVaultAndKeyReferenceResponse' key_encryption_key: Key Vault Key Url and vault id of the key encryption key. KeyEncryptionKey is optional and when provided is used to unwrap the disk encryption key.
        """
        if disk_encryption_key is not None:
            pulumi.set(__self__, "disk_encryption_key", disk_encryption_key)
        if key_encryption_key is not None:
            pulumi.set(__self__, "key_encryption_key", key_encryption_key)

    @property
    @pulumi.getter(name="diskEncryptionKey")
    def disk_encryption_key(self) -> Optional['outputs.KeyVaultAndSecretReferenceResponse']:
        """
        Key Vault Secret Url and vault id of the disk encryption key
        """
        return pulumi.get(self, "disk_encryption_key")

    @property
    @pulumi.getter(name="keyEncryptionKey")
    def key_encryption_key(self) -> Optional['outputs.KeyVaultAndKeyReferenceResponse']:
        """
        Key Vault Key Url and vault id of the key encryption key. KeyEncryptionKey is optional and when provided is used to unwrap the disk encryption key.
        """
        return pulumi.get(self, "key_encryption_key")


@pulumi.output_type
class ImageDiskReferenceResponse(dict):
    """
    The source image used for creating the disk.
    """
    def __init__(__self__, *,
                 id: str,
                 lun: Optional[int] = None):
        """
        The source image used for creating the disk.
        :param str id: A relative uri containing either a Platform Image Repository or user image reference.
        :param int lun: If the disk is created from an image's data disk, this is an index that indicates which of the data disks in the image to use. For OS disks, this field is null.
        """
        pulumi.set(__self__, "id", id)
        if lun is not None:
            pulumi.set(__self__, "lun", lun)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        A relative uri containing either a Platform Image Repository or user image reference.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def lun(self) -> Optional[int]:
        """
        If the disk is created from an image's data disk, this is an index that indicates which of the data disks in the image to use. For OS disks, this field is null.
        """
        return pulumi.get(self, "lun")


@pulumi.output_type
class KeyVaultAndKeyReferenceResponse(dict):
    """
    Key Vault Key Url and vault id of KeK, KeK is optional and when provided is used to unwrap the encryptionKey
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyUrl":
            suggest = "key_url"
        elif key == "sourceVault":
            suggest = "source_vault"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyVaultAndKeyReferenceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyVaultAndKeyReferenceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyVaultAndKeyReferenceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_url: str,
                 source_vault: 'outputs.SourceVaultResponse'):
        """
        Key Vault Key Url and vault id of KeK, KeK is optional and when provided is used to unwrap the encryptionKey
        :param str key_url: Url pointing to a key or secret in KeyVault
        :param 'SourceVaultResponse' source_vault: Resource id of the KeyVault containing the key or secret
        """
        pulumi.set(__self__, "key_url", key_url)
        pulumi.set(__self__, "source_vault", source_vault)

    @property
    @pulumi.getter(name="keyUrl")
    def key_url(self) -> str:
        """
        Url pointing to a key or secret in KeyVault
        """
        return pulumi.get(self, "key_url")

    @property
    @pulumi.getter(name="sourceVault")
    def source_vault(self) -> 'outputs.SourceVaultResponse':
        """
        Resource id of the KeyVault containing the key or secret
        """
        return pulumi.get(self, "source_vault")


@pulumi.output_type
class KeyVaultAndSecretReferenceResponse(dict):
    """
    Key Vault Secret Url and vault id of the encryption key 
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "secretUrl":
            suggest = "secret_url"
        elif key == "sourceVault":
            suggest = "source_vault"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyVaultAndSecretReferenceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyVaultAndSecretReferenceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyVaultAndSecretReferenceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 secret_url: str,
                 source_vault: 'outputs.SourceVaultResponse'):
        """
        Key Vault Secret Url and vault id of the encryption key 
        :param str secret_url: Url pointing to a key or secret in KeyVault
        :param 'SourceVaultResponse' source_vault: Resource id of the KeyVault containing the key or secret
        """
        pulumi.set(__self__, "secret_url", secret_url)
        pulumi.set(__self__, "source_vault", source_vault)

    @property
    @pulumi.getter(name="secretUrl")
    def secret_url(self) -> str:
        """
        Url pointing to a key or secret in KeyVault
        """
        return pulumi.get(self, "secret_url")

    @property
    @pulumi.getter(name="sourceVault")
    def source_vault(self) -> 'outputs.SourceVaultResponse':
        """
        Resource id of the KeyVault containing the key or secret
        """
        return pulumi.get(self, "source_vault")


@pulumi.output_type
class ShareInfoElementResponse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "vmUri":
            suggest = "vm_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ShareInfoElementResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ShareInfoElementResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ShareInfoElementResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 vm_uri: str):
        """
        :param str vm_uri: A relative URI containing the ID of the VM that has the disk attached.
        """
        pulumi.set(__self__, "vm_uri", vm_uri)

    @property
    @pulumi.getter(name="vmUri")
    def vm_uri(self) -> str:
        """
        A relative URI containing the ID of the VM that has the disk attached.
        """
        return pulumi.get(self, "vm_uri")


@pulumi.output_type
class SnapshotSkuResponse(dict):
    """
    The snapshots sku name. Can be Standard_LRS, Premium_LRS, or Standard_ZRS.
    """
    def __init__(__self__, *,
                 tier: str,
                 name: Optional[str] = None):
        """
        The snapshots sku name. Can be Standard_LRS, Premium_LRS, or Standard_ZRS.
        :param str tier: The sku tier.
        :param str name: The sku name.
        """
        pulumi.set(__self__, "tier", tier)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def tier(self) -> str:
        """
        The sku tier.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The sku name.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class SourceVaultResponse(dict):
    """
    The vault id is an Azure Resource Manager Resource id in the form /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        The vault id is an Azure Resource Manager Resource id in the form /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}
        :param str id: Resource Id
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")


