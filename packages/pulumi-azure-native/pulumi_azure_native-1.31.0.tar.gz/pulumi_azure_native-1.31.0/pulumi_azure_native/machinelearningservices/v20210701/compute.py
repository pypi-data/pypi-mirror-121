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
from ._inputs import *

__all__ = ['ComputeArgs', 'Compute']

@pulumi.input_type
class ComputeArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 compute_name: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['IdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union['AKSArgs', 'AmlComputeArgs', 'ComputeInstanceArgs', 'DataFactoryArgs', 'DataLakeAnalyticsArgs', 'DatabricksArgs', 'HDInsightArgs', 'KubernetesArgs', 'SynapseSparkArgs', 'VirtualMachineArgs']]] = None,
                 sku: Optional[pulumi.Input['SkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Compute resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        :param pulumi.Input[str] compute_name: Name of the Azure Machine Learning compute.
        :param pulumi.Input['IdentityArgs'] identity: The identity of the resource.
        :param pulumi.Input[str] location: Specifies the location of the resource.
        :param pulumi.Input[Union['AKSArgs', 'AmlComputeArgs', 'ComputeInstanceArgs', 'DataFactoryArgs', 'DataLakeAnalyticsArgs', 'DatabricksArgs', 'HDInsightArgs', 'KubernetesArgs', 'SynapseSparkArgs', 'VirtualMachineArgs']] properties: Compute properties
        :param pulumi.Input['SkuArgs'] sku: The sku of the workspace.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Contains resource tags defined as key/value pairs.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if compute_name is not None:
            pulumi.set(__self__, "compute_name", compute_name)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        Name of Azure Machine Learning workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter(name="computeName")
    def compute_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Azure Machine Learning compute.
        """
        return pulumi.get(self, "compute_name")

    @compute_name.setter
    def compute_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_name", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['IdentityArgs']]:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['IdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Union['AKSArgs', 'AmlComputeArgs', 'ComputeInstanceArgs', 'DataFactoryArgs', 'DataLakeAnalyticsArgs', 'DatabricksArgs', 'HDInsightArgs', 'KubernetesArgs', 'SynapseSparkArgs', 'VirtualMachineArgs']]]:
        """
        Compute properties
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Union['AKSArgs', 'AmlComputeArgs', 'ComputeInstanceArgs', 'DataFactoryArgs', 'DataLakeAnalyticsArgs', 'DatabricksArgs', 'HDInsightArgs', 'KubernetesArgs', 'SynapseSparkArgs', 'VirtualMachineArgs']]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        The sku of the workspace.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Compute(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compute_name: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AKSArgs'], pulumi.InputType['AmlComputeArgs'], pulumi.InputType['ComputeInstanceArgs'], pulumi.InputType['DataFactoryArgs'], pulumi.InputType['DataLakeAnalyticsArgs'], pulumi.InputType['DatabricksArgs'], pulumi.InputType['HDInsightArgs'], pulumi.InputType['KubernetesArgs'], pulumi.InputType['SynapseSparkArgs'], pulumi.InputType['VirtualMachineArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Machine Learning compute object wrapped into ARM resource envelope.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compute_name: Name of the Azure Machine Learning compute.
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: The identity of the resource.
        :param pulumi.Input[str] location: Specifies the location of the resource.
        :param pulumi.Input[Union[pulumi.InputType['AKSArgs'], pulumi.InputType['AmlComputeArgs'], pulumi.InputType['ComputeInstanceArgs'], pulumi.InputType['DataFactoryArgs'], pulumi.InputType['DataLakeAnalyticsArgs'], pulumi.InputType['DatabricksArgs'], pulumi.InputType['HDInsightArgs'], pulumi.InputType['KubernetesArgs'], pulumi.InputType['SynapseSparkArgs'], pulumi.InputType['VirtualMachineArgs']]] properties: Compute properties
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku of the workspace.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Contains resource tags defined as key/value pairs.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ComputeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Machine Learning compute object wrapped into ARM resource envelope.

        :param str resource_name: The name of the resource.
        :param ComputeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ComputeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compute_name: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AKSArgs'], pulumi.InputType['AmlComputeArgs'], pulumi.InputType['ComputeInstanceArgs'], pulumi.InputType['DataFactoryArgs'], pulumi.InputType['DataLakeAnalyticsArgs'], pulumi.InputType['DatabricksArgs'], pulumi.InputType['HDInsightArgs'], pulumi.InputType['KubernetesArgs'], pulumi.InputType['SynapseSparkArgs'], pulumi.InputType['VirtualMachineArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ComputeArgs.__new__(ComputeArgs)

            __props__.__dict__["compute_name"] = compute_name
            __props__.__dict__["identity"] = identity
            __props__.__dict__["location"] = location
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20210701:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20180301preview:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20180301preview:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20181119:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20181119:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20190501:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20190501:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20190601:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20190601:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20191101:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20191101:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200101:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200101:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200218preview:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200218preview:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200301:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200301:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200401:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200401:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200501preview:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200501preview:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200515preview:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200515preview:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200601:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200601:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200801:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200801:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20200901preview:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20200901preview:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20210101:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20210101:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20210301preview:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20210301preview:Compute"), pulumi.Alias(type_="azure-native:machinelearningservices/v20210401:Compute"), pulumi.Alias(type_="azure-nextgen:machinelearningservices/v20210401:Compute")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Compute, __self__).__init__(
            'azure-native:machinelearningservices/v20210701:Compute',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Compute':
        """
        Get an existing Compute resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ComputeArgs.__new__(ComputeArgs)

        __props__.__dict__["identity"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Compute(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Any]:
        """
        Compute properties
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of the workspace.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        System data
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

