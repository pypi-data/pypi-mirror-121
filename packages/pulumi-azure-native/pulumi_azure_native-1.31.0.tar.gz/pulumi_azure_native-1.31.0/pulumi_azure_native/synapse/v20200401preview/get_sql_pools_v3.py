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
    'GetSqlPoolsV3Result',
    'AwaitableGetSqlPoolsV3Result',
    'get_sql_pools_v3',
]

@pulumi.output_type
class GetSqlPoolsV3Result:
    """
    A sql pool resource.
    """
    def __init__(__self__, auto_pause_timer=None, auto_resume=None, current_service_objective_name=None, id=None, kind=None, location=None, max_service_objective_name=None, name=None, requested_service_objective_name=None, sku=None, sql_pool_guid=None, status=None, system_data=None, tags=None, type=None):
        if auto_pause_timer and not isinstance(auto_pause_timer, int):
            raise TypeError("Expected argument 'auto_pause_timer' to be a int")
        pulumi.set(__self__, "auto_pause_timer", auto_pause_timer)
        if auto_resume and not isinstance(auto_resume, bool):
            raise TypeError("Expected argument 'auto_resume' to be a bool")
        pulumi.set(__self__, "auto_resume", auto_resume)
        if current_service_objective_name and not isinstance(current_service_objective_name, str):
            raise TypeError("Expected argument 'current_service_objective_name' to be a str")
        pulumi.set(__self__, "current_service_objective_name", current_service_objective_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if max_service_objective_name and not isinstance(max_service_objective_name, str):
            raise TypeError("Expected argument 'max_service_objective_name' to be a str")
        pulumi.set(__self__, "max_service_objective_name", max_service_objective_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if requested_service_objective_name and not isinstance(requested_service_objective_name, str):
            raise TypeError("Expected argument 'requested_service_objective_name' to be a str")
        pulumi.set(__self__, "requested_service_objective_name", requested_service_objective_name)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if sql_pool_guid and not isinstance(sql_pool_guid, str):
            raise TypeError("Expected argument 'sql_pool_guid' to be a str")
        pulumi.set(__self__, "sql_pool_guid", sql_pool_guid)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="autoPauseTimer")
    def auto_pause_timer(self) -> Optional[int]:
        """
        The period of inactivity in minutes before automatically pausing the sql pool.
        """
        return pulumi.get(self, "auto_pause_timer")

    @property
    @pulumi.getter(name="autoResume")
    def auto_resume(self) -> Optional[bool]:
        """
        Indicates whether the sql pool can automatically resume when connection attempts are made.
        """
        return pulumi.get(self, "auto_resume")

    @property
    @pulumi.getter(name="currentServiceObjectiveName")
    def current_service_objective_name(self) -> str:
        """
        The current service level objective name of the sql pool.
        """
        return pulumi.get(self, "current_service_objective_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Kind of SqlPool.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxServiceObjectiveName")
    def max_service_objective_name(self) -> Optional[str]:
        """
        The max service level objective name of the sql pool.
        """
        return pulumi.get(self, "max_service_objective_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requestedServiceObjectiveName")
    def requested_service_objective_name(self) -> str:
        """
        The requested service level objective name of the sql pool.
        """
        return pulumi.get(self, "requested_service_objective_name")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuV3Response']:
        """
        The sql pool SKU. The list of SKUs may vary by region and support offer.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="sqlPoolGuid")
    def sql_pool_guid(self) -> str:
        """
        The Guid of the sql pool.
        """
        return pulumi.get(self, "sql_pool_guid")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the sql pool.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        SystemData of SqlPool.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetSqlPoolsV3Result(GetSqlPoolsV3Result):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlPoolsV3Result(
            auto_pause_timer=self.auto_pause_timer,
            auto_resume=self.auto_resume,
            current_service_objective_name=self.current_service_objective_name,
            id=self.id,
            kind=self.kind,
            location=self.location,
            max_service_objective_name=self.max_service_objective_name,
            name=self.name,
            requested_service_objective_name=self.requested_service_objective_name,
            sku=self.sku,
            sql_pool_guid=self.sql_pool_guid,
            status=self.status,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_sql_pools_v3(resource_group_name: Optional[str] = None,
                     sql_pool_name: Optional[str] = None,
                     workspace_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlPoolsV3Result:
    """
    A sql pool resource.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sql_pool_name: The name of the sql pool.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['sqlPoolName'] = sql_pool_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:synapse/v20200401preview:getSqlPoolsV3', __args__, opts=opts, typ=GetSqlPoolsV3Result).value

    return AwaitableGetSqlPoolsV3Result(
        auto_pause_timer=__ret__.auto_pause_timer,
        auto_resume=__ret__.auto_resume,
        current_service_objective_name=__ret__.current_service_objective_name,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        max_service_objective_name=__ret__.max_service_objective_name,
        name=__ret__.name,
        requested_service_objective_name=__ret__.requested_service_objective_name,
        sku=__ret__.sku,
        sql_pool_guid=__ret__.sql_pool_guid,
        status=__ret__.status,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)
