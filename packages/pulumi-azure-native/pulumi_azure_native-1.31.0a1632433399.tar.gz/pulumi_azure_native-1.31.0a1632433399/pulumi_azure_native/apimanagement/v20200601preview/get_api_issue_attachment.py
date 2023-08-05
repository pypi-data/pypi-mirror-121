# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetApiIssueAttachmentResult',
    'AwaitableGetApiIssueAttachmentResult',
    'get_api_issue_attachment',
]

@pulumi.output_type
class GetApiIssueAttachmentResult:
    """
    Issue Attachment Contract details.
    """
    def __init__(__self__, content=None, content_format=None, id=None, name=None, title=None, type=None):
        if content and not isinstance(content, str):
            raise TypeError("Expected argument 'content' to be a str")
        pulumi.set(__self__, "content", content)
        if content_format and not isinstance(content_format, str):
            raise TypeError("Expected argument 'content_format' to be a str")
        pulumi.set(__self__, "content_format", content_format)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if title and not isinstance(title, str):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, "title", title)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        An HTTP link or Base64-encoded binary data.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="contentFormat")
    def content_format(self) -> str:
        """
        Either 'link' if content is provided via an HTTP link or the MIME type of the Base64-encoded binary data provided in the 'content' property.
        """
        return pulumi.get(self, "content_format")

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
    @pulumi.getter
    def title(self) -> str:
        """
        Filename by which the binary data will be saved.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetApiIssueAttachmentResult(GetApiIssueAttachmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApiIssueAttachmentResult(
            content=self.content,
            content_format=self.content_format,
            id=self.id,
            name=self.name,
            title=self.title,
            type=self.type)


def get_api_issue_attachment(api_id: Optional[str] = None,
                             attachment_id: Optional[str] = None,
                             issue_id: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             service_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApiIssueAttachmentResult:
    """
    Issue Attachment Contract details.


    :param str api_id: API identifier. Must be unique in the current API Management service instance.
    :param str attachment_id: Attachment identifier within an Issue. Must be unique in the current Issue.
    :param str issue_id: Issue identifier. Must be unique in the current API Management service instance.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['apiId'] = api_id
    __args__['attachmentId'] = attachment_id
    __args__['issueId'] = issue_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20200601preview:getApiIssueAttachment', __args__, opts=opts, typ=GetApiIssueAttachmentResult).value

    return AwaitableGetApiIssueAttachmentResult(
        content=__ret__.content,
        content_format=__ret__.content_format,
        id=__ret__.id,
        name=__ret__.name,
        title=__ret__.title,
        type=__ret__.type)
