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
    'ListDatabaseAccountConnectionStringsResult',
    'AwaitableListDatabaseAccountConnectionStringsResult',
    'list_database_account_connection_strings',
]

@pulumi.output_type
class ListDatabaseAccountConnectionStringsResult:
    """
    The connection strings for the given database account.
    """
    def __init__(__self__, connection_strings=None):
        if connection_strings and not isinstance(connection_strings, list):
            raise TypeError("Expected argument 'connection_strings' to be a list")
        pulumi.set(__self__, "connection_strings", connection_strings)

    @property
    @pulumi.getter(name="connectionStrings")
    def connection_strings(self) -> Optional[Sequence['outputs.DatabaseAccountConnectionStringResponse']]:
        """
        An array that contains the connection strings for the Cosmos DB account.
        """
        return pulumi.get(self, "connection_strings")


class AwaitableListDatabaseAccountConnectionStringsResult(ListDatabaseAccountConnectionStringsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListDatabaseAccountConnectionStringsResult(
            connection_strings=self.connection_strings)


def list_database_account_connection_strings(account_name: Optional[str] = None,
                                             resource_group_name: Optional[str] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListDatabaseAccountConnectionStringsResult:
    """
    The connection strings for the given database account.


    :param str account_name: Cosmos DB database account name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:documentdb/v20210701preview:listDatabaseAccountConnectionStrings', __args__, opts=opts, typ=ListDatabaseAccountConnectionStringsResult).value

    return AwaitableListDatabaseAccountConnectionStringsResult(
        connection_strings=__ret__.connection_strings)
