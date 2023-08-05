# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = ['CertificateArgs', 'Certificate']

@pulumi.input_type
class CertificateArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 data: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input['CertificateFormat']] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 thumbprint_algorithm: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Certificate resource.
        :param pulumi.Input[str] account_name: The name of the Batch account.
        :param pulumi.Input[str] data: The maximum size is 10KB.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the Batch account.
        :param pulumi.Input[str] certificate_name: The identifier for the certificate. This must be made up of algorithm and thumbprint separated by a dash, and must match the certificate data in the request. For example SHA1-a3d1c5.
        :param pulumi.Input['CertificateFormat'] format: The format of the certificate - either Pfx or Cer. If omitted, the default is Pfx.
        :param pulumi.Input[str] password: This must not be specified if the certificate format is Cer.
        :param pulumi.Input[str] thumbprint: This must match the thumbprint from the name.
        :param pulumi.Input[str] thumbprint_algorithm: This must match the first portion of the certificate name. Currently required to be 'SHA1'.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "data", data)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if certificate_name is not None:
            pulumi.set(__self__, "certificate_name", certificate_name)
        if format is not None:
            pulumi.set(__self__, "format", format)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)
        if thumbprint_algorithm is not None:
            pulumi.set(__self__, "thumbprint_algorithm", thumbprint_algorithm)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the Batch account.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def data(self) -> pulumi.Input[str]:
        """
        The maximum size is 10KB.
        """
        return pulumi.get(self, "data")

    @data.setter
    def data(self, value: pulumi.Input[str]):
        pulumi.set(self, "data", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the Batch account.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="certificateName")
    def certificate_name(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier for the certificate. This must be made up of algorithm and thumbprint separated by a dash, and must match the certificate data in the request. For example SHA1-a3d1c5.
        """
        return pulumi.get(self, "certificate_name")

    @certificate_name.setter
    def certificate_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_name", value)

    @property
    @pulumi.getter
    def format(self) -> Optional[pulumi.Input['CertificateFormat']]:
        """
        The format of the certificate - either Pfx or Cer. If omitted, the default is Pfx.
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: Optional[pulumi.Input['CertificateFormat']]):
        pulumi.set(self, "format", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        This must not be specified if the certificate format is Cer.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        This must match the thumbprint from the name.
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint", value)

    @property
    @pulumi.getter(name="thumbprintAlgorithm")
    def thumbprint_algorithm(self) -> Optional[pulumi.Input[str]]:
        """
        This must match the first portion of the certificate name. Currently required to be 'SHA1'.
        """
        return pulumi.get(self, "thumbprint_algorithm")

    @thumbprint_algorithm.setter
    def thumbprint_algorithm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint_algorithm", value)


class Certificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input['CertificateFormat']] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 thumbprint_algorithm: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Contains information about a certificate.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Batch account.
        :param pulumi.Input[str] certificate_name: The identifier for the certificate. This must be made up of algorithm and thumbprint separated by a dash, and must match the certificate data in the request. For example SHA1-a3d1c5.
        :param pulumi.Input[str] data: The maximum size is 10KB.
        :param pulumi.Input['CertificateFormat'] format: The format of the certificate - either Pfx or Cer. If omitted, the default is Pfx.
        :param pulumi.Input[str] password: This must not be specified if the certificate format is Cer.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the Batch account.
        :param pulumi.Input[str] thumbprint: This must match the thumbprint from the name.
        :param pulumi.Input[str] thumbprint_algorithm: This must match the first portion of the certificate name. Currently required to be 'SHA1'.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Contains information about a certificate.

        :param str resource_name: The name of the resource.
        :param CertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input['CertificateFormat']] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 thumbprint_algorithm: Optional[pulumi.Input[str]] = None,
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
            __props__ = CertificateArgs.__new__(CertificateArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["certificate_name"] = certificate_name
            if data is None and not opts.urn:
                raise TypeError("Missing required property 'data'")
            __props__.__dict__["data"] = data
            __props__.__dict__["format"] = format
            __props__.__dict__["password"] = password
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["thumbprint"] = thumbprint
            __props__.__dict__["thumbprint_algorithm"] = thumbprint_algorithm
            __props__.__dict__["delete_certificate_error"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["previous_provisioning_state"] = None
            __props__.__dict__["previous_provisioning_state_transition_time"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["provisioning_state_transition_time"] = None
            __props__.__dict__["public_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:batch/v20210601:Certificate"), pulumi.Alias(type_="azure-native:batch:Certificate"), pulumi.Alias(type_="azure-nextgen:batch:Certificate"), pulumi.Alias(type_="azure-native:batch/v20170901:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20170901:Certificate"), pulumi.Alias(type_="azure-native:batch/v20181201:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20181201:Certificate"), pulumi.Alias(type_="azure-native:batch/v20190401:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20190401:Certificate"), pulumi.Alias(type_="azure-native:batch/v20190801:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20190801:Certificate"), pulumi.Alias(type_="azure-native:batch/v20200301:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20200301:Certificate"), pulumi.Alias(type_="azure-native:batch/v20200501:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20200501:Certificate"), pulumi.Alias(type_="azure-native:batch/v20200901:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20200901:Certificate"), pulumi.Alias(type_="azure-native:batch/v20210101:Certificate"), pulumi.Alias(type_="azure-nextgen:batch/v20210101:Certificate")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Certificate, __self__).__init__(
            'azure-native:batch/v20210601:Certificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Certificate':
        """
        Get an existing Certificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CertificateArgs.__new__(CertificateArgs)

        __props__.__dict__["delete_certificate_error"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["format"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["previous_provisioning_state"] = None
        __props__.__dict__["previous_provisioning_state_transition_time"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["provisioning_state_transition_time"] = None
        __props__.__dict__["public_data"] = None
        __props__.__dict__["thumbprint"] = None
        __props__.__dict__["thumbprint_algorithm"] = None
        __props__.__dict__["type"] = None
        return Certificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deleteCertificateError")
    def delete_certificate_error(self) -> pulumi.Output['outputs.DeleteCertificateErrorResponse']:
        """
        This is only returned when the certificate provisioningState is 'Failed'.
        """
        return pulumi.get(self, "delete_certificate_error")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The ETag of the resource, used for concurrency statements.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def format(self) -> pulumi.Output[Optional[str]]:
        """
        The format of the certificate - either Pfx or Cer. If omitted, the default is Pfx.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="previousProvisioningState")
    def previous_provisioning_state(self) -> pulumi.Output[str]:
        """
        The previous provisioned state of the resource
        """
        return pulumi.get(self, "previous_provisioning_state")

    @property
    @pulumi.getter(name="previousProvisioningStateTransitionTime")
    def previous_provisioning_state_transition_time(self) -> pulumi.Output[str]:
        return pulumi.get(self, "previous_provisioning_state_transition_time")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="provisioningStateTransitionTime")
    def provisioning_state_transition_time(self) -> pulumi.Output[str]:
        return pulumi.get(self, "provisioning_state_transition_time")

    @property
    @pulumi.getter(name="publicData")
    def public_data(self) -> pulumi.Output[str]:
        """
        The public key of the certificate.
        """
        return pulumi.get(self, "public_data")

    @property
    @pulumi.getter
    def thumbprint(self) -> pulumi.Output[Optional[str]]:
        """
        This must match the thumbprint from the name.
        """
        return pulumi.get(self, "thumbprint")

    @property
    @pulumi.getter(name="thumbprintAlgorithm")
    def thumbprint_algorithm(self) -> pulumi.Output[Optional[str]]:
        """
        This must match the first portion of the certificate name. Currently required to be 'SHA1'.
        """
        return pulumi.get(self, "thumbprint_algorithm")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

