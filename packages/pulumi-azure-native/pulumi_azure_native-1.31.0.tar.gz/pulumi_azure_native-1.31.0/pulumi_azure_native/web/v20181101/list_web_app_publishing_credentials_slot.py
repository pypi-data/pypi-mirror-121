# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'ListWebAppPublishingCredentialsSlotResult',
    'AwaitableListWebAppPublishingCredentialsSlotResult',
    'list_web_app_publishing_credentials_slot',
]

@pulumi.output_type
class ListWebAppPublishingCredentialsSlotResult:
    """
    User credentials used for publishing activity.
    """
    def __init__(__self__, id=None, kind=None, name=None, publishing_password=None, publishing_password_hash=None, publishing_password_hash_salt=None, publishing_user_name=None, scm_uri=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if publishing_password and not isinstance(publishing_password, str):
            raise TypeError("Expected argument 'publishing_password' to be a str")
        pulumi.set(__self__, "publishing_password", publishing_password)
        if publishing_password_hash and not isinstance(publishing_password_hash, str):
            raise TypeError("Expected argument 'publishing_password_hash' to be a str")
        pulumi.set(__self__, "publishing_password_hash", publishing_password_hash)
        if publishing_password_hash_salt and not isinstance(publishing_password_hash_salt, str):
            raise TypeError("Expected argument 'publishing_password_hash_salt' to be a str")
        pulumi.set(__self__, "publishing_password_hash_salt", publishing_password_hash_salt)
        if publishing_user_name and not isinstance(publishing_user_name, str):
            raise TypeError("Expected argument 'publishing_user_name' to be a str")
        pulumi.set(__self__, "publishing_user_name", publishing_user_name)
        if scm_uri and not isinstance(scm_uri, str):
            raise TypeError("Expected argument 'scm_uri' to be a str")
        pulumi.set(__self__, "scm_uri", scm_uri)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publishingPassword")
    def publishing_password(self) -> Optional[str]:
        """
        Password used for publishing.
        """
        return pulumi.get(self, "publishing_password")

    @property
    @pulumi.getter(name="publishingPasswordHash")
    def publishing_password_hash(self) -> Optional[str]:
        """
        Password hash used for publishing.
        """
        return pulumi.get(self, "publishing_password_hash")

    @property
    @pulumi.getter(name="publishingPasswordHashSalt")
    def publishing_password_hash_salt(self) -> Optional[str]:
        """
        Password hash salt used for publishing.
        """
        return pulumi.get(self, "publishing_password_hash_salt")

    @property
    @pulumi.getter(name="publishingUserName")
    def publishing_user_name(self) -> str:
        """
        Username used for publishing.
        """
        return pulumi.get(self, "publishing_user_name")

    @property
    @pulumi.getter(name="scmUri")
    def scm_uri(self) -> Optional[str]:
        """
        Url of SCM site.
        """
        return pulumi.get(self, "scm_uri")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableListWebAppPublishingCredentialsSlotResult(ListWebAppPublishingCredentialsSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWebAppPublishingCredentialsSlotResult(
            id=self.id,
            kind=self.kind,
            name=self.name,
            publishing_password=self.publishing_password,
            publishing_password_hash=self.publishing_password_hash,
            publishing_password_hash_salt=self.publishing_password_hash_salt,
            publishing_user_name=self.publishing_user_name,
            scm_uri=self.scm_uri,
            type=self.type)


def list_web_app_publishing_credentials_slot(name: Optional[str] = None,
                                             resource_group_name: Optional[str] = None,
                                             slot: Optional[str] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWebAppPublishingCredentialsSlotResult:
    """
    User credentials used for publishing activity.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get the publishing credentials for the production slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20181101:listWebAppPublishingCredentialsSlot', __args__, opts=opts, typ=ListWebAppPublishingCredentialsSlotResult).value

    return AwaitableListWebAppPublishingCredentialsSlotResult(
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        publishing_password=__ret__.publishing_password,
        publishing_password_hash=__ret__.publishing_password_hash,
        publishing_password_hash_salt=__ret__.publishing_password_hash_salt,
        publishing_user_name=__ret__.publishing_user_name,
        scm_uri=__ret__.scm_uri,
        type=__ret__.type)
