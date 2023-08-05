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
    'GetSubscriptionFeatureRegistrationResult',
    'AwaitableGetSubscriptionFeatureRegistrationResult',
    'get_subscription_feature_registration',
]

@pulumi.output_type
class GetSubscriptionFeatureRegistrationResult:
    """
    Subscription feature registration details
    """
    def __init__(__self__, id=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.SubscriptionFeatureRegistrationResponseProperties':
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetSubscriptionFeatureRegistrationResult(GetSubscriptionFeatureRegistrationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubscriptionFeatureRegistrationResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_subscription_feature_registration(feature_name: Optional[str] = None,
                                          provider_namespace: Optional[str] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubscriptionFeatureRegistrationResult:
    """
    Subscription feature registration details
    API Version: 2021-07-01.


    :param str feature_name: The feature name.
    :param str provider_namespace: The provider namespace.
    """
    __args__ = dict()
    __args__['featureName'] = feature_name
    __args__['providerNamespace'] = provider_namespace
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:features:getSubscriptionFeatureRegistration', __args__, opts=opts, typ=GetSubscriptionFeatureRegistrationResult).value

    return AwaitableGetSubscriptionFeatureRegistrationResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)
