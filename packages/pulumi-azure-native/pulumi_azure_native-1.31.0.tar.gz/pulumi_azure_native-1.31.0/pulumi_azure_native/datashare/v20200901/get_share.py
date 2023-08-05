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
    'GetShareResult',
    'AwaitableGetShareResult',
    'get_share',
]

@pulumi.output_type
class GetShareResult:
    """
    A share data transfer object.
    """
    def __init__(__self__, created_at=None, description=None, id=None, name=None, provisioning_state=None, share_kind=None, system_data=None, terms=None, type=None, user_email=None, user_name=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if share_kind and not isinstance(share_kind, str):
            raise TypeError("Expected argument 'share_kind' to be a str")
        pulumi.set(__self__, "share_kind", share_kind)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if terms and not isinstance(terms, str):
            raise TypeError("Expected argument 'terms' to be a str")
        pulumi.set(__self__, "terms", terms)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_email and not isinstance(user_email, str):
            raise TypeError("Expected argument 'user_email' to be a str")
        pulumi.set(__self__, "user_email", user_email)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Time at which the share was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Share description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource id of the azure resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the azure resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Gets or sets the provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="shareKind")
    def share_kind(self) -> Optional[str]:
        """
        Share kind.
        """
        return pulumi.get(self, "share_kind")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        System Data of the Azure resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def terms(self) -> Optional[str]:
        """
        Share terms.
        """
        return pulumi.get(self, "terms")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the azure resource
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userEmail")
    def user_email(self) -> str:
        """
        Email of the user who created the resource
        """
        return pulumi.get(self, "user_email")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> str:
        """
        Name of the user who created the resource
        """
        return pulumi.get(self, "user_name")


class AwaitableGetShareResult(GetShareResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetShareResult(
            created_at=self.created_at,
            description=self.description,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            share_kind=self.share_kind,
            system_data=self.system_data,
            terms=self.terms,
            type=self.type,
            user_email=self.user_email,
            user_name=self.user_name)


def get_share(account_name: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              share_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetShareResult:
    """
    A share data transfer object.


    :param str account_name: The name of the share account.
    :param str resource_group_name: The resource group name.
    :param str share_name: The name of the share to retrieve.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['shareName'] = share_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:datashare/v20200901:getShare', __args__, opts=opts, typ=GetShareResult).value

    return AwaitableGetShareResult(
        created_at=__ret__.created_at,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        share_kind=__ret__.share_kind,
        system_data=__ret__.system_data,
        terms=__ret__.terms,
        type=__ret__.type,
        user_email=__ret__.user_email,
        user_name=__ret__.user_name)
