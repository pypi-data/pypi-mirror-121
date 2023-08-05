# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = ['ServerEndpointArgs', 'ServerEndpoint']

@pulumi.input_type
class ServerEndpointArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 storage_sync_service_name: pulumi.Input[str],
                 sync_group_name: pulumi.Input[str],
                 cloud_tiering: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 offline_data_transfer: Optional[pulumi.Input[str]] = None,
                 offline_data_transfer_share_name: Optional[pulumi.Input[str]] = None,
                 server_endpoint_name: Optional[pulumi.Input[str]] = None,
                 server_local_path: Optional[pulumi.Input[str]] = None,
                 server_resource_id: Optional[pulumi.Input[str]] = None,
                 tier_files_older_than_days: Optional[pulumi.Input[int]] = None,
                 volume_free_space_percent: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a ServerEndpoint resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] storage_sync_service_name: Name of Storage Sync Service resource.
        :param pulumi.Input[str] sync_group_name: Name of Sync Group resource.
        :param pulumi.Input[str] cloud_tiering: Cloud Tiering.
        :param pulumi.Input[str] friendly_name: Friendly Name
        :param pulumi.Input[str] offline_data_transfer: Offline data transfer
        :param pulumi.Input[str] offline_data_transfer_share_name: Offline data transfer share name
        :param pulumi.Input[str] server_endpoint_name: Name of Server Endpoint object.
        :param pulumi.Input[str] server_local_path: Server Local path.
        :param pulumi.Input[str] server_resource_id: Server Resource Id.
        :param pulumi.Input[int] tier_files_older_than_days: Tier files older than days.
        :param pulumi.Input[int] volume_free_space_percent: Level of free space to be maintained by Cloud Tiering if it is enabled.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "storage_sync_service_name", storage_sync_service_name)
        pulumi.set(__self__, "sync_group_name", sync_group_name)
        if cloud_tiering is not None:
            pulumi.set(__self__, "cloud_tiering", cloud_tiering)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if offline_data_transfer is not None:
            pulumi.set(__self__, "offline_data_transfer", offline_data_transfer)
        if offline_data_transfer_share_name is not None:
            pulumi.set(__self__, "offline_data_transfer_share_name", offline_data_transfer_share_name)
        if server_endpoint_name is not None:
            pulumi.set(__self__, "server_endpoint_name", server_endpoint_name)
        if server_local_path is not None:
            pulumi.set(__self__, "server_local_path", server_local_path)
        if server_resource_id is not None:
            pulumi.set(__self__, "server_resource_id", server_resource_id)
        if tier_files_older_than_days is not None:
            pulumi.set(__self__, "tier_files_older_than_days", tier_files_older_than_days)
        if volume_free_space_percent is not None:
            pulumi.set(__self__, "volume_free_space_percent", volume_free_space_percent)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="storageSyncServiceName")
    def storage_sync_service_name(self) -> pulumi.Input[str]:
        """
        Name of Storage Sync Service resource.
        """
        return pulumi.get(self, "storage_sync_service_name")

    @storage_sync_service_name.setter
    def storage_sync_service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_sync_service_name", value)

    @property
    @pulumi.getter(name="syncGroupName")
    def sync_group_name(self) -> pulumi.Input[str]:
        """
        Name of Sync Group resource.
        """
        return pulumi.get(self, "sync_group_name")

    @sync_group_name.setter
    def sync_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "sync_group_name", value)

    @property
    @pulumi.getter(name="cloudTiering")
    def cloud_tiering(self) -> Optional[pulumi.Input[str]]:
        """
        Cloud Tiering.
        """
        return pulumi.get(self, "cloud_tiering")

    @cloud_tiering.setter
    def cloud_tiering(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_tiering", value)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Friendly Name
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter(name="offlineDataTransfer")
    def offline_data_transfer(self) -> Optional[pulumi.Input[str]]:
        """
        Offline data transfer
        """
        return pulumi.get(self, "offline_data_transfer")

    @offline_data_transfer.setter
    def offline_data_transfer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "offline_data_transfer", value)

    @property
    @pulumi.getter(name="offlineDataTransferShareName")
    def offline_data_transfer_share_name(self) -> Optional[pulumi.Input[str]]:
        """
        Offline data transfer share name
        """
        return pulumi.get(self, "offline_data_transfer_share_name")

    @offline_data_transfer_share_name.setter
    def offline_data_transfer_share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "offline_data_transfer_share_name", value)

    @property
    @pulumi.getter(name="serverEndpointName")
    def server_endpoint_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of Server Endpoint object.
        """
        return pulumi.get(self, "server_endpoint_name")

    @server_endpoint_name.setter
    def server_endpoint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_endpoint_name", value)

    @property
    @pulumi.getter(name="serverLocalPath")
    def server_local_path(self) -> Optional[pulumi.Input[str]]:
        """
        Server Local path.
        """
        return pulumi.get(self, "server_local_path")

    @server_local_path.setter
    def server_local_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_local_path", value)

    @property
    @pulumi.getter(name="serverResourceId")
    def server_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Server Resource Id.
        """
        return pulumi.get(self, "server_resource_id")

    @server_resource_id.setter
    def server_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_resource_id", value)

    @property
    @pulumi.getter(name="tierFilesOlderThanDays")
    def tier_files_older_than_days(self) -> Optional[pulumi.Input[int]]:
        """
        Tier files older than days.
        """
        return pulumi.get(self, "tier_files_older_than_days")

    @tier_files_older_than_days.setter
    def tier_files_older_than_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "tier_files_older_than_days", value)

    @property
    @pulumi.getter(name="volumeFreeSpacePercent")
    def volume_free_space_percent(self) -> Optional[pulumi.Input[int]]:
        """
        Level of free space to be maintained by Cloud Tiering if it is enabled.
        """
        return pulumi.get(self, "volume_free_space_percent")

    @volume_free_space_percent.setter
    def volume_free_space_percent(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "volume_free_space_percent", value)


class ServerEndpoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_tiering: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 offline_data_transfer: Optional[pulumi.Input[str]] = None,
                 offline_data_transfer_share_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_endpoint_name: Optional[pulumi.Input[str]] = None,
                 server_local_path: Optional[pulumi.Input[str]] = None,
                 server_resource_id: Optional[pulumi.Input[str]] = None,
                 storage_sync_service_name: Optional[pulumi.Input[str]] = None,
                 sync_group_name: Optional[pulumi.Input[str]] = None,
                 tier_files_older_than_days: Optional[pulumi.Input[int]] = None,
                 volume_free_space_percent: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Server Endpoint object.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cloud_tiering: Cloud Tiering.
        :param pulumi.Input[str] friendly_name: Friendly Name
        :param pulumi.Input[str] offline_data_transfer: Offline data transfer
        :param pulumi.Input[str] offline_data_transfer_share_name: Offline data transfer share name
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] server_endpoint_name: Name of Server Endpoint object.
        :param pulumi.Input[str] server_local_path: Server Local path.
        :param pulumi.Input[str] server_resource_id: Server Resource Id.
        :param pulumi.Input[str] storage_sync_service_name: Name of Storage Sync Service resource.
        :param pulumi.Input[str] sync_group_name: Name of Sync Group resource.
        :param pulumi.Input[int] tier_files_older_than_days: Tier files older than days.
        :param pulumi.Input[int] volume_free_space_percent: Level of free space to be maintained by Cloud Tiering if it is enabled.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServerEndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Server Endpoint object.

        :param str resource_name: The name of the resource.
        :param ServerEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServerEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_tiering: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 offline_data_transfer: Optional[pulumi.Input[str]] = None,
                 offline_data_transfer_share_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_endpoint_name: Optional[pulumi.Input[str]] = None,
                 server_local_path: Optional[pulumi.Input[str]] = None,
                 server_resource_id: Optional[pulumi.Input[str]] = None,
                 storage_sync_service_name: Optional[pulumi.Input[str]] = None,
                 sync_group_name: Optional[pulumi.Input[str]] = None,
                 tier_files_older_than_days: Optional[pulumi.Input[int]] = None,
                 volume_free_space_percent: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServerEndpointArgs.__new__(ServerEndpointArgs)

            __props__.__dict__["cloud_tiering"] = cloud_tiering
            __props__.__dict__["friendly_name"] = friendly_name
            __props__.__dict__["offline_data_transfer"] = offline_data_transfer
            __props__.__dict__["offline_data_transfer_share_name"] = offline_data_transfer_share_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["server_endpoint_name"] = server_endpoint_name
            __props__.__dict__["server_local_path"] = server_local_path
            __props__.__dict__["server_resource_id"] = server_resource_id
            if storage_sync_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_sync_service_name'")
            __props__.__dict__["storage_sync_service_name"] = storage_sync_service_name
            if sync_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'sync_group_name'")
            __props__.__dict__["sync_group_name"] = sync_group_name
            __props__.__dict__["tier_files_older_than_days"] = tier_files_older_than_days
            __props__.__dict__["volume_free_space_percent"] = volume_free_space_percent
            __props__.__dict__["last_operation_name"] = None
            __props__.__dict__["last_workflow_id"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["offline_data_transfer_storage_account_resource_id"] = None
            __props__.__dict__["offline_data_transfer_storage_account_tenant_id"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["sync_status"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storagesync/v20181001:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20170605preview:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20170605preview:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20180402:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20180402:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20180701:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20180701:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20190201:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190201:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20190301:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190301:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20190601:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190601:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20191001:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20191001:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20200301:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20200301:ServerEndpoint"), pulumi.Alias(type_="azure-native:storagesync/v20200901:ServerEndpoint"), pulumi.Alias(type_="azure-nextgen:storagesync/v20200901:ServerEndpoint")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ServerEndpoint, __self__).__init__(
            'azure-native:storagesync/v20181001:ServerEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ServerEndpoint':
        """
        Get an existing ServerEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ServerEndpointArgs.__new__(ServerEndpointArgs)

        __props__.__dict__["cloud_tiering"] = None
        __props__.__dict__["friendly_name"] = None
        __props__.__dict__["last_operation_name"] = None
        __props__.__dict__["last_workflow_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["offline_data_transfer"] = None
        __props__.__dict__["offline_data_transfer_share_name"] = None
        __props__.__dict__["offline_data_transfer_storage_account_resource_id"] = None
        __props__.__dict__["offline_data_transfer_storage_account_tenant_id"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["server_local_path"] = None
        __props__.__dict__["server_resource_id"] = None
        __props__.__dict__["sync_status"] = None
        __props__.__dict__["tier_files_older_than_days"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["volume_free_space_percent"] = None
        return ServerEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cloudTiering")
    def cloud_tiering(self) -> pulumi.Output[Optional[str]]:
        """
        Cloud Tiering.
        """
        return pulumi.get(self, "cloud_tiering")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        Friendly Name
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="lastOperationName")
    def last_operation_name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Last Operation Name
        """
        return pulumi.get(self, "last_operation_name")

    @property
    @pulumi.getter(name="lastWorkflowId")
    def last_workflow_id(self) -> pulumi.Output[Optional[str]]:
        """
        ServerEndpoint lastWorkflowId
        """
        return pulumi.get(self, "last_workflow_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="offlineDataTransfer")
    def offline_data_transfer(self) -> pulumi.Output[Optional[str]]:
        """
        Offline data transfer
        """
        return pulumi.get(self, "offline_data_transfer")

    @property
    @pulumi.getter(name="offlineDataTransferShareName")
    def offline_data_transfer_share_name(self) -> pulumi.Output[Optional[str]]:
        """
        Offline data transfer share name
        """
        return pulumi.get(self, "offline_data_transfer_share_name")

    @property
    @pulumi.getter(name="offlineDataTransferStorageAccountResourceId")
    def offline_data_transfer_storage_account_resource_id(self) -> pulumi.Output[str]:
        """
        Offline data transfer storage account resource ID
        """
        return pulumi.get(self, "offline_data_transfer_storage_account_resource_id")

    @property
    @pulumi.getter(name="offlineDataTransferStorageAccountTenantId")
    def offline_data_transfer_storage_account_tenant_id(self) -> pulumi.Output[str]:
        """
        Offline data transfer storage account tenant ID
        """
        return pulumi.get(self, "offline_data_transfer_storage_account_tenant_id")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        ServerEndpoint Provisioning State
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serverLocalPath")
    def server_local_path(self) -> pulumi.Output[Optional[str]]:
        """
        Server Local path.
        """
        return pulumi.get(self, "server_local_path")

    @property
    @pulumi.getter(name="serverResourceId")
    def server_resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        Server Resource Id.
        """
        return pulumi.get(self, "server_resource_id")

    @property
    @pulumi.getter(name="syncStatus")
    def sync_status(self) -> pulumi.Output[Optional['outputs.ServerEndpointHealthResponse']]:
        """
        Server Endpoint properties.
        """
        return pulumi.get(self, "sync_status")

    @property
    @pulumi.getter(name="tierFilesOlderThanDays")
    def tier_files_older_than_days(self) -> pulumi.Output[Optional[int]]:
        """
        Tier files older than days.
        """
        return pulumi.get(self, "tier_files_older_than_days")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="volumeFreeSpacePercent")
    def volume_free_space_percent(self) -> pulumi.Output[Optional[int]]:
        """
        Level of free space to be maintained by Cloud Tiering if it is enabled.
        """
        return pulumi.get(self, "volume_free_space_percent")

