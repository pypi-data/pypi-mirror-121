# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'AccessModeSettingsExclusionArgs',
    'AccessModeSettingsArgs',
    'PrivateLinkServiceConnectionStateArgs',
]

@pulumi.input_type
class AccessModeSettingsExclusionArgs:
    def __init__(__self__, *,
                 ingestion_access_mode: Optional[pulumi.Input[Union[str, 'AccessMode']]] = None,
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                 query_access_mode: Optional[pulumi.Input[Union[str, 'AccessMode']]] = None):
        """
        Properties that define the scope private link mode settings exclusion item. This setting applies to a specific private endpoint connection and overrides the default settings for that private endpoint connection.
        :param pulumi.Input[Union[str, 'AccessMode']] ingestion_access_mode: Specifies the access mode of ingestion through the specified private endpoint connection in the exclusion.
        :param pulumi.Input[str] private_endpoint_connection_name: The private endpoint connection name associated to the private endpoint on which we want to apply the specific access mode settings.
        :param pulumi.Input[Union[str, 'AccessMode']] query_access_mode: Specifies the access mode of queries through the specified private endpoint connection in the exclusion.
        """
        if ingestion_access_mode is not None:
            pulumi.set(__self__, "ingestion_access_mode", ingestion_access_mode)
        if private_endpoint_connection_name is not None:
            pulumi.set(__self__, "private_endpoint_connection_name", private_endpoint_connection_name)
        if query_access_mode is not None:
            pulumi.set(__self__, "query_access_mode", query_access_mode)

    @property
    @pulumi.getter(name="ingestionAccessMode")
    def ingestion_access_mode(self) -> Optional[pulumi.Input[Union[str, 'AccessMode']]]:
        """
        Specifies the access mode of ingestion through the specified private endpoint connection in the exclusion.
        """
        return pulumi.get(self, "ingestion_access_mode")

    @ingestion_access_mode.setter
    def ingestion_access_mode(self, value: Optional[pulumi.Input[Union[str, 'AccessMode']]]):
        pulumi.set(self, "ingestion_access_mode", value)

    @property
    @pulumi.getter(name="privateEndpointConnectionName")
    def private_endpoint_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The private endpoint connection name associated to the private endpoint on which we want to apply the specific access mode settings.
        """
        return pulumi.get(self, "private_endpoint_connection_name")

    @private_endpoint_connection_name.setter
    def private_endpoint_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_endpoint_connection_name", value)

    @property
    @pulumi.getter(name="queryAccessMode")
    def query_access_mode(self) -> Optional[pulumi.Input[Union[str, 'AccessMode']]]:
        """
        Specifies the access mode of queries through the specified private endpoint connection in the exclusion.
        """
        return pulumi.get(self, "query_access_mode")

    @query_access_mode.setter
    def query_access_mode(self, value: Optional[pulumi.Input[Union[str, 'AccessMode']]]):
        pulumi.set(self, "query_access_mode", value)


@pulumi.input_type
class AccessModeSettingsArgs:
    def __init__(__self__, *,
                 ingestion_access_mode: pulumi.Input[Union[str, 'AccessMode']],
                 query_access_mode: pulumi.Input[Union[str, 'AccessMode']],
                 exclusions: Optional[pulumi.Input[Sequence[pulumi.Input['AccessModeSettingsExclusionArgs']]]] = None):
        """
        Properties that define the scope private link mode settings.
        :param pulumi.Input[Union[str, 'AccessMode']] ingestion_access_mode: Specifies the default access mode of ingestion through associated private endpoints in scope. If not specified default value is 'Open'. You can override this default setting for a specific private endpoint connection by adding an exclusion in the 'exclusions' array.
        :param pulumi.Input[Union[str, 'AccessMode']] query_access_mode: Specifies the default access mode of queries through associated private endpoints in scope. If not specified default value is 'Open'. You can override this default setting for a specific private endpoint connection by adding an exclusion in the 'exclusions' array.
        :param pulumi.Input[Sequence[pulumi.Input['AccessModeSettingsExclusionArgs']]] exclusions: List of exclusions that override the default access mode settings for specific private endpoint connections.
        """
        pulumi.set(__self__, "ingestion_access_mode", ingestion_access_mode)
        pulumi.set(__self__, "query_access_mode", query_access_mode)
        if exclusions is not None:
            pulumi.set(__self__, "exclusions", exclusions)

    @property
    @pulumi.getter(name="ingestionAccessMode")
    def ingestion_access_mode(self) -> pulumi.Input[Union[str, 'AccessMode']]:
        """
        Specifies the default access mode of ingestion through associated private endpoints in scope. If not specified default value is 'Open'. You can override this default setting for a specific private endpoint connection by adding an exclusion in the 'exclusions' array.
        """
        return pulumi.get(self, "ingestion_access_mode")

    @ingestion_access_mode.setter
    def ingestion_access_mode(self, value: pulumi.Input[Union[str, 'AccessMode']]):
        pulumi.set(self, "ingestion_access_mode", value)

    @property
    @pulumi.getter(name="queryAccessMode")
    def query_access_mode(self) -> pulumi.Input[Union[str, 'AccessMode']]:
        """
        Specifies the default access mode of queries through associated private endpoints in scope. If not specified default value is 'Open'. You can override this default setting for a specific private endpoint connection by adding an exclusion in the 'exclusions' array.
        """
        return pulumi.get(self, "query_access_mode")

    @query_access_mode.setter
    def query_access_mode(self, value: pulumi.Input[Union[str, 'AccessMode']]):
        pulumi.set(self, "query_access_mode", value)

    @property
    @pulumi.getter
    def exclusions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccessModeSettingsExclusionArgs']]]]:
        """
        List of exclusions that override the default access mode settings for specific private endpoint connections.
        """
        return pulumi.get(self, "exclusions")

    @exclusions.setter
    def exclusions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccessModeSettingsExclusionArgs']]]]):
        pulumi.set(self, "exclusions", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


