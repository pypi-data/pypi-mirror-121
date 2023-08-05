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
    'EventHubEventSubscriptionDestinationResponse',
    'EventSubscriptionFilterResponse',
    'HybridConnectionEventSubscriptionDestinationResponse',
    'RetryPolicyResponse',
    'StorageBlobDeadLetterDestinationResponse',
    'StorageQueueEventSubscriptionDestinationResponse',
    'WebHookEventSubscriptionDestinationResponse',
]

@pulumi.output_type
class EventHubEventSubscriptionDestinationResponse(dict):
    """
    Information about the event hub destination for an event subscription
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointType":
            suggest = "endpoint_type"
        elif key == "resourceId":
            suggest = "resource_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventHubEventSubscriptionDestinationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventHubEventSubscriptionDestinationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventHubEventSubscriptionDestinationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint_type: str,
                 resource_id: Optional[str] = None):
        """
        Information about the event hub destination for an event subscription
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'EventHub'.
        :param str resource_id: The Azure Resource Id that represents the endpoint of an Event Hub destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_type", 'EventHub')
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'EventHub'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource Id that represents the endpoint of an Event Hub destination of an event subscription.
        """
        return pulumi.get(self, "resource_id")


@pulumi.output_type
class EventSubscriptionFilterResponse(dict):
    """
    Filter for the Event Subscription
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "includedEventTypes":
            suggest = "included_event_types"
        elif key == "isSubjectCaseSensitive":
            suggest = "is_subject_case_sensitive"
        elif key == "subjectBeginsWith":
            suggest = "subject_begins_with"
        elif key == "subjectEndsWith":
            suggest = "subject_ends_with"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventSubscriptionFilterResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventSubscriptionFilterResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventSubscriptionFilterResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 included_event_types: Optional[Sequence[str]] = None,
                 is_subject_case_sensitive: Optional[bool] = None,
                 subject_begins_with: Optional[str] = None,
                 subject_ends_with: Optional[str] = None):
        """
        Filter for the Event Subscription
        :param Sequence[str] included_event_types: A list of applicable event types that need to be part of the event subscription. 
               If it is desired to subscribe to all event types, the string "all" needs to be specified as an element in this list.
        :param bool is_subject_case_sensitive: Specifies if the SubjectBeginsWith and SubjectEndsWith properties of the filter 
               should be compared in a case sensitive manner.
        :param str subject_begins_with: An optional string to filter events for an event subscription based on a resource path prefix.
               The format of this depends on the publisher of the events. 
               Wildcard characters are not supported in this path.
        :param str subject_ends_with: An optional string to filter events for an event subscription based on a resource path suffix.
               Wildcard characters are not supported in this path.
        """
        if included_event_types is not None:
            pulumi.set(__self__, "included_event_types", included_event_types)
        if is_subject_case_sensitive is None:
            is_subject_case_sensitive = False
        if is_subject_case_sensitive is not None:
            pulumi.set(__self__, "is_subject_case_sensitive", is_subject_case_sensitive)
        if subject_begins_with is not None:
            pulumi.set(__self__, "subject_begins_with", subject_begins_with)
        if subject_ends_with is not None:
            pulumi.set(__self__, "subject_ends_with", subject_ends_with)

    @property
    @pulumi.getter(name="includedEventTypes")
    def included_event_types(self) -> Optional[Sequence[str]]:
        """
        A list of applicable event types that need to be part of the event subscription. 
        If it is desired to subscribe to all event types, the string "all" needs to be specified as an element in this list.
        """
        return pulumi.get(self, "included_event_types")

    @property
    @pulumi.getter(name="isSubjectCaseSensitive")
    def is_subject_case_sensitive(self) -> Optional[bool]:
        """
        Specifies if the SubjectBeginsWith and SubjectEndsWith properties of the filter 
        should be compared in a case sensitive manner.
        """
        return pulumi.get(self, "is_subject_case_sensitive")

    @property
    @pulumi.getter(name="subjectBeginsWith")
    def subject_begins_with(self) -> Optional[str]:
        """
        An optional string to filter events for an event subscription based on a resource path prefix.
        The format of this depends on the publisher of the events. 
        Wildcard characters are not supported in this path.
        """
        return pulumi.get(self, "subject_begins_with")

    @property
    @pulumi.getter(name="subjectEndsWith")
    def subject_ends_with(self) -> Optional[str]:
        """
        An optional string to filter events for an event subscription based on a resource path suffix.
        Wildcard characters are not supported in this path.
        """
        return pulumi.get(self, "subject_ends_with")


@pulumi.output_type
class HybridConnectionEventSubscriptionDestinationResponse(dict):
    """
    Information about the HybridConnection destination for an event subscription.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointType":
            suggest = "endpoint_type"
        elif key == "resourceId":
            suggest = "resource_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in HybridConnectionEventSubscriptionDestinationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        HybridConnectionEventSubscriptionDestinationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        HybridConnectionEventSubscriptionDestinationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint_type: str,
                 resource_id: Optional[str] = None):
        """
        Information about the HybridConnection destination for an event subscription.
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'HybridConnection'.
        :param str resource_id: The Azure Resource ID of an hybrid connection that is the destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_type", 'HybridConnection')
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'HybridConnection'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource ID of an hybrid connection that is the destination of an event subscription.
        """
        return pulumi.get(self, "resource_id")


@pulumi.output_type
class RetryPolicyResponse(dict):
    """
    Information about the retry policy for an event subscription
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "eventTimeToLiveInMinutes":
            suggest = "event_time_to_live_in_minutes"
        elif key == "maxDeliveryAttempts":
            suggest = "max_delivery_attempts"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RetryPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RetryPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RetryPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 event_time_to_live_in_minutes: Optional[int] = None,
                 max_delivery_attempts: Optional[int] = None):
        """
        Information about the retry policy for an event subscription
        :param int event_time_to_live_in_minutes: Time To Live (in minutes) for events.
        :param int max_delivery_attempts: Maximum number of delivery retry attempts for events.
        """
        if event_time_to_live_in_minutes is not None:
            pulumi.set(__self__, "event_time_to_live_in_minutes", event_time_to_live_in_minutes)
        if max_delivery_attempts is not None:
            pulumi.set(__self__, "max_delivery_attempts", max_delivery_attempts)

    @property
    @pulumi.getter(name="eventTimeToLiveInMinutes")
    def event_time_to_live_in_minutes(self) -> Optional[int]:
        """
        Time To Live (in minutes) for events.
        """
        return pulumi.get(self, "event_time_to_live_in_minutes")

    @property
    @pulumi.getter(name="maxDeliveryAttempts")
    def max_delivery_attempts(self) -> Optional[int]:
        """
        Maximum number of delivery retry attempts for events.
        """
        return pulumi.get(self, "max_delivery_attempts")


@pulumi.output_type
class StorageBlobDeadLetterDestinationResponse(dict):
    """
    Information about the storage blob based dead letter destination.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointType":
            suggest = "endpoint_type"
        elif key == "blobContainerName":
            suggest = "blob_container_name"
        elif key == "resourceId":
            suggest = "resource_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StorageBlobDeadLetterDestinationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StorageBlobDeadLetterDestinationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StorageBlobDeadLetterDestinationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint_type: str,
                 blob_container_name: Optional[str] = None,
                 resource_id: Optional[str] = None):
        """
        Information about the storage blob based dead letter destination.
        :param str endpoint_type: Type of the endpoint for the dead letter destination
               Expected value is 'StorageBlob'.
        :param str blob_container_name: The name of the Storage blob container that is the destination of the deadletter events
        :param str resource_id: The Azure Resource ID of the storage account that is the destination of the deadletter events. For example: /subscriptions/{AzureSubscriptionId}/resourceGroups/{ResourceGroupName}/providers/microsoft.Storage/storageAccounts/{StorageAccountName}
        """
        pulumi.set(__self__, "endpoint_type", 'StorageBlob')
        if blob_container_name is not None:
            pulumi.set(__self__, "blob_container_name", blob_container_name)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the dead letter destination
        Expected value is 'StorageBlob'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="blobContainerName")
    def blob_container_name(self) -> Optional[str]:
        """
        The name of the Storage blob container that is the destination of the deadletter events
        """
        return pulumi.get(self, "blob_container_name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource ID of the storage account that is the destination of the deadletter events. For example: /subscriptions/{AzureSubscriptionId}/resourceGroups/{ResourceGroupName}/providers/microsoft.Storage/storageAccounts/{StorageAccountName}
        """
        return pulumi.get(self, "resource_id")


@pulumi.output_type
class StorageQueueEventSubscriptionDestinationResponse(dict):
    """
    Information about the storage queue destination for an event subscription.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointType":
            suggest = "endpoint_type"
        elif key == "queueName":
            suggest = "queue_name"
        elif key == "resourceId":
            suggest = "resource_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StorageQueueEventSubscriptionDestinationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StorageQueueEventSubscriptionDestinationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StorageQueueEventSubscriptionDestinationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint_type: str,
                 queue_name: Optional[str] = None,
                 resource_id: Optional[str] = None):
        """
        Information about the storage queue destination for an event subscription.
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'StorageQueue'.
        :param str queue_name: The name of the Storage queue under a storage account that is the destination of an event subscription.
        :param str resource_id: The Azure Resource ID of the storage account that contains the queue that is the destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_type", 'StorageQueue')
        if queue_name is not None:
            pulumi.set(__self__, "queue_name", queue_name)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'StorageQueue'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="queueName")
    def queue_name(self) -> Optional[str]:
        """
        The name of the Storage queue under a storage account that is the destination of an event subscription.
        """
        return pulumi.get(self, "queue_name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource ID of the storage account that contains the queue that is the destination of an event subscription.
        """
        return pulumi.get(self, "resource_id")


@pulumi.output_type
class WebHookEventSubscriptionDestinationResponse(dict):
    """
    Information about the webhook destination for an event subscription
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointBaseUrl":
            suggest = "endpoint_base_url"
        elif key == "endpointType":
            suggest = "endpoint_type"
        elif key == "endpointUrl":
            suggest = "endpoint_url"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebHookEventSubscriptionDestinationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebHookEventSubscriptionDestinationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WebHookEventSubscriptionDestinationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint_base_url: str,
                 endpoint_type: str,
                 endpoint_url: Optional[str] = None):
        """
        Information about the webhook destination for an event subscription
        :param str endpoint_base_url: The base URL that represents the endpoint of the destination of an event subscription.
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'WebHook'.
        :param str endpoint_url: The URL that represents the endpoint of the destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_base_url", endpoint_base_url)
        pulumi.set(__self__, "endpoint_type", 'WebHook')
        if endpoint_url is not None:
            pulumi.set(__self__, "endpoint_url", endpoint_url)

    @property
    @pulumi.getter(name="endpointBaseUrl")
    def endpoint_base_url(self) -> str:
        """
        The base URL that represents the endpoint of the destination of an event subscription.
        """
        return pulumi.get(self, "endpoint_base_url")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'WebHook'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="endpointUrl")
    def endpoint_url(self) -> Optional[str]:
        """
        The URL that represents the endpoint of the destination of an event subscription.
        """
        return pulumi.get(self, "endpoint_url")


