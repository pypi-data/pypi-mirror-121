# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ListDeploymentInfoResult',
    'AwaitableListDeploymentInfoResult',
    'list_deployment_info',
]

@pulumi.output_type
class ListDeploymentInfoResult:
    """
    The properties of deployment in Elastic cloud corresponding to the Elastic monitor resource.
    """
    def __init__(__self__, disk_capacity=None, memory_capacity=None, status=None, version=None):
        if disk_capacity and not isinstance(disk_capacity, str):
            raise TypeError("Expected argument 'disk_capacity' to be a str")
        pulumi.set(__self__, "disk_capacity", disk_capacity)
        if memory_capacity and not isinstance(memory_capacity, str):
            raise TypeError("Expected argument 'memory_capacity' to be a str")
        pulumi.set(__self__, "memory_capacity", memory_capacity)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="diskCapacity")
    def disk_capacity(self) -> str:
        """
        Disk capacity of the elasticsearch in Elastic cloud deployment.
        """
        return pulumi.get(self, "disk_capacity")

    @property
    @pulumi.getter(name="memoryCapacity")
    def memory_capacity(self) -> str:
        """
        RAM capacity of the elasticsearch in Elastic cloud deployment.
        """
        return pulumi.get(self, "memory_capacity")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The Elastic deployment status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Version of the elasticsearch in Elastic cloud deployment.
        """
        return pulumi.get(self, "version")


class AwaitableListDeploymentInfoResult(ListDeploymentInfoResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListDeploymentInfoResult(
            disk_capacity=self.disk_capacity,
            memory_capacity=self.memory_capacity,
            status=self.status,
            version=self.version)


def list_deployment_info(monitor_name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListDeploymentInfoResult:
    """
    The properties of deployment in Elastic cloud corresponding to the Elastic monitor resource.
    API Version: 2020-07-01.


    :param str monitor_name: Monitor resource name
    :param str resource_group_name: The name of the resource group to which the Elastic resource belongs.
    """
    __args__ = dict()
    __args__['monitorName'] = monitor_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:elastic:listDeploymentInfo', __args__, opts=opts, typ=ListDeploymentInfoResult).value

    return AwaitableListDeploymentInfoResult(
        disk_capacity=__ret__.disk_capacity,
        memory_capacity=__ret__.memory_capacity,
        status=__ret__.status,
        version=__ret__.version)
