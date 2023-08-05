# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AddressType',
    'ClassDiscriminator',
    'DataAccountType',
    'DoubleEncryption',
    'FilterFileType',
    'JobDeliveryType',
    'KekType',
    'LogCollectionLevel',
    'NotificationStageName',
    'SkuName',
    'TransferConfigurationType',
    'TransferType',
    'TransportShipmentTypes',
]


class AddressType(str, Enum):
    """
    Type of address.
    """
    NONE = "None"
    """Address type not known."""
    RESIDENTIAL = "Residential"
    """Residential Address."""
    COMMERCIAL = "Commercial"
    """Commercial Address."""


class ClassDiscriminator(str, Enum):
    """
    Indicates the type of job details.
    """
    DATA_BOX = "DataBox"
    """Data Box orders."""
    DATA_BOX_DISK = "DataBoxDisk"
    """Data Box Disk orders."""
    DATA_BOX_HEAVY = "DataBoxHeavy"
    """Data Box Heavy orders."""


class DataAccountType(str, Enum):
    """
    Type of the account of data.
    """
    STORAGE_ACCOUNT = "StorageAccount"
    """Storage Accounts ."""
    MANAGED_DISK = "ManagedDisk"
    """Azure Managed disk storage."""


class DoubleEncryption(str, Enum):
    """
    Defines secondary layer of software-based encryption enablement.
    """
    ENABLED = "Enabled"
    """Software-based encryption is enabled."""
    DISABLED = "Disabled"
    """Software-based encryption is disabled."""


class FilterFileType(str, Enum):
    """
    Type of the filter file.
    """
    AZURE_BLOB = "AzureBlob"
    """Filter file is of the type AzureBlob."""
    AZURE_FILE = "AzureFile"
    """Filter file is of the type AzureFiles."""


class JobDeliveryType(str, Enum):
    """
    Delivery type of Job.
    """
    NON_SCHEDULED = "NonScheduled"
    """Non Scheduled job."""
    SCHEDULED = "Scheduled"
    """Scheduled job."""


class KekType(str, Enum):
    """
    Type of encryption key used for key encryption.
    """
    MICROSOFT_MANAGED = "MicrosoftManaged"
    """Key encryption key is managed by Microsoft."""
    CUSTOMER_MANAGED = "CustomerManaged"
    """Key encryption key is managed by the Customer."""


class LogCollectionLevel(str, Enum):
    """
    Level of the logs to be collected.
    """
    ERROR = "Error"
    """Only Errors will be collected in the logs."""
    VERBOSE = "Verbose"
    """Verbose logging (includes Errors, CRC, size information and others)."""


class NotificationStageName(str, Enum):
    """
    Name of the stage.
    """
    DEVICE_PREPARED = "DevicePrepared"
    """Notification at device prepared stage."""
    DISPATCHED = "Dispatched"
    """Notification at device dispatched stage."""
    DELIVERED = "Delivered"
    """Notification at device delivered stage."""
    PICKED_UP = "PickedUp"
    """Notification at device picked up from user stage."""
    AT_AZURE_DC = "AtAzureDC"
    """Notification at device received at Azure datacenter stage."""
    DATA_COPY = "DataCopy"
    """Notification at data copy started stage."""


class SkuName(str, Enum):
    """
    The sku name.
    """
    DATA_BOX = "DataBox"
    """Data Box."""
    DATA_BOX_DISK = "DataBoxDisk"
    """Data Box Disk."""
    DATA_BOX_HEAVY = "DataBoxHeavy"
    """Data Box Heavy."""


class TransferConfigurationType(str, Enum):
    """
    Type of the configuration for transfer.
    """
    TRANSFER_ALL = "TransferAll"
    """Transfer all the data."""
    TRANSFER_USING_FILTER = "TransferUsingFilter"
    """Transfer using filter."""


class TransferType(str, Enum):
    """
    Type of the data transfer.
    """
    IMPORT_TO_AZURE = "ImportToAzure"
    """Import data to azure."""
    EXPORT_FROM_AZURE = "ExportFromAzure"
    """Export data from azure."""


class TransportShipmentTypes(str, Enum):
    """
    Indicates Shipment Logistics type that the customer preferred.
    """
    CUSTOMER_MANAGED = "CustomerManaged"
    """Shipment Logistics is handled by the customer."""
    MICROSOFT_MANAGED = "MicrosoftManaged"
    """Shipment Logistics is handled by Microsoft."""
