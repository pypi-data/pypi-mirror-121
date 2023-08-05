# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetStaticSiteUserProvidedFunctionAppForStaticSiteResult',
    'AwaitableGetStaticSiteUserProvidedFunctionAppForStaticSiteResult',
    'get_static_site_user_provided_function_app_for_static_site',
]

@pulumi.output_type
class GetStaticSiteUserProvidedFunctionAppForStaticSiteResult:
    """
    Static Site User Provided Function App ARM resource.
    """
    def __init__(__self__, created_on=None, function_app_region=None, function_app_resource_id=None, id=None, kind=None, name=None, type=None):
        if created_on and not isinstance(created_on, str):
            raise TypeError("Expected argument 'created_on' to be a str")
        pulumi.set(__self__, "created_on", created_on)
        if function_app_region and not isinstance(function_app_region, str):
            raise TypeError("Expected argument 'function_app_region' to be a str")
        pulumi.set(__self__, "function_app_region", function_app_region)
        if function_app_resource_id and not isinstance(function_app_resource_id, str):
            raise TypeError("Expected argument 'function_app_resource_id' to be a str")
        pulumi.set(__self__, "function_app_resource_id", function_app_resource_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> str:
        """
        The date and time on which the function app was registered with the static site.
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter(name="functionAppRegion")
    def function_app_region(self) -> Optional[str]:
        """
        The region of the function app registered with the static site
        """
        return pulumi.get(self, "function_app_region")

    @property
    @pulumi.getter(name="functionAppResourceId")
    def function_app_resource_id(self) -> Optional[str]:
        """
        The resource id of the function app registered with the static site
        """
        return pulumi.get(self, "function_app_resource_id")

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
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetStaticSiteUserProvidedFunctionAppForStaticSiteResult(GetStaticSiteUserProvidedFunctionAppForStaticSiteResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStaticSiteUserProvidedFunctionAppForStaticSiteResult(
            created_on=self.created_on,
            function_app_region=self.function_app_region,
            function_app_resource_id=self.function_app_resource_id,
            id=self.id,
            kind=self.kind,
            name=self.name,
            type=self.type)


def get_static_site_user_provided_function_app_for_static_site(function_app_name: Optional[str] = None,
                                                               name: Optional[str] = None,
                                                               resource_group_name: Optional[str] = None,
                                                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStaticSiteUserProvidedFunctionAppForStaticSiteResult:
    """
    Static Site User Provided Function App ARM resource.


    :param str function_app_name: Name of the function app registered with the static site.
    :param str name: Name of the static site.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['functionAppName'] = function_app_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20210201:getStaticSiteUserProvidedFunctionAppForStaticSite', __args__, opts=opts, typ=GetStaticSiteUserProvidedFunctionAppForStaticSiteResult).value

    return AwaitableGetStaticSiteUserProvidedFunctionAppForStaticSiteResult(
        created_on=__ret__.created_on,
        function_app_region=__ret__.function_app_region,
        function_app_resource_id=__ret__.function_app_resource_id,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        type=__ret__.type)
