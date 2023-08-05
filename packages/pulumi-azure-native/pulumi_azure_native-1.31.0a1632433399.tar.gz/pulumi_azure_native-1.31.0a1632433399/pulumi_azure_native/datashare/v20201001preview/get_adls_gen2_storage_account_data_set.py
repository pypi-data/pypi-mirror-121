# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetADLSGen2StorageAccountDataSetResult',
    'AwaitableGetADLSGen2StorageAccountDataSetResult',
    'get_adls_gen2_storage_account_data_set',
]

@pulumi.output_type
class GetADLSGen2StorageAccountDataSetResult:
    """
    An ADLSGen2 storage account data set.
    """
    def __init__(__self__, data_set_id=None, id=None, kind=None, location=None, name=None, paths=None, storage_account_resource_id=None, system_data=None, type=None):
        if data_set_id and not isinstance(data_set_id, str):
            raise TypeError("Expected argument 'data_set_id' to be a str")
        pulumi.set(__self__, "data_set_id", data_set_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if paths and not isinstance(paths, list):
            raise TypeError("Expected argument 'paths' to be a list")
        pulumi.set(__self__, "paths", paths)
        if storage_account_resource_id and not isinstance(storage_account_resource_id, str):
            raise TypeError("Expected argument 'storage_account_resource_id' to be a str")
        pulumi.set(__self__, "storage_account_resource_id", storage_account_resource_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dataSetId")
    def data_set_id(self) -> str:
        """
        Unique id for identifying a data set resource
        """
        return pulumi.get(self, "data_set_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource id of the azure resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Kind of data set.
        Expected value is 'AdlsGen2StorageAccount'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Location of the ADLSGen2 storage account.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the azure resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def paths(self) -> Sequence['outputs.ADLSGen2StorageAccountPathResponse']:
        """
        A list of ADLSGen2 storage account paths.
        """
        return pulumi.get(self, "paths")

    @property
    @pulumi.getter(name="storageAccountResourceId")
    def storage_account_resource_id(self) -> str:
        """
        Resource id of the ADLSGen2 storage account.
        """
        return pulumi.get(self, "storage_account_resource_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        System Data of the Azure resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the azure resource
        """
        return pulumi.get(self, "type")


class AwaitableGetADLSGen2StorageAccountDataSetResult(GetADLSGen2StorageAccountDataSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetADLSGen2StorageAccountDataSetResult(
            data_set_id=self.data_set_id,
            id=self.id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            paths=self.paths,
            storage_account_resource_id=self.storage_account_resource_id,
            system_data=self.system_data,
            type=self.type)


def get_adls_gen2_storage_account_data_set(account_name: Optional[str] = None,
                                           data_set_name: Optional[str] = None,
                                           resource_group_name: Optional[str] = None,
                                           share_name: Optional[str] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetADLSGen2StorageAccountDataSetResult:
    """
    An ADLSGen2 storage account data set.


    :param str account_name: The name of the share account.
    :param str data_set_name: The name of the dataSet.
    :param str resource_group_name: The resource group name.
    :param str share_name: The name of the share.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['dataSetName'] = data_set_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['shareName'] = share_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:datashare/v20201001preview:getADLSGen2StorageAccountDataSet', __args__, opts=opts, typ=GetADLSGen2StorageAccountDataSetResult).value

    return AwaitableGetADLSGen2StorageAccountDataSetResult(
        data_set_id=__ret__.data_set_id,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        paths=__ret__.paths,
        storage_account_resource_id=__ret__.storage_account_resource_id,
        system_data=__ret__.system_data,
        type=__ret__.type)
