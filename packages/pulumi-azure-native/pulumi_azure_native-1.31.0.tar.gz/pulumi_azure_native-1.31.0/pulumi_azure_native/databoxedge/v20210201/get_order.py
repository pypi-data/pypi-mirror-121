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
    'GetOrderResult',
    'AwaitableGetOrderResult',
    'get_order',
]

@pulumi.output_type
class GetOrderResult:
    """
    The order details.
    """
    def __init__(__self__, contact_information=None, current_status=None, delivery_tracking_info=None, id=None, name=None, order_history=None, return_tracking_info=None, serial_number=None, shipment_type=None, shipping_address=None, system_data=None, type=None):
        if contact_information and not isinstance(contact_information, dict):
            raise TypeError("Expected argument 'contact_information' to be a dict")
        pulumi.set(__self__, "contact_information", contact_information)
        if current_status and not isinstance(current_status, dict):
            raise TypeError("Expected argument 'current_status' to be a dict")
        pulumi.set(__self__, "current_status", current_status)
        if delivery_tracking_info and not isinstance(delivery_tracking_info, list):
            raise TypeError("Expected argument 'delivery_tracking_info' to be a list")
        pulumi.set(__self__, "delivery_tracking_info", delivery_tracking_info)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if order_history and not isinstance(order_history, list):
            raise TypeError("Expected argument 'order_history' to be a list")
        pulumi.set(__self__, "order_history", order_history)
        if return_tracking_info and not isinstance(return_tracking_info, list):
            raise TypeError("Expected argument 'return_tracking_info' to be a list")
        pulumi.set(__self__, "return_tracking_info", return_tracking_info)
        if serial_number and not isinstance(serial_number, str):
            raise TypeError("Expected argument 'serial_number' to be a str")
        pulumi.set(__self__, "serial_number", serial_number)
        if shipment_type and not isinstance(shipment_type, str):
            raise TypeError("Expected argument 'shipment_type' to be a str")
        pulumi.set(__self__, "shipment_type", shipment_type)
        if shipping_address and not isinstance(shipping_address, dict):
            raise TypeError("Expected argument 'shipping_address' to be a dict")
        pulumi.set(__self__, "shipping_address", shipping_address)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="contactInformation")
    def contact_information(self) -> 'outputs.ContactDetailsResponse':
        """
        The contact details.
        """
        return pulumi.get(self, "contact_information")

    @property
    @pulumi.getter(name="currentStatus")
    def current_status(self) -> 'outputs.OrderStatusResponse':
        """
        Current status of the order.
        """
        return pulumi.get(self, "current_status")

    @property
    @pulumi.getter(name="deliveryTrackingInfo")
    def delivery_tracking_info(self) -> Sequence['outputs.TrackingInfoResponse']:
        """
        Tracking information for the package delivered to the customer whether it has an original or a replacement device.
        """
        return pulumi.get(self, "delivery_tracking_info")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orderHistory")
    def order_history(self) -> Sequence['outputs.OrderStatusResponse']:
        """
        List of status changes in the order.
        """
        return pulumi.get(self, "order_history")

    @property
    @pulumi.getter(name="returnTrackingInfo")
    def return_tracking_info(self) -> Sequence['outputs.TrackingInfoResponse']:
        """
        Tracking information for the package returned from the customer whether it has an original or a replacement device.
        """
        return pulumi.get(self, "return_tracking_info")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> str:
        """
        Serial number of the device.
        """
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter(name="shipmentType")
    def shipment_type(self) -> Optional[str]:
        """
        ShipmentType of the order
        """
        return pulumi.get(self, "shipment_type")

    @property
    @pulumi.getter(name="shippingAddress")
    def shipping_address(self) -> Optional['outputs.AddressResponse']:
        """
        The shipping address.
        """
        return pulumi.get(self, "shipping_address")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Order configured on ASE resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")


class AwaitableGetOrderResult(GetOrderResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrderResult(
            contact_information=self.contact_information,
            current_status=self.current_status,
            delivery_tracking_info=self.delivery_tracking_info,
            id=self.id,
            name=self.name,
            order_history=self.order_history,
            return_tracking_info=self.return_tracking_info,
            serial_number=self.serial_number,
            shipment_type=self.shipment_type,
            shipping_address=self.shipping_address,
            system_data=self.system_data,
            type=self.type)


def get_order(device_name: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrderResult:
    """
    The order details.


    :param str device_name: The device name.
    :param str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['deviceName'] = device_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:databoxedge/v20210201:getOrder', __args__, opts=opts, typ=GetOrderResult).value

    return AwaitableGetOrderResult(
        contact_information=__ret__.contact_information,
        current_status=__ret__.current_status,
        delivery_tracking_info=__ret__.delivery_tracking_info,
        id=__ret__.id,
        name=__ret__.name,
        order_history=__ret__.order_history,
        return_tracking_info=__ret__.return_tracking_info,
        serial_number=__ret__.serial_number,
        shipment_type=__ret__.shipment_type,
        shipping_address=__ret__.shipping_address,
        system_data=__ret__.system_data,
        type=__ret__.type)
