# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'ListManagedClusterMonitoringUserCredentialsResult',
    'AwaitableListManagedClusterMonitoringUserCredentialsResult',
    'list_managed_cluster_monitoring_user_credentials',
]

@pulumi.output_type
class ListManagedClusterMonitoringUserCredentialsResult:
    """
    The list of credential result response.
    """
    def __init__(__self__, kubeconfigs=None):
        if kubeconfigs and not isinstance(kubeconfigs, list):
            raise TypeError("Expected argument 'kubeconfigs' to be a list")
        pulumi.set(__self__, "kubeconfigs", kubeconfigs)

    @property
    @pulumi.getter
    def kubeconfigs(self) -> Sequence['outputs.CredentialResultResponse']:
        """
        Base64-encoded Kubernetes configuration file.
        """
        return pulumi.get(self, "kubeconfigs")


class AwaitableListManagedClusterMonitoringUserCredentialsResult(ListManagedClusterMonitoringUserCredentialsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListManagedClusterMonitoringUserCredentialsResult(
            kubeconfigs=self.kubeconfigs)


def list_managed_cluster_monitoring_user_credentials(resource_group_name: Optional[str] = None,
                                                     resource_name: Optional[str] = None,
                                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListManagedClusterMonitoringUserCredentialsResult:
    """
    The list of credential result response.
    API Version: 2021-03-01.


    :param str resource_group_name: The name of the resource group.
    :param str resource_name: The name of the managed cluster resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:containerservice:listManagedClusterMonitoringUserCredentials', __args__, opts=opts, typ=ListManagedClusterMonitoringUserCredentialsResult).value

    return AwaitableListManagedClusterMonitoringUserCredentialsResult(
        kubeconfigs=__ret__.kubeconfigs)
