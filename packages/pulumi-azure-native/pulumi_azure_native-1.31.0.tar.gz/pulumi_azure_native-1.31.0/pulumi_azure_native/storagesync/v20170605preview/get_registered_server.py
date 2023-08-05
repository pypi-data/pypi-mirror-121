# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetRegisteredServerResult',
    'AwaitableGetRegisteredServerResult',
    'get_registered_server',
]

@pulumi.output_type
class GetRegisteredServerResult:
    """
    Registered Server resource.
    """
    def __init__(__self__, agent_version=None, cluster_id=None, cluster_name=None, id=None, last_heart_beat=None, last_workflow_id=None, name=None, provisioning_state=None, server_certificate=None, server_id=None, server_managementt_error_code=None, server_os_version=None, server_role=None, storage_sync_service_uid=None, type=None):
        if agent_version and not isinstance(agent_version, str):
            raise TypeError("Expected argument 'agent_version' to be a str")
        pulumi.set(__self__, "agent_version", agent_version)
        if cluster_id and not isinstance(cluster_id, str):
            raise TypeError("Expected argument 'cluster_id' to be a str")
        pulumi.set(__self__, "cluster_id", cluster_id)
        if cluster_name and not isinstance(cluster_name, str):
            raise TypeError("Expected argument 'cluster_name' to be a str")
        pulumi.set(__self__, "cluster_name", cluster_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_heart_beat and not isinstance(last_heart_beat, str):
            raise TypeError("Expected argument 'last_heart_beat' to be a str")
        pulumi.set(__self__, "last_heart_beat", last_heart_beat)
        if last_workflow_id and not isinstance(last_workflow_id, str):
            raise TypeError("Expected argument 'last_workflow_id' to be a str")
        pulumi.set(__self__, "last_workflow_id", last_workflow_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if server_certificate and not isinstance(server_certificate, str):
            raise TypeError("Expected argument 'server_certificate' to be a str")
        pulumi.set(__self__, "server_certificate", server_certificate)
        if server_id and not isinstance(server_id, str):
            raise TypeError("Expected argument 'server_id' to be a str")
        pulumi.set(__self__, "server_id", server_id)
        if server_managementt_error_code and not isinstance(server_managementt_error_code, int):
            raise TypeError("Expected argument 'server_managementt_error_code' to be a int")
        pulumi.set(__self__, "server_managementt_error_code", server_managementt_error_code)
        if server_os_version and not isinstance(server_os_version, str):
            raise TypeError("Expected argument 'server_os_version' to be a str")
        pulumi.set(__self__, "server_os_version", server_os_version)
        if server_role and not isinstance(server_role, str):
            raise TypeError("Expected argument 'server_role' to be a str")
        pulumi.set(__self__, "server_role", server_role)
        if storage_sync_service_uid and not isinstance(storage_sync_service_uid, str):
            raise TypeError("Expected argument 'storage_sync_service_uid' to be a str")
        pulumi.set(__self__, "storage_sync_service_uid", storage_sync_service_uid)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> Optional[str]:
        """
        Registered Server Agent Version
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> Optional[str]:
        """
        Registered Server clusterId
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[str]:
        """
        Registered Server clusterName
        """
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastHeartBeat")
    def last_heart_beat(self) -> Optional[str]:
        """
        Registered Server last heart beat
        """
        return pulumi.get(self, "last_heart_beat")

    @property
    @pulumi.getter(name="lastWorkflowId")
    def last_workflow_id(self) -> Optional[str]:
        """
        Registered Server lastWorkflowId
        """
        return pulumi.get(self, "last_workflow_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Registered Server Provisioning State
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serverCertificate")
    def server_certificate(self) -> Optional[str]:
        """
        Registered Server Certificate
        """
        return pulumi.get(self, "server_certificate")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[str]:
        """
        Registered Server serverId
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter(name="serverManagementtErrorCode")
    def server_managementt_error_code(self) -> Optional[int]:
        """
        Registered Server Management Error Code
        """
        return pulumi.get(self, "server_managementt_error_code")

    @property
    @pulumi.getter(name="serverOSVersion")
    def server_os_version(self) -> Optional[str]:
        """
        Registered Server OS Version
        """
        return pulumi.get(self, "server_os_version")

    @property
    @pulumi.getter(name="serverRole")
    def server_role(self) -> Optional[str]:
        """
        Registered Server serverRole
        """
        return pulumi.get(self, "server_role")

    @property
    @pulumi.getter(name="storageSyncServiceUid")
    def storage_sync_service_uid(self) -> Optional[str]:
        """
        Registered Server storageSyncServiceUid
        """
        return pulumi.get(self, "storage_sync_service_uid")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetRegisteredServerResult(GetRegisteredServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegisteredServerResult(
            agent_version=self.agent_version,
            cluster_id=self.cluster_id,
            cluster_name=self.cluster_name,
            id=self.id,
            last_heart_beat=self.last_heart_beat,
            last_workflow_id=self.last_workflow_id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            server_certificate=self.server_certificate,
            server_id=self.server_id,
            server_managementt_error_code=self.server_managementt_error_code,
            server_os_version=self.server_os_version,
            server_role=self.server_role,
            storage_sync_service_uid=self.storage_sync_service_uid,
            type=self.type)


def get_registered_server(resource_group_name: Optional[str] = None,
                          server_id: Optional[str] = None,
                          storage_sync_service_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegisteredServerResult:
    """
    Registered Server resource.


    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    :param str server_id: GUID identifying the on-premises server.
    :param str storage_sync_service_name: Name of Storage Sync Service resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverId'] = server_id
    __args__['storageSyncServiceName'] = storage_sync_service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:storagesync/v20170605preview:getRegisteredServer', __args__, opts=opts, typ=GetRegisteredServerResult).value

    return AwaitableGetRegisteredServerResult(
        agent_version=__ret__.agent_version,
        cluster_id=__ret__.cluster_id,
        cluster_name=__ret__.cluster_name,
        id=__ret__.id,
        last_heart_beat=__ret__.last_heart_beat,
        last_workflow_id=__ret__.last_workflow_id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        server_certificate=__ret__.server_certificate,
        server_id=__ret__.server_id,
        server_managementt_error_code=__ret__.server_managementt_error_code,
        server_os_version=__ret__.server_os_version,
        server_role=__ret__.server_role,
        storage_sync_service_uid=__ret__.storage_sync_service_uid,
        type=__ret__.type)
