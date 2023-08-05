# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetAdvancedThreatProtectionResult',
    'AwaitableGetAdvancedThreatProtectionResult',
    'get_advanced_threat_protection',
]

@pulumi.output_type
class GetAdvancedThreatProtectionResult:
    """
    The Advanced Threat Protection resource.
    """
    def __init__(__self__, id=None, is_enabled=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_enabled and not isinstance(is_enabled, bool):
            raise TypeError("Expected argument 'is_enabled' to be a bool")
        pulumi.set(__self__, "is_enabled", is_enabled)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> Optional[bool]:
        """
        Indicates whether Advanced Threat Protection is enabled.
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetAdvancedThreatProtectionResult(GetAdvancedThreatProtectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAdvancedThreatProtectionResult(
            id=self.id,
            is_enabled=self.is_enabled,
            name=self.name,
            type=self.type)


def get_advanced_threat_protection(resource_id: Optional[str] = None,
                                   setting_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAdvancedThreatProtectionResult:
    """
    The Advanced Threat Protection resource.


    :param str resource_id: The identifier of the resource.
    :param str setting_name: Advanced Threat Protection setting name.
    """
    __args__ = dict()
    __args__['resourceId'] = resource_id
    __args__['settingName'] = setting_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:security/v20170801preview:getAdvancedThreatProtection', __args__, opts=opts, typ=GetAdvancedThreatProtectionResult).value

    return AwaitableGetAdvancedThreatProtectionResult(
        id=__ret__.id,
        is_enabled=__ret__.is_enabled,
        name=__ret__.name,
        type=__ret__.type)
