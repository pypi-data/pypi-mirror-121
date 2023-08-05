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
    'GetMaintenanceConfigurationResult',
    'AwaitableGetMaintenanceConfigurationResult',
    'get_maintenance_configuration',
]

@pulumi.output_type
class GetMaintenanceConfigurationResult:
    """
    Maintenance configuration record type
    """
    def __init__(__self__, duration=None, expiration_date_time=None, extension_properties=None, id=None, install_patches=None, location=None, maintenance_scope=None, name=None, namespace=None, recur_every=None, start_date_time=None, system_data=None, tags=None, time_zone=None, type=None, visibility=None):
        if duration and not isinstance(duration, str):
            raise TypeError("Expected argument 'duration' to be a str")
        pulumi.set(__self__, "duration", duration)
        if expiration_date_time and not isinstance(expiration_date_time, str):
            raise TypeError("Expected argument 'expiration_date_time' to be a str")
        pulumi.set(__self__, "expiration_date_time", expiration_date_time)
        if extension_properties and not isinstance(extension_properties, dict):
            raise TypeError("Expected argument 'extension_properties' to be a dict")
        pulumi.set(__self__, "extension_properties", extension_properties)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if install_patches and not isinstance(install_patches, dict):
            raise TypeError("Expected argument 'install_patches' to be a dict")
        pulumi.set(__self__, "install_patches", install_patches)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if maintenance_scope and not isinstance(maintenance_scope, str):
            raise TypeError("Expected argument 'maintenance_scope' to be a str")
        pulumi.set(__self__, "maintenance_scope", maintenance_scope)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if namespace and not isinstance(namespace, str):
            raise TypeError("Expected argument 'namespace' to be a str")
        pulumi.set(__self__, "namespace", namespace)
        if recur_every and not isinstance(recur_every, str):
            raise TypeError("Expected argument 'recur_every' to be a str")
        pulumi.set(__self__, "recur_every", recur_every)
        if start_date_time and not isinstance(start_date_time, str):
            raise TypeError("Expected argument 'start_date_time' to be a str")
        pulumi.set(__self__, "start_date_time", start_date_time)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if time_zone and not isinstance(time_zone, str):
            raise TypeError("Expected argument 'time_zone' to be a str")
        pulumi.set(__self__, "time_zone", time_zone)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if visibility and not isinstance(visibility, str):
            raise TypeError("Expected argument 'visibility' to be a str")
        pulumi.set(__self__, "visibility", visibility)

    @property
    @pulumi.getter
    def duration(self) -> Optional[str]:
        """
        Duration of the maintenance window in HH:mm format. If not provided, default value will be used based on maintenance scope provided. Example: 05:00.
        """
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="expirationDateTime")
    def expiration_date_time(self) -> Optional[str]:
        """
        Effective expiration date of the maintenance window in YYYY-MM-DD hh:mm format. The window will be created in the time zone provided and adjusted to daylight savings according to that time zone. Expiration date must be set to a future date. If not provided, it will be set to the maximum datetime 9999-12-31 23:59:59.
        """
        return pulumi.get(self, "expiration_date_time")

    @property
    @pulumi.getter(name="extensionProperties")
    def extension_properties(self) -> Optional[Mapping[str, str]]:
        """
        Gets or sets extensionProperties of the maintenanceConfiguration
        """
        return pulumi.get(self, "extension_properties")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified identifier of the resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="installPatches")
    def install_patches(self) -> Optional['outputs.InputPatchConfigurationResponse']:
        """
        The input parameters to be passed to the patch run operation.
        """
        return pulumi.get(self, "install_patches")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Gets or sets location of the resource
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceScope")
    def maintenance_scope(self) -> Optional[str]:
        """
        Gets or sets maintenanceScope of the configuration
        """
        return pulumi.get(self, "maintenance_scope")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        Gets or sets namespace of the resource
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="recurEvery")
    def recur_every(self) -> Optional[str]:
        """
        Rate at which a Maintenance window is expected to recur. The rate can be expressed as daily, weekly, or monthly schedules. Daily schedule are formatted as recurEvery: [Frequency as integer]['Day(s)']. If no frequency is provided, the default frequency is 1. Daily schedule examples are recurEvery: Day, recurEvery: 3Days.  Weekly schedule are formatted as recurEvery: [Frequency as integer]['Week(s)'] [Optional comma separated list of weekdays Monday-Sunday]. Weekly schedule examples are recurEvery: 3Weeks, recurEvery: Week Saturday,Sunday. Monthly schedules are formatted as [Frequency as integer]['Month(s)'] [Comma separated list of month days] or [Frequency as integer]['Month(s)'] [Week of Month (First, Second, Third, Fourth, Last)] [Weekday Monday-Sunday] [Optional Offset(No. of days)]. Offset value must be between -6 to 6 inclusive. Monthly schedule examples are recurEvery: Month, recurEvery: 2Months, recurEvery: Month day23,day24, recurEvery: Month Last Sunday, recurEvery: Month Fourth Monday, recurEvery: Month Last Sunday Offset-3, recurEvery: Month Third Sunday Offset6.
        """
        return pulumi.get(self, "recur_every")

    @property
    @pulumi.getter(name="startDateTime")
    def start_date_time(self) -> Optional[str]:
        """
        Effective start date of the maintenance window in YYYY-MM-DD hh:mm format. The start date can be set to either the current date or future date. The window will be created in the time zone provided and adjusted to daylight savings according to that time zone.
        """
        return pulumi.get(self, "start_date_time")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Gets or sets tags of the resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> Optional[str]:
        """
        Name of the timezone. List of timezones can be obtained by executing [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell. Example: Pacific Standard Time, UTC, W. Europe Standard Time, Korea Standard Time, Cen. Australia Standard Time.
        """
        return pulumi.get(self, "time_zone")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def visibility(self) -> Optional[str]:
        """
        Gets or sets the visibility of the configuration. The default value is 'Custom'
        """
        return pulumi.get(self, "visibility")


class AwaitableGetMaintenanceConfigurationResult(GetMaintenanceConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMaintenanceConfigurationResult(
            duration=self.duration,
            expiration_date_time=self.expiration_date_time,
            extension_properties=self.extension_properties,
            id=self.id,
            install_patches=self.install_patches,
            location=self.location,
            maintenance_scope=self.maintenance_scope,
            name=self.name,
            namespace=self.namespace,
            recur_every=self.recur_every,
            start_date_time=self.start_date_time,
            system_data=self.system_data,
            tags=self.tags,
            time_zone=self.time_zone,
            type=self.type,
            visibility=self.visibility)


def get_maintenance_configuration(resource_group_name: Optional[str] = None,
                                  resource_name: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMaintenanceConfigurationResult:
    """
    Maintenance configuration record type


    :param str resource_group_name: Resource Group Name
    :param str resource_name: Maintenance Configuration Name
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:maintenance/v20210401preview:getMaintenanceConfiguration', __args__, opts=opts, typ=GetMaintenanceConfigurationResult).value

    return AwaitableGetMaintenanceConfigurationResult(
        duration=__ret__.duration,
        expiration_date_time=__ret__.expiration_date_time,
        extension_properties=__ret__.extension_properties,
        id=__ret__.id,
        install_patches=__ret__.install_patches,
        location=__ret__.location,
        maintenance_scope=__ret__.maintenance_scope,
        name=__ret__.name,
        namespace=__ret__.namespace,
        recur_every=__ret__.recur_every,
        start_date_time=__ret__.start_date_time,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        time_zone=__ret__.time_zone,
        type=__ret__.type,
        visibility=__ret__.visibility)
