# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = ['SiteSensorArgs', 'SiteSensor']

@pulumi.input_type
class SiteSensorArgs:
    def __init__(__self__, *,
                 iot_defender_location: pulumi.Input[str],
                 site_name: pulumi.Input[str],
                 sensor_name: Optional[pulumi.Input[str]] = None,
                 sensor_type: Optional[pulumi.Input[Union[str, 'SensorType']]] = None,
                 ti_automatic_updates: Optional[pulumi.Input[bool]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SiteSensor resource.
        :param pulumi.Input[str] iot_defender_location: Defender for IoT location
        :param pulumi.Input[str] site_name: Site Name
        :param pulumi.Input[str] sensor_name: Name of the IoT sensor
        :param pulumi.Input[Union[str, 'SensorType']] sensor_type: Type of sensor
        :param pulumi.Input[bool] ti_automatic_updates: TI Automatic mode status of the IoT sensor
        :param pulumi.Input[str] zone: Zone of the IoT sensor
        """
        pulumi.set(__self__, "iot_defender_location", iot_defender_location)
        pulumi.set(__self__, "site_name", site_name)
        if sensor_name is not None:
            pulumi.set(__self__, "sensor_name", sensor_name)
        if sensor_type is not None:
            pulumi.set(__self__, "sensor_type", sensor_type)
        if ti_automatic_updates is not None:
            pulumi.set(__self__, "ti_automatic_updates", ti_automatic_updates)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="iotDefenderLocation")
    def iot_defender_location(self) -> pulumi.Input[str]:
        """
        Defender for IoT location
        """
        return pulumi.get(self, "iot_defender_location")

    @iot_defender_location.setter
    def iot_defender_location(self, value: pulumi.Input[str]):
        pulumi.set(self, "iot_defender_location", value)

    @property
    @pulumi.getter(name="siteName")
    def site_name(self) -> pulumi.Input[str]:
        """
        Site Name
        """
        return pulumi.get(self, "site_name")

    @site_name.setter
    def site_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "site_name", value)

    @property
    @pulumi.getter(name="sensorName")
    def sensor_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the IoT sensor
        """
        return pulumi.get(self, "sensor_name")

    @sensor_name.setter
    def sensor_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sensor_name", value)

    @property
    @pulumi.getter(name="sensorType")
    def sensor_type(self) -> Optional[pulumi.Input[Union[str, 'SensorType']]]:
        """
        Type of sensor
        """
        return pulumi.get(self, "sensor_type")

    @sensor_type.setter
    def sensor_type(self, value: Optional[pulumi.Input[Union[str, 'SensorType']]]):
        pulumi.set(self, "sensor_type", value)

    @property
    @pulumi.getter(name="tiAutomaticUpdates")
    def ti_automatic_updates(self) -> Optional[pulumi.Input[bool]]:
        """
        TI Automatic mode status of the IoT sensor
        """
        return pulumi.get(self, "ti_automatic_updates")

    @ti_automatic_updates.setter
    def ti_automatic_updates(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ti_automatic_updates", value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        Zone of the IoT sensor
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


class SiteSensor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 iot_defender_location: Optional[pulumi.Input[str]] = None,
                 sensor_name: Optional[pulumi.Input[str]] = None,
                 sensor_type: Optional[pulumi.Input[Union[str, 'SensorType']]] = None,
                 site_name: Optional[pulumi.Input[str]] = None,
                 ti_automatic_updates: Optional[pulumi.Input[bool]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        IoT sensor model
        API Version: 2021-09-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] iot_defender_location: Defender for IoT location
        :param pulumi.Input[str] sensor_name: Name of the IoT sensor
        :param pulumi.Input[Union[str, 'SensorType']] sensor_type: Type of sensor
        :param pulumi.Input[str] site_name: Site Name
        :param pulumi.Input[bool] ti_automatic_updates: TI Automatic mode status of the IoT sensor
        :param pulumi.Input[str] zone: Zone of the IoT sensor
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SiteSensorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        IoT sensor model
        API Version: 2021-09-01-preview.

        :param str resource_name: The name of the resource.
        :param SiteSensorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SiteSensorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 iot_defender_location: Optional[pulumi.Input[str]] = None,
                 sensor_name: Optional[pulumi.Input[str]] = None,
                 sensor_type: Optional[pulumi.Input[Union[str, 'SensorType']]] = None,
                 site_name: Optional[pulumi.Input[str]] = None,
                 ti_automatic_updates: Optional[pulumi.Input[bool]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
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
            __props__ = SiteSensorArgs.__new__(SiteSensorArgs)

            if iot_defender_location is None and not opts.urn:
                raise TypeError("Missing required property 'iot_defender_location'")
            __props__.__dict__["iot_defender_location"] = iot_defender_location
            __props__.__dict__["sensor_name"] = sensor_name
            __props__.__dict__["sensor_type"] = sensor_type
            if site_name is None and not opts.urn:
                raise TypeError("Missing required property 'site_name'")
            __props__.__dict__["site_name"] = site_name
            __props__.__dict__["ti_automatic_updates"] = ti_automatic_updates
            __props__.__dict__["zone"] = zone
            __props__.__dict__["connectivity_time"] = None
            __props__.__dict__["dynamic_learning"] = None
            __props__.__dict__["learning_mode"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["sensor_status"] = None
            __props__.__dict__["sensor_version"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["ti_status"] = None
            __props__.__dict__["ti_version"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:iotsecurity:SiteSensor"), pulumi.Alias(type_="azure-native:iotsecurity/v20210901preview:SiteSensor"), pulumi.Alias(type_="azure-nextgen:iotsecurity/v20210901preview:SiteSensor")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SiteSensor, __self__).__init__(
            'azure-native:iotsecurity:SiteSensor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SiteSensor':
        """
        Get an existing SiteSensor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SiteSensorArgs.__new__(SiteSensorArgs)

        __props__.__dict__["connectivity_time"] = None
        __props__.__dict__["dynamic_learning"] = None
        __props__.__dict__["learning_mode"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["sensor_status"] = None
        __props__.__dict__["sensor_type"] = None
        __props__.__dict__["sensor_version"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["ti_automatic_updates"] = None
        __props__.__dict__["ti_status"] = None
        __props__.__dict__["ti_version"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["zone"] = None
        return SiteSensor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectivityTime")
    def connectivity_time(self) -> pulumi.Output[str]:
        """
        Last connectivity time of the IoT sensor
        """
        return pulumi.get(self, "connectivity_time")

    @property
    @pulumi.getter(name="dynamicLearning")
    def dynamic_learning(self) -> pulumi.Output[bool]:
        """
        Dynamic mode status of the IoT sensor
        """
        return pulumi.get(self, "dynamic_learning")

    @property
    @pulumi.getter(name="learningMode")
    def learning_mode(self) -> pulumi.Output[bool]:
        """
        Learning mode status of the IoT sensor
        """
        return pulumi.get(self, "learning_mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sensorStatus")
    def sensor_status(self) -> pulumi.Output[str]:
        """
        Status of the IoT sensor
        """
        return pulumi.get(self, "sensor_status")

    @property
    @pulumi.getter(name="sensorType")
    def sensor_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of sensor
        """
        return pulumi.get(self, "sensor_type")

    @property
    @pulumi.getter(name="sensorVersion")
    def sensor_version(self) -> pulumi.Output[str]:
        """
        Version of the IoT sensor
        """
        return pulumi.get(self, "sensor_version")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="tiAutomaticUpdates")
    def ti_automatic_updates(self) -> pulumi.Output[Optional[bool]]:
        """
        TI Automatic mode status of the IoT sensor
        """
        return pulumi.get(self, "ti_automatic_updates")

    @property
    @pulumi.getter(name="tiStatus")
    def ti_status(self) -> pulumi.Output[str]:
        """
        TI Status of the IoT sensor
        """
        return pulumi.get(self, "ti_status")

    @property
    @pulumi.getter(name="tiVersion")
    def ti_version(self) -> pulumi.Output[str]:
        """
        TI Version of the IoT sensor
        """
        return pulumi.get(self, "ti_version")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[Optional[str]]:
        """
        Zone of the IoT sensor
        """
        return pulumi.get(self, "zone")

