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
    'GetConsumerGroupResult',
    'AwaitableGetConsumerGroupResult',
    'get_consumer_group',
]

@pulumi.output_type
class GetConsumerGroupResult:
    """
    Single item in List or Get Consumer group operation
    """
    def __init__(__self__, created_at=None, id=None, name=None, system_data=None, type=None, updated_at=None, user_metadata=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if user_metadata and not isinstance(user_metadata, str):
            raise TypeError("Expected argument 'user_metadata' to be a str")
        pulumi.set(__self__, "user_metadata", user_metadata)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Exact time the message was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The exact time the message was updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="userMetadata")
    def user_metadata(self) -> Optional[str]:
        """
        User Metadata is a placeholder to store user-defined string data with maximum length 1024. e.g. it can be used to store descriptive data, such as list of teams and their contact information also user-defined configuration settings can be stored.
        """
        return pulumi.get(self, "user_metadata")


class AwaitableGetConsumerGroupResult(GetConsumerGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConsumerGroupResult(
            created_at=self.created_at,
            id=self.id,
            name=self.name,
            system_data=self.system_data,
            type=self.type,
            updated_at=self.updated_at,
            user_metadata=self.user_metadata)


def get_consumer_group(consumer_group_name: Optional[str] = None,
                       event_hub_name: Optional[str] = None,
                       namespace_name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConsumerGroupResult:
    """
    Single item in List or Get Consumer group operation


    :param str consumer_group_name: The consumer group name
    :param str event_hub_name: The Event Hub name
    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    __args__ = dict()
    __args__['consumerGroupName'] = consumer_group_name
    __args__['eventHubName'] = event_hub_name
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:eventhub/v20210601preview:getConsumerGroup', __args__, opts=opts, typ=GetConsumerGroupResult).value

    return AwaitableGetConsumerGroupResult(
        created_at=__ret__.created_at,
        id=__ret__.id,
        name=__ret__.name,
        system_data=__ret__.system_data,
        type=__ret__.type,
        updated_at=__ret__.updated_at,
        user_metadata=__ret__.user_metadata)
