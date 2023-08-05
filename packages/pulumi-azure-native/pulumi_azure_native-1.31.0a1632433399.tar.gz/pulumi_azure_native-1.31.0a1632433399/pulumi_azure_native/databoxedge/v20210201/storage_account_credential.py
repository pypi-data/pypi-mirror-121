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
from ._inputs import *

__all__ = ['StorageAccountCredentialArgs', 'StorageAccountCredential']

@pulumi.input_type
class StorageAccountCredentialArgs:
    def __init__(__self__, *,
                 account_type: pulumi.Input[Union[str, 'AccountType']],
                 alias: pulumi.Input[str],
                 device_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 ssl_status: pulumi.Input[Union[str, 'SSLStatus']],
                 account_key: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']] = None,
                 blob_domain_name: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a StorageAccountCredential resource.
        :param pulumi.Input[Union[str, 'AccountType']] account_type: Type of storage accessed on the storage account.
        :param pulumi.Input[str] alias: Alias for the storage account.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'SSLStatus']] ssl_status: Signifies whether SSL needs to be enabled or not.
        :param pulumi.Input['AsymmetricEncryptedSecretArgs'] account_key: Encrypted storage key.
        :param pulumi.Input[str] blob_domain_name: Blob end point for private clouds.
        :param pulumi.Input[str] connection_string: Connection string for the storage account. Use this string if username and account key are not specified.
        :param pulumi.Input[str] name: The storage account credential name.
        :param pulumi.Input[str] storage_account_id: Id of the storage account.
        :param pulumi.Input[str] user_name: Username for the storage account.
        """
        pulumi.set(__self__, "account_type", account_type)
        pulumi.set(__self__, "alias", alias)
        pulumi.set(__self__, "device_name", device_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "ssl_status", ssl_status)
        if account_key is not None:
            pulumi.set(__self__, "account_key", account_key)
        if blob_domain_name is not None:
            pulumi.set(__self__, "blob_domain_name", blob_domain_name)
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if storage_account_id is not None:
            pulumi.set(__self__, "storage_account_id", storage_account_id)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> pulumi.Input[Union[str, 'AccountType']]:
        """
        Type of storage accessed on the storage account.
        """
        return pulumi.get(self, "account_type")

    @account_type.setter
    def account_type(self, value: pulumi.Input[Union[str, 'AccountType']]):
        pulumi.set(self, "account_type", value)

    @property
    @pulumi.getter
    def alias(self) -> pulumi.Input[str]:
        """
        Alias for the storage account.
        """
        return pulumi.get(self, "alias")

    @alias.setter
    def alias(self, value: pulumi.Input[str]):
        pulumi.set(self, "alias", value)

    @property
    @pulumi.getter(name="deviceName")
    def device_name(self) -> pulumi.Input[str]:
        """
        The device name.
        """
        return pulumi.get(self, "device_name")

    @device_name.setter
    def device_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="sslStatus")
    def ssl_status(self) -> pulumi.Input[Union[str, 'SSLStatus']]:
        """
        Signifies whether SSL needs to be enabled or not.
        """
        return pulumi.get(self, "ssl_status")

    @ssl_status.setter
    def ssl_status(self, value: pulumi.Input[Union[str, 'SSLStatus']]):
        pulumi.set(self, "ssl_status", value)

    @property
    @pulumi.getter(name="accountKey")
    def account_key(self) -> Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]:
        """
        Encrypted storage key.
        """
        return pulumi.get(self, "account_key")

    @account_key.setter
    def account_key(self, value: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]):
        pulumi.set(self, "account_key", value)

    @property
    @pulumi.getter(name="blobDomainName")
    def blob_domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Blob end point for private clouds.
        """
        return pulumi.get(self, "blob_domain_name")

    @blob_domain_name.setter
    def blob_domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "blob_domain_name", value)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        Connection string for the storage account. Use this string if username and account key are not specified.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_string", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The storage account credential name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of the storage account.
        """
        return pulumi.get(self, "storage_account_id")

    @storage_account_id.setter
    def storage_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_id", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        Username for the storage account.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


class StorageAccountCredential(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_key: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]] = None,
                 account_type: Optional[pulumi.Input[Union[str, 'AccountType']]] = None,
                 alias: Optional[pulumi.Input[str]] = None,
                 blob_domain_name: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 ssl_status: Optional[pulumi.Input[Union[str, 'SSLStatus']]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The storage account credential.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']] account_key: Encrypted storage key.
        :param pulumi.Input[Union[str, 'AccountType']] account_type: Type of storage accessed on the storage account.
        :param pulumi.Input[str] alias: Alias for the storage account.
        :param pulumi.Input[str] blob_domain_name: Blob end point for private clouds.
        :param pulumi.Input[str] connection_string: Connection string for the storage account. Use this string if username and account key are not specified.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] name: The storage account credential name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'SSLStatus']] ssl_status: Signifies whether SSL needs to be enabled or not.
        :param pulumi.Input[str] storage_account_id: Id of the storage account.
        :param pulumi.Input[str] user_name: Username for the storage account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StorageAccountCredentialArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The storage account credential.

        :param str resource_name: The name of the resource.
        :param StorageAccountCredentialArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StorageAccountCredentialArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_key: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]] = None,
                 account_type: Optional[pulumi.Input[Union[str, 'AccountType']]] = None,
                 alias: Optional[pulumi.Input[str]] = None,
                 blob_domain_name: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 ssl_status: Optional[pulumi.Input[Union[str, 'SSLStatus']]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = StorageAccountCredentialArgs.__new__(StorageAccountCredentialArgs)

            __props__.__dict__["account_key"] = account_key
            if account_type is None and not opts.urn:
                raise TypeError("Missing required property 'account_type'")
            __props__.__dict__["account_type"] = account_type
            if alias is None and not opts.urn:
                raise TypeError("Missing required property 'alias'")
            __props__.__dict__["alias"] = alias
            __props__.__dict__["blob_domain_name"] = blob_domain_name
            __props__.__dict__["connection_string"] = connection_string
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__["device_name"] = device_name
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if ssl_status is None and not opts.urn:
                raise TypeError("Missing required property 'ssl_status'")
            __props__.__dict__["ssl_status"] = ssl_status
            __props__.__dict__["storage_account_id"] = storage_account_id
            __props__.__dict__["user_name"] = user_name
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:databoxedge/v20210201:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20190301:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190301:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20190701:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190701:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20190801:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190801:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20200501preview:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200501preview:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20200901:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20200901preview:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901preview:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20201201:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20201201:StorageAccountCredential"), pulumi.Alias(type_="azure-native:databoxedge/v20210201preview:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20210201preview:StorageAccountCredential")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StorageAccountCredential, __self__).__init__(
            'azure-native:databoxedge/v20210201:StorageAccountCredential',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageAccountCredential':
        """
        Get an existing StorageAccountCredential resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StorageAccountCredentialArgs.__new__(StorageAccountCredentialArgs)

        __props__.__dict__["account_key"] = None
        __props__.__dict__["account_type"] = None
        __props__.__dict__["alias"] = None
        __props__.__dict__["blob_domain_name"] = None
        __props__.__dict__["connection_string"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["ssl_status"] = None
        __props__.__dict__["storage_account_id"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["user_name"] = None
        return StorageAccountCredential(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountKey")
    def account_key(self) -> pulumi.Output[Optional['outputs.AsymmetricEncryptedSecretResponse']]:
        """
        Encrypted storage key.
        """
        return pulumi.get(self, "account_key")

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> pulumi.Output[str]:
        """
        Type of storage accessed on the storage account.
        """
        return pulumi.get(self, "account_type")

    @property
    @pulumi.getter
    def alias(self) -> pulumi.Output[str]:
        """
        Alias for the storage account.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="blobDomainName")
    def blob_domain_name(self) -> pulumi.Output[Optional[str]]:
        """
        Blob end point for private clouds.
        """
        return pulumi.get(self, "blob_domain_name")

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> pulumi.Output[Optional[str]]:
        """
        Connection string for the storage account. Use this string if username and account key are not specified.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sslStatus")
    def ssl_status(self) -> pulumi.Output[str]:
        """
        Signifies whether SSL needs to be enabled or not.
        """
        return pulumi.get(self, "ssl_status")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> pulumi.Output[Optional[str]]:
        """
        Id of the storage account.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        StorageAccountCredential object
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[Optional[str]]:
        """
        Username for the storage account.
        """
        return pulumi.get(self, "user_name")

