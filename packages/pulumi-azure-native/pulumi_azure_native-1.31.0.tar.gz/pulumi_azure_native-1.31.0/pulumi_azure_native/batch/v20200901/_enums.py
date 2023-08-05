# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AutoUserScope',
    'CachingType',
    'CertificateFormat',
    'CertificateStoreLocation',
    'CertificateVisibility',
    'ComputeNodeDeallocationOption',
    'ComputeNodeFillType',
    'ContainerType',
    'ContainerWorkingDirectory',
    'DiskEncryptionTarget',
    'ElevationLevel',
    'IPAddressProvisioningType',
    'InboundEndpointProtocol',
    'InterNodeCommunicationState',
    'KeySource',
    'LoginMode',
    'NetworkSecurityGroupRuleAccess',
    'PoolAllocationMode',
    'PublicNetworkAccessType',
    'ResourceIdentityType',
    'StorageAccountType',
]


class AutoUserScope(str, Enum):
    """
    The default value is Pool. If the pool is running Windows a value of Task should be specified if stricter isolation between tasks is required. For example, if the task mutates the registry in a way which could impact other tasks, or if certificates have been specified on the pool which should not be accessible by normal tasks but should be accessible by start tasks.
    """
    TASK = "Task"
    """Specifies that the service should create a new user for the task."""
    POOL = "Pool"
    """Specifies that the task runs as the common auto user account which is created on every node in a pool."""


class CachingType(str, Enum):
    """
    Values are:

     none - The caching mode for the disk is not enabled.
     readOnly - The caching mode for the disk is read only.
     readWrite - The caching mode for the disk is read and write.

     The default value for caching is none. For information about the caching options see: https://blogs.msdn.microsoft.com/windowsazurestorage/2012/06/27/exploring-windows-azure-drives-disks-and-images/.
    """
    NONE = "None"
    """The caching mode for the disk is not enabled."""
    READ_ONLY = "ReadOnly"
    """The caching mode for the disk is read only."""
    READ_WRITE = "ReadWrite"
    """The caching mode for the disk is read and write."""


class CertificateFormat(str, Enum):
    """
    The format of the certificate - either Pfx or Cer. If omitted, the default is Pfx.
    """
    PFX = "Pfx"
    """The certificate is a PFX (PKCS#12) formatted certificate or certificate chain."""
    CER = "Cer"
    """The certificate is a base64-encoded X.509 certificate."""


class CertificateStoreLocation(str, Enum):
    """
    The default value is currentUser. This property is applicable only for pools configured with Windows nodes (that is, created with cloudServiceConfiguration, or with virtualMachineConfiguration using a Windows image reference). For Linux compute nodes, the certificates are stored in a directory inside the task working directory and an environment variable AZ_BATCH_CERTIFICATES_DIR is supplied to the task to query for this location. For certificates with visibility of 'remoteUser', a 'certs' directory is created in the user's home directory (e.g., /home/{user-name}/certs) and certificates are placed in that directory.
    """
    CURRENT_USER = "CurrentUser"
    """Certificates should be installed to the CurrentUser certificate store."""
    LOCAL_MACHINE = "LocalMachine"
    """Certificates should be installed to the LocalMachine certificate store."""


class CertificateVisibility(str, Enum):
    START_TASK = "StartTask"
    """The certificate should be visible to the user account under which the start task is run. Note that if AutoUser Scope is Pool for both the StartTask and a Task, this certificate will be visible to the Task as well."""
    TASK = "Task"
    """The certificate should be visible to the user accounts under which job tasks are run."""
    REMOTE_USER = "RemoteUser"
    """The certificate should be visible to the user accounts under which users remotely access the node."""


class ComputeNodeDeallocationOption(str, Enum):
    """
    If omitted, the default value is Requeue.
    """
    REQUEUE = "Requeue"
    """Terminate running task processes and requeue the tasks. The tasks will run again when a node is available. Remove nodes as soon as tasks have been terminated."""
    TERMINATE = "Terminate"
    """Terminate running tasks. The tasks will be completed with failureInfo indicating that they were terminated, and will not run again. Remove nodes as soon as tasks have been terminated."""
    TASK_COMPLETION = "TaskCompletion"
    """Allow currently running tasks to complete. Schedule no new tasks while waiting. Remove nodes when all tasks have completed."""
    RETAINED_DATA = "RetainedData"
    """Allow currently running tasks to complete, then wait for all task data retention periods to expire. Schedule no new tasks while waiting. Remove nodes when all task retention periods have expired."""


class ComputeNodeFillType(str, Enum):
    SPREAD = "Spread"
    """Tasks should be assigned evenly across all nodes in the pool."""
    PACK = "Pack"
    """As many tasks as possible (taskSlotsPerNode) should be assigned to each node in the pool before any tasks are assigned to the next node in the pool."""


class ContainerType(str, Enum):
    DOCKER_COMPATIBLE = "DockerCompatible"
    """A Docker compatible container technology will be used to launch the containers."""


class ContainerWorkingDirectory(str, Enum):
    TASK_WORKING_DIRECTORY = "TaskWorkingDirectory"
    """Use the standard Batch service task working directory, which will contain the Task resource files populated by Batch."""
    CONTAINER_IMAGE_DEFAULT = "ContainerImageDefault"
    """Using container image defined working directory. Beware that this directory will not contain the resource files downloaded by Batch."""


class DiskEncryptionTarget(str, Enum):
    """
    If omitted, no disks on the compute nodes in the pool will be encrypted.
    """
    OS_DISK = "OsDisk"
    """The OS Disk on the compute node is encrypted."""
    TEMPORARY_DISK = "TemporaryDisk"
    """The temporary disk on the compute node is encrypted. On Linux this encryption applies to other partitions (such as those on mounted data disks) when encryption occurs at boot time."""


class ElevationLevel(str, Enum):
    """
    nonAdmin - The auto user is a standard user without elevated access. admin - The auto user is a user with elevated access and operates with full Administrator permissions. The default value is nonAdmin.
    """
    NON_ADMIN = "NonAdmin"
    """The user is a standard user without elevated access."""
    ADMIN = "Admin"
    """The user is a user with elevated access and operates with full Administrator permissions."""


class IPAddressProvisioningType(str, Enum):
    """
    The default value is BatchManaged
    """
    BATCH_MANAGED = "BatchManaged"
    """A public IP will be created and managed by Batch. There may be multiple public IPs depending on the size of the Pool."""
    USER_MANAGED = "UserManaged"
    """Public IPs are provided by the user and will be used to provision the Compute Nodes."""
    NO_PUBLIC_IP_ADDRESSES = "NoPublicIPAddresses"
    """No public IP Address will be created for the Compute Nodes in the Pool."""


class InboundEndpointProtocol(str, Enum):
    TCP = "TCP"
    """Use TCP for the endpoint."""
    UDP = "UDP"
    """Use UDP for the endpoint."""


class InterNodeCommunicationState(str, Enum):
    """
    This imposes restrictions on which nodes can be assigned to the pool. Enabling this value can reduce the chance of the requested number of nodes to be allocated in the pool. If not specified, this value defaults to 'Disabled'.
    """
    ENABLED = "Enabled"
    """Enable network communication between virtual machines."""
    DISABLED = "Disabled"
    """Disable network communication between virtual machines."""


class KeySource(str, Enum):
    """
    Type of the key source.
    """
    MICROSOFT_BATCH = "Microsoft.Batch"
    """Batch creates and manages the encryption keys used to protect the account data."""
    MICROSOFT_KEY_VAULT = "Microsoft.KeyVault"
    """The encryption keys used to protect the account data are stored in an external key vault. If this is set then the Batch Account identity must be set to `SystemAssigned` and a valid Key Identifier must also be supplied under the keyVaultProperties."""


class LoginMode(str, Enum):
    """
    Specifies login mode for the user. The default value for VirtualMachineConfiguration pools is interactive mode and for CloudServiceConfiguration pools is batch mode.
    """
    BATCH = "Batch"
    """The LOGON32_LOGON_BATCH Win32 login mode. The batch login mode is recommended for long running parallel processes."""
    INTERACTIVE = "Interactive"
    """The LOGON32_LOGON_INTERACTIVE Win32 login mode. Some applications require having permissions associated with the interactive login mode. If this is the case for an application used in your task, then this option is recommended."""


class NetworkSecurityGroupRuleAccess(str, Enum):
    ALLOW = "Allow"
    """Allow access."""
    DENY = "Deny"
    """Deny access."""


class PoolAllocationMode(str, Enum):
    """
    The pool allocation mode also affects how clients may authenticate to the Batch Service API. If the mode is BatchService, clients may authenticate using access keys or Azure Active Directory. If the mode is UserSubscription, clients must use Azure Active Directory. The default is BatchService.
    """
    BATCH_SERVICE = "BatchService"
    """Pools will be allocated in subscriptions owned by the Batch service."""
    USER_SUBSCRIPTION = "UserSubscription"
    """Pools will be allocated in a subscription owned by the user."""


class PublicNetworkAccessType(str, Enum):
    """
    If not specified, the default value is 'enabled'.
    """
    ENABLED = "Enabled"
    """Enables connectivity to Azure Batch through public DNS."""
    DISABLED = "Disabled"
    """Disables public connectivity and enables private connectivity to Azure Batch Service through private endpoint resource."""


class ResourceIdentityType(str, Enum):
    """
    The type of identity used for the Batch account.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    """Batch account has a system assigned identity with it."""
    NONE = "None"
    """Batch account has no identity associated with it. Setting `None` in update account will remove existing identities."""


class StorageAccountType(str, Enum):
    """
    If omitted, the default is "Standard_LRS". Values are:

     Standard_LRS - The data disk should use standard locally redundant storage.
     Premium_LRS - The data disk should use premium locally redundant storage.
    """
    STANDARD_LRS = "Standard_LRS"
    """The data disk should use standard locally redundant storage."""
    PREMIUM_LRS = "Premium_LRS"
    """The data disk should use premium locally redundant storage."""
