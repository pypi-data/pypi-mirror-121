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

__all__ = ['GalleryImageArgs', 'GalleryImage']

@pulumi.input_type
class GalleryImageArgs:
    def __init__(__self__, *,
                 gallery_name: pulumi.Input[str],
                 identifier: pulumi.Input['GalleryImageIdentifierArgs'],
                 os_state: pulumi.Input['OperatingSystemStateTypes'],
                 os_type: pulumi.Input['OperatingSystemTypes'],
                 resource_group_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 disallowed: Optional[pulumi.Input['DisallowedArgs']] = None,
                 end_of_life_date: Optional[pulumi.Input[str]] = None,
                 eula: Optional[pulumi.Input[str]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input['GalleryImageFeatureArgs']]]] = None,
                 gallery_image_name: Optional[pulumi.Input[str]] = None,
                 hyper_v_generation: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 privacy_statement_uri: Optional[pulumi.Input[str]] = None,
                 purchase_plan: Optional[pulumi.Input['ImagePurchasePlanArgs']] = None,
                 recommended: Optional[pulumi.Input['RecommendedMachineConfigurationArgs']] = None,
                 release_note_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a GalleryImage resource.
        :param pulumi.Input[str] gallery_name: The name of the Shared Image Gallery in which the Image Definition is to be created.
        :param pulumi.Input['GalleryImageIdentifierArgs'] identifier: This is the gallery image definition identifier.
        :param pulumi.Input['OperatingSystemStateTypes'] os_state: This property allows the user to specify whether the virtual machines created under this image are 'Generalized' or 'Specialized'.
        :param pulumi.Input['OperatingSystemTypes'] os_type: This property allows you to specify the type of the OS that is included in the disk when creating a VM from a managed image. <br><br> Possible values are: <br><br> **Windows** <br><br> **Linux**
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] description: The description of this gallery image definition resource. This property is updatable.
        :param pulumi.Input['DisallowedArgs'] disallowed: Describes the disallowed disk types.
        :param pulumi.Input[str] end_of_life_date: The end of life date of the gallery image definition. This property can be used for decommissioning purposes. This property is updatable.
        :param pulumi.Input[str] eula: The Eula agreement for the gallery image definition.
        :param pulumi.Input[Sequence[pulumi.Input['GalleryImageFeatureArgs']]] features: A list of gallery image features.
        :param pulumi.Input[str] gallery_image_name: The name of the gallery image definition to be created or updated. The allowed characters are alphabets and numbers with dots, dashes, and periods allowed in the middle. The maximum length is 80 characters.
        :param pulumi.Input[Union[str, 'HyperVGeneration']] hyper_v_generation: The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] privacy_statement_uri: The privacy statement uri.
        :param pulumi.Input['ImagePurchasePlanArgs'] purchase_plan: Describes the gallery image definition purchase plan. This is used by marketplace images.
        :param pulumi.Input['RecommendedMachineConfigurationArgs'] recommended: The properties describe the recommended machine configuration for this Image Definition. These properties are updatable.
        :param pulumi.Input[str] release_note_uri: The release note uri.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, "gallery_name", gallery_name)
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "os_state", os_state)
        pulumi.set(__self__, "os_type", os_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disallowed is not None:
            pulumi.set(__self__, "disallowed", disallowed)
        if end_of_life_date is not None:
            pulumi.set(__self__, "end_of_life_date", end_of_life_date)
        if eula is not None:
            pulumi.set(__self__, "eula", eula)
        if features is not None:
            pulumi.set(__self__, "features", features)
        if gallery_image_name is not None:
            pulumi.set(__self__, "gallery_image_name", gallery_image_name)
        if hyper_v_generation is not None:
            pulumi.set(__self__, "hyper_v_generation", hyper_v_generation)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if privacy_statement_uri is not None:
            pulumi.set(__self__, "privacy_statement_uri", privacy_statement_uri)
        if purchase_plan is not None:
            pulumi.set(__self__, "purchase_plan", purchase_plan)
        if recommended is not None:
            pulumi.set(__self__, "recommended", recommended)
        if release_note_uri is not None:
            pulumi.set(__self__, "release_note_uri", release_note_uri)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="galleryName")
    def gallery_name(self) -> pulumi.Input[str]:
        """
        The name of the Shared Image Gallery in which the Image Definition is to be created.
        """
        return pulumi.get(self, "gallery_name")

    @gallery_name.setter
    def gallery_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "gallery_name", value)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input['GalleryImageIdentifierArgs']:
        """
        This is the gallery image definition identifier.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input['GalleryImageIdentifierArgs']):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter(name="osState")
    def os_state(self) -> pulumi.Input['OperatingSystemStateTypes']:
        """
        This property allows the user to specify whether the virtual machines created under this image are 'Generalized' or 'Specialized'.
        """
        return pulumi.get(self, "os_state")

    @os_state.setter
    def os_state(self, value: pulumi.Input['OperatingSystemStateTypes']):
        pulumi.set(self, "os_state", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Input['OperatingSystemTypes']:
        """
        This property allows you to specify the type of the OS that is included in the disk when creating a VM from a managed image. <br><br> Possible values are: <br><br> **Windows** <br><br> **Linux**
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: pulumi.Input['OperatingSystemTypes']):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of this gallery image definition resource. This property is updatable.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def disallowed(self) -> Optional[pulumi.Input['DisallowedArgs']]:
        """
        Describes the disallowed disk types.
        """
        return pulumi.get(self, "disallowed")

    @disallowed.setter
    def disallowed(self, value: Optional[pulumi.Input['DisallowedArgs']]):
        pulumi.set(self, "disallowed", value)

    @property
    @pulumi.getter(name="endOfLifeDate")
    def end_of_life_date(self) -> Optional[pulumi.Input[str]]:
        """
        The end of life date of the gallery image definition. This property can be used for decommissioning purposes. This property is updatable.
        """
        return pulumi.get(self, "end_of_life_date")

    @end_of_life_date.setter
    def end_of_life_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_of_life_date", value)

    @property
    @pulumi.getter
    def eula(self) -> Optional[pulumi.Input[str]]:
        """
        The Eula agreement for the gallery image definition.
        """
        return pulumi.get(self, "eula")

    @eula.setter
    def eula(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eula", value)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GalleryImageFeatureArgs']]]]:
        """
        A list of gallery image features.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GalleryImageFeatureArgs']]]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter(name="galleryImageName")
    def gallery_image_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the gallery image definition to be created or updated. The allowed characters are alphabets and numbers with dots, dashes, and periods allowed in the middle. The maximum length is 80 characters.
        """
        return pulumi.get(self, "gallery_image_name")

    @gallery_image_name.setter
    def gallery_image_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gallery_image_name", value)

    @property
    @pulumi.getter(name="hyperVGeneration")
    def hyper_v_generation(self) -> Optional[pulumi.Input[Union[str, 'HyperVGeneration']]]:
        """
        The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        """
        return pulumi.get(self, "hyper_v_generation")

    @hyper_v_generation.setter
    def hyper_v_generation(self, value: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]]):
        pulumi.set(self, "hyper_v_generation", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="privacyStatementUri")
    def privacy_statement_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The privacy statement uri.
        """
        return pulumi.get(self, "privacy_statement_uri")

    @privacy_statement_uri.setter
    def privacy_statement_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "privacy_statement_uri", value)

    @property
    @pulumi.getter(name="purchasePlan")
    def purchase_plan(self) -> Optional[pulumi.Input['ImagePurchasePlanArgs']]:
        """
        Describes the gallery image definition purchase plan. This is used by marketplace images.
        """
        return pulumi.get(self, "purchase_plan")

    @purchase_plan.setter
    def purchase_plan(self, value: Optional[pulumi.Input['ImagePurchasePlanArgs']]):
        pulumi.set(self, "purchase_plan", value)

    @property
    @pulumi.getter
    def recommended(self) -> Optional[pulumi.Input['RecommendedMachineConfigurationArgs']]:
        """
        The properties describe the recommended machine configuration for this Image Definition. These properties are updatable.
        """
        return pulumi.get(self, "recommended")

    @recommended.setter
    def recommended(self, value: Optional[pulumi.Input['RecommendedMachineConfigurationArgs']]):
        pulumi.set(self, "recommended", value)

    @property
    @pulumi.getter(name="releaseNoteUri")
    def release_note_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The release note uri.
        """
        return pulumi.get(self, "release_note_uri")

    @release_note_uri.setter
    def release_note_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "release_note_uri", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class GalleryImage(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disallowed: Optional[pulumi.Input[pulumi.InputType['DisallowedArgs']]] = None,
                 end_of_life_date: Optional[pulumi.Input[str]] = None,
                 eula: Optional[pulumi.Input[str]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GalleryImageFeatureArgs']]]]] = None,
                 gallery_image_name: Optional[pulumi.Input[str]] = None,
                 gallery_name: Optional[pulumi.Input[str]] = None,
                 hyper_v_generation: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]] = None,
                 identifier: Optional[pulumi.Input[pulumi.InputType['GalleryImageIdentifierArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_state: Optional[pulumi.Input['OperatingSystemStateTypes']] = None,
                 os_type: Optional[pulumi.Input['OperatingSystemTypes']] = None,
                 privacy_statement_uri: Optional[pulumi.Input[str]] = None,
                 purchase_plan: Optional[pulumi.Input[pulumi.InputType['ImagePurchasePlanArgs']]] = None,
                 recommended: Optional[pulumi.Input[pulumi.InputType['RecommendedMachineConfigurationArgs']]] = None,
                 release_note_uri: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Specifies information about the gallery image definition that you want to create or update.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of this gallery image definition resource. This property is updatable.
        :param pulumi.Input[pulumi.InputType['DisallowedArgs']] disallowed: Describes the disallowed disk types.
        :param pulumi.Input[str] end_of_life_date: The end of life date of the gallery image definition. This property can be used for decommissioning purposes. This property is updatable.
        :param pulumi.Input[str] eula: The Eula agreement for the gallery image definition.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GalleryImageFeatureArgs']]]] features: A list of gallery image features.
        :param pulumi.Input[str] gallery_image_name: The name of the gallery image definition to be created or updated. The allowed characters are alphabets and numbers with dots, dashes, and periods allowed in the middle. The maximum length is 80 characters.
        :param pulumi.Input[str] gallery_name: The name of the Shared Image Gallery in which the Image Definition is to be created.
        :param pulumi.Input[Union[str, 'HyperVGeneration']] hyper_v_generation: The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        :param pulumi.Input[pulumi.InputType['GalleryImageIdentifierArgs']] identifier: This is the gallery image definition identifier.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input['OperatingSystemStateTypes'] os_state: This property allows the user to specify whether the virtual machines created under this image are 'Generalized' or 'Specialized'.
        :param pulumi.Input['OperatingSystemTypes'] os_type: This property allows you to specify the type of the OS that is included in the disk when creating a VM from a managed image. <br><br> Possible values are: <br><br> **Windows** <br><br> **Linux**
        :param pulumi.Input[str] privacy_statement_uri: The privacy statement uri.
        :param pulumi.Input[pulumi.InputType['ImagePurchasePlanArgs']] purchase_plan: Describes the gallery image definition purchase plan. This is used by marketplace images.
        :param pulumi.Input[pulumi.InputType['RecommendedMachineConfigurationArgs']] recommended: The properties describe the recommended machine configuration for this Image Definition. These properties are updatable.
        :param pulumi.Input[str] release_note_uri: The release note uri.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GalleryImageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Specifies information about the gallery image definition that you want to create or update.

        :param str resource_name: The name of the resource.
        :param GalleryImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GalleryImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disallowed: Optional[pulumi.Input[pulumi.InputType['DisallowedArgs']]] = None,
                 end_of_life_date: Optional[pulumi.Input[str]] = None,
                 eula: Optional[pulumi.Input[str]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GalleryImageFeatureArgs']]]]] = None,
                 gallery_image_name: Optional[pulumi.Input[str]] = None,
                 gallery_name: Optional[pulumi.Input[str]] = None,
                 hyper_v_generation: Optional[pulumi.Input[Union[str, 'HyperVGeneration']]] = None,
                 identifier: Optional[pulumi.Input[pulumi.InputType['GalleryImageIdentifierArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_state: Optional[pulumi.Input['OperatingSystemStateTypes']] = None,
                 os_type: Optional[pulumi.Input['OperatingSystemTypes']] = None,
                 privacy_statement_uri: Optional[pulumi.Input[str]] = None,
                 purchase_plan: Optional[pulumi.Input[pulumi.InputType['ImagePurchasePlanArgs']]] = None,
                 recommended: Optional[pulumi.Input[pulumi.InputType['RecommendedMachineConfigurationArgs']]] = None,
                 release_note_uri: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = GalleryImageArgs.__new__(GalleryImageArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["disallowed"] = disallowed
            __props__.__dict__["end_of_life_date"] = end_of_life_date
            __props__.__dict__["eula"] = eula
            __props__.__dict__["features"] = features
            __props__.__dict__["gallery_image_name"] = gallery_image_name
            if gallery_name is None and not opts.urn:
                raise TypeError("Missing required property 'gallery_name'")
            __props__.__dict__["gallery_name"] = gallery_name
            __props__.__dict__["hyper_v_generation"] = hyper_v_generation
            if identifier is None and not opts.urn:
                raise TypeError("Missing required property 'identifier'")
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["location"] = location
            if os_state is None and not opts.urn:
                raise TypeError("Missing required property 'os_state'")
            __props__.__dict__["os_state"] = os_state
            if os_type is None and not opts.urn:
                raise TypeError("Missing required property 'os_type'")
            __props__.__dict__["os_type"] = os_type
            __props__.__dict__["privacy_statement_uri"] = privacy_statement_uri
            __props__.__dict__["purchase_plan"] = purchase_plan
            __props__.__dict__["recommended"] = recommended
            __props__.__dict__["release_note_uri"] = release_note_uri
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute/v20200930:GalleryImage"), pulumi.Alias(type_="azure-native:compute:GalleryImage"), pulumi.Alias(type_="azure-nextgen:compute:GalleryImage"), pulumi.Alias(type_="azure-native:compute/v20180601:GalleryImage"), pulumi.Alias(type_="azure-nextgen:compute/v20180601:GalleryImage"), pulumi.Alias(type_="azure-native:compute/v20190301:GalleryImage"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:GalleryImage"), pulumi.Alias(type_="azure-native:compute/v20190701:GalleryImage"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:GalleryImage"), pulumi.Alias(type_="azure-native:compute/v20191201:GalleryImage"), pulumi.Alias(type_="azure-nextgen:compute/v20191201:GalleryImage"), pulumi.Alias(type_="azure-native:compute/v20210701:GalleryImage"), pulumi.Alias(type_="azure-nextgen:compute/v20210701:GalleryImage")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(GalleryImage, __self__).__init__(
            'azure-native:compute/v20200930:GalleryImage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'GalleryImage':
        """
        Get an existing GalleryImage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GalleryImageArgs.__new__(GalleryImageArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["disallowed"] = None
        __props__.__dict__["end_of_life_date"] = None
        __props__.__dict__["eula"] = None
        __props__.__dict__["features"] = None
        __props__.__dict__["hyper_v_generation"] = None
        __props__.__dict__["identifier"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["os_state"] = None
        __props__.__dict__["os_type"] = None
        __props__.__dict__["privacy_statement_uri"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["purchase_plan"] = None
        __props__.__dict__["recommended"] = None
        __props__.__dict__["release_note_uri"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return GalleryImage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of this gallery image definition resource. This property is updatable.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def disallowed(self) -> pulumi.Output[Optional['outputs.DisallowedResponse']]:
        """
        Describes the disallowed disk types.
        """
        return pulumi.get(self, "disallowed")

    @property
    @pulumi.getter(name="endOfLifeDate")
    def end_of_life_date(self) -> pulumi.Output[Optional[str]]:
        """
        The end of life date of the gallery image definition. This property can be used for decommissioning purposes. This property is updatable.
        """
        return pulumi.get(self, "end_of_life_date")

    @property
    @pulumi.getter
    def eula(self) -> pulumi.Output[Optional[str]]:
        """
        The Eula agreement for the gallery image definition.
        """
        return pulumi.get(self, "eula")

    @property
    @pulumi.getter
    def features(self) -> pulumi.Output[Optional[Sequence['outputs.GalleryImageFeatureResponse']]]:
        """
        A list of gallery image features.
        """
        return pulumi.get(self, "features")

    @property
    @pulumi.getter(name="hyperVGeneration")
    def hyper_v_generation(self) -> pulumi.Output[Optional[str]]:
        """
        The hypervisor generation of the Virtual Machine. Applicable to OS disks only.
        """
        return pulumi.get(self, "hyper_v_generation")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output['outputs.GalleryImageIdentifierResponse']:
        """
        This is the gallery image definition identifier.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osState")
    def os_state(self) -> pulumi.Output[str]:
        """
        This property allows the user to specify whether the virtual machines created under this image are 'Generalized' or 'Specialized'.
        """
        return pulumi.get(self, "os_state")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[str]:
        """
        This property allows you to specify the type of the OS that is included in the disk when creating a VM from a managed image. <br><br> Possible values are: <br><br> **Windows** <br><br> **Linux**
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="privacyStatementUri")
    def privacy_statement_uri(self) -> pulumi.Output[Optional[str]]:
        """
        The privacy statement uri.
        """
        return pulumi.get(self, "privacy_statement_uri")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="purchasePlan")
    def purchase_plan(self) -> pulumi.Output[Optional['outputs.ImagePurchasePlanResponse']]:
        """
        Describes the gallery image definition purchase plan. This is used by marketplace images.
        """
        return pulumi.get(self, "purchase_plan")

    @property
    @pulumi.getter
    def recommended(self) -> pulumi.Output[Optional['outputs.RecommendedMachineConfigurationResponse']]:
        """
        The properties describe the recommended machine configuration for this Image Definition. These properties are updatable.
        """
        return pulumi.get(self, "recommended")

    @property
    @pulumi.getter(name="releaseNoteUri")
    def release_note_uri(self) -> pulumi.Output[Optional[str]]:
        """
        The release note uri.
        """
        return pulumi.get(self, "release_note_uri")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

