# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['SapMonitorArgs', 'SapMonitor']

@pulumi.input_type
class SapMonitorArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 enable_customer_analytics: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_arm_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_shared_key: Optional[pulumi.Input[str]] = None,
                 monitor_subnet: Optional[pulumi.Input[str]] = None,
                 sap_monitor_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a SapMonitor resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group.
        :param pulumi.Input[bool] enable_customer_analytics: The value indicating whether to send analytics to Microsoft
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] log_analytics_workspace_arm_id: The ARM ID of the Log Analytics Workspace that is used for monitoring
        :param pulumi.Input[str] log_analytics_workspace_id: The workspace ID of the log analytics workspace to be used for monitoring
        :param pulumi.Input[str] log_analytics_workspace_shared_key: The shared key of the log analytics workspace that is used for monitoring
        :param pulumi.Input[str] monitor_subnet: The subnet which the SAP monitor will be deployed in
        :param pulumi.Input[str] sap_monitor_name: Name of the SAP monitor resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if enable_customer_analytics is not None:
            pulumi.set(__self__, "enable_customer_analytics", enable_customer_analytics)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if log_analytics_workspace_arm_id is not None:
            pulumi.set(__self__, "log_analytics_workspace_arm_id", log_analytics_workspace_arm_id)
        if log_analytics_workspace_id is not None:
            pulumi.set(__self__, "log_analytics_workspace_id", log_analytics_workspace_id)
        if log_analytics_workspace_shared_key is not None:
            pulumi.set(__self__, "log_analytics_workspace_shared_key", log_analytics_workspace_shared_key)
        if monitor_subnet is not None:
            pulumi.set(__self__, "monitor_subnet", monitor_subnet)
        if sap_monitor_name is not None:
            pulumi.set(__self__, "sap_monitor_name", sap_monitor_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="enableCustomerAnalytics")
    def enable_customer_analytics(self) -> Optional[pulumi.Input[bool]]:
        """
        The value indicating whether to send analytics to Microsoft
        """
        return pulumi.get(self, "enable_customer_analytics")

    @enable_customer_analytics.setter
    def enable_customer_analytics(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_customer_analytics", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceArmId")
    def log_analytics_workspace_arm_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ARM ID of the Log Analytics Workspace that is used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_arm_id")

    @log_analytics_workspace_arm_id.setter
    def log_analytics_workspace_arm_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_analytics_workspace_arm_id", value)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The workspace ID of the log analytics workspace to be used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_analytics_workspace_id", value)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceSharedKey")
    def log_analytics_workspace_shared_key(self) -> Optional[pulumi.Input[str]]:
        """
        The shared key of the log analytics workspace that is used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_shared_key")

    @log_analytics_workspace_shared_key.setter
    def log_analytics_workspace_shared_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_analytics_workspace_shared_key", value)

    @property
    @pulumi.getter(name="monitorSubnet")
    def monitor_subnet(self) -> Optional[pulumi.Input[str]]:
        """
        The subnet which the SAP monitor will be deployed in
        """
        return pulumi.get(self, "monitor_subnet")

    @monitor_subnet.setter
    def monitor_subnet(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_subnet", value)

    @property
    @pulumi.getter(name="sapMonitorName")
    def sap_monitor_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the SAP monitor resource.
        """
        return pulumi.get(self, "sap_monitor_name")

    @sap_monitor_name.setter
    def sap_monitor_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sap_monitor_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class SapMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_customer_analytics: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_arm_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_shared_key: Optional[pulumi.Input[str]] = None,
                 monitor_subnet: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_monitor_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        SAP monitor info on Azure (ARM properties and SAP monitor properties)

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enable_customer_analytics: The value indicating whether to send analytics to Microsoft
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] log_analytics_workspace_arm_id: The ARM ID of the Log Analytics Workspace that is used for monitoring
        :param pulumi.Input[str] log_analytics_workspace_id: The workspace ID of the log analytics workspace to be used for monitoring
        :param pulumi.Input[str] log_analytics_workspace_shared_key: The shared key of the log analytics workspace that is used for monitoring
        :param pulumi.Input[str] monitor_subnet: The subnet which the SAP monitor will be deployed in
        :param pulumi.Input[str] resource_group_name: Name of the resource group.
        :param pulumi.Input[str] sap_monitor_name: Name of the SAP monitor resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SapMonitorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        SAP monitor info on Azure (ARM properties and SAP monitor properties)

        :param str resource_name: The name of the resource.
        :param SapMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SapMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_customer_analytics: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_arm_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_shared_key: Optional[pulumi.Input[str]] = None,
                 monitor_subnet: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_monitor_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = SapMonitorArgs.__new__(SapMonitorArgs)

            __props__.__dict__["enable_customer_analytics"] = enable_customer_analytics
            __props__.__dict__["location"] = location
            __props__.__dict__["log_analytics_workspace_arm_id"] = log_analytics_workspace_arm_id
            __props__.__dict__["log_analytics_workspace_id"] = log_analytics_workspace_id
            __props__.__dict__["log_analytics_workspace_shared_key"] = log_analytics_workspace_shared_key
            __props__.__dict__["monitor_subnet"] = monitor_subnet
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sap_monitor_name"] = sap_monitor_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["managed_resource_group_name"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["sap_monitor_collector_version"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:hanaonazure/v20200207preview:SapMonitor"), pulumi.Alias(type_="azure-native:hanaonazure:SapMonitor"), pulumi.Alias(type_="azure-nextgen:hanaonazure:SapMonitor")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SapMonitor, __self__).__init__(
            'azure-native:hanaonazure/v20200207preview:SapMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SapMonitor':
        """
        Get an existing SapMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SapMonitorArgs.__new__(SapMonitorArgs)

        __props__.__dict__["enable_customer_analytics"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["log_analytics_workspace_arm_id"] = None
        __props__.__dict__["log_analytics_workspace_id"] = None
        __props__.__dict__["log_analytics_workspace_shared_key"] = None
        __props__.__dict__["managed_resource_group_name"] = None
        __props__.__dict__["monitor_subnet"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sap_monitor_collector_version"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return SapMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="enableCustomerAnalytics")
    def enable_customer_analytics(self) -> pulumi.Output[Optional[bool]]:
        """
        The value indicating whether to send analytics to Microsoft
        """
        return pulumi.get(self, "enable_customer_analytics")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceArmId")
    def log_analytics_workspace_arm_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ARM ID of the Log Analytics Workspace that is used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_arm_id")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> pulumi.Output[Optional[str]]:
        """
        The workspace ID of the log analytics workspace to be used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceSharedKey")
    def log_analytics_workspace_shared_key(self) -> pulumi.Output[Optional[str]]:
        """
        The shared key of the log analytics workspace that is used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_shared_key")

    @property
    @pulumi.getter(name="managedResourceGroupName")
    def managed_resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group the SAP Monitor resources get deployed into.
        """
        return pulumi.get(self, "managed_resource_group_name")

    @property
    @pulumi.getter(name="monitorSubnet")
    def monitor_subnet(self) -> pulumi.Output[Optional[str]]:
        """
        The subnet which the SAP monitor will be deployed in
        """
        return pulumi.get(self, "monitor_subnet")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        State of provisioning of the HanaInstance
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sapMonitorCollectorVersion")
    def sap_monitor_collector_version(self) -> pulumi.Output[str]:
        """
        The version of the payload running in the Collector VM
        """
        return pulumi.get(self, "sap_monitor_collector_version")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

