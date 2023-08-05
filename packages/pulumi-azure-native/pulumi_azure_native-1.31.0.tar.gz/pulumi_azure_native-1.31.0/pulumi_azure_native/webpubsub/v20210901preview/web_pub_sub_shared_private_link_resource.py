# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = ['WebPubSubSharedPrivateLinkResourceArgs', 'WebPubSubSharedPrivateLinkResource']

@pulumi.input_type
class WebPubSubSharedPrivateLinkResourceArgs:
    def __init__(__self__, *,
                 group_id: pulumi.Input[str],
                 private_link_resource_id: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 request_message: Optional[pulumi.Input[str]] = None,
                 shared_private_link_resource_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WebPubSubSharedPrivateLinkResource resource.
        :param pulumi.Input[str] group_id: The group id from the provider of resource the shared private link resource is for
        :param pulumi.Input[str] private_link_resource_id: The resource id of the resource the shared private link resource is for
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] resource_name: The name of the resource.
        :param pulumi.Input[str] request_message: The request message for requesting approval of the shared private link resource
        :param pulumi.Input[str] shared_private_link_resource_name: The name of the shared private link resource
        """
        pulumi.set(__self__, "group_id", group_id)
        pulumi.set(__self__, "private_link_resource_id", private_link_resource_id)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if request_message is not None:
            pulumi.set(__self__, "request_message", request_message)
        if shared_private_link_resource_name is not None:
            pulumi.set(__self__, "shared_private_link_resource_name", shared_private_link_resource_name)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Input[str]:
        """
        The group id from the provider of resource the shared private link resource is for
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="privateLinkResourceId")
    def private_link_resource_id(self) -> pulumi.Input[str]:
        """
        The resource id of the resource the shared private link resource is for
        """
        return pulumi.get(self, "private_link_resource_id")

    @private_link_resource_id.setter
    def private_link_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "private_link_resource_id", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> Optional[pulumi.Input[str]]:
        """
        The request message for requesting approval of the shared private link resource
        """
        return pulumi.get(self, "request_message")

    @request_message.setter
    def request_message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_message", value)

    @property
    @pulumi.getter(name="sharedPrivateLinkResourceName")
    def shared_private_link_resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the shared private link resource
        """
        return pulumi.get(self, "shared_private_link_resource_name")

    @shared_private_link_resource_name.setter
    def shared_private_link_resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "shared_private_link_resource_name", value)


class WebPubSubSharedPrivateLinkResource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 private_link_resource_id: Optional[pulumi.Input[str]] = None,
                 request_message: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 shared_private_link_resource_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Describes a Shared Private Link Resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_id: The group id from the provider of resource the shared private link resource is for
        :param pulumi.Input[str] private_link_resource_id: The resource id of the resource the shared private link resource is for
        :param pulumi.Input[str] request_message: The request message for requesting approval of the shared private link resource
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] resource_name_: The name of the resource.
        :param pulumi.Input[str] shared_private_link_resource_name: The name of the shared private link resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebPubSubSharedPrivateLinkResourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a Shared Private Link Resource

        :param str resource_name: The name of the resource.
        :param WebPubSubSharedPrivateLinkResourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebPubSubSharedPrivateLinkResourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 private_link_resource_id: Optional[pulumi.Input[str]] = None,
                 request_message: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 shared_private_link_resource_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebPubSubSharedPrivateLinkResourceArgs.__new__(WebPubSubSharedPrivateLinkResourceArgs)

            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__["group_id"] = group_id
            if private_link_resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'private_link_resource_id'")
            __props__.__dict__["private_link_resource_id"] = private_link_resource_id
            __props__.__dict__["request_message"] = request_message
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["shared_private_link_resource_name"] = shared_private_link_resource_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:webpubsub/v20210901preview:WebPubSubSharedPrivateLinkResource"), pulumi.Alias(type_="azure-native:webpubsub:WebPubSubSharedPrivateLinkResource"), pulumi.Alias(type_="azure-nextgen:webpubsub:WebPubSubSharedPrivateLinkResource"), pulumi.Alias(type_="azure-native:webpubsub/v20210401preview:WebPubSubSharedPrivateLinkResource"), pulumi.Alias(type_="azure-nextgen:webpubsub/v20210401preview:WebPubSubSharedPrivateLinkResource"), pulumi.Alias(type_="azure-native:webpubsub/v20210601preview:WebPubSubSharedPrivateLinkResource"), pulumi.Alias(type_="azure-nextgen:webpubsub/v20210601preview:WebPubSubSharedPrivateLinkResource")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebPubSubSharedPrivateLinkResource, __self__).__init__(
            'azure-native:webpubsub/v20210901preview:WebPubSubSharedPrivateLinkResource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebPubSubSharedPrivateLinkResource':
        """
        Get an existing WebPubSubSharedPrivateLinkResource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WebPubSubSharedPrivateLinkResourceArgs.__new__(WebPubSubSharedPrivateLinkResourceArgs)

        __props__.__dict__["group_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["private_link_resource_id"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["request_message"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return WebPubSubSharedPrivateLinkResource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        """
        The group id from the provider of resource the shared private link resource is for
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateLinkResourceId")
    def private_link_resource_id(self) -> pulumi.Output[str]:
        """
        The resource id of the resource the shared private link resource is for
        """
        return pulumi.get(self, "private_link_resource_id")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the shared private link resource
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> pulumi.Output[Optional[str]]:
        """
        The request message for requesting approval of the shared private link resource
        """
        return pulumi.get(self, "request_message")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the shared private link resource
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, "type")

