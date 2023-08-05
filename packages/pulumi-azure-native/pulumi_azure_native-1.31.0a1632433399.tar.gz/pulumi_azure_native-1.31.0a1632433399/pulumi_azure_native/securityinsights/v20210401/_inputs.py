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
    'IncidentLabelArgs',
    'IncidentOwnerInfoArgs',
    'ThreatIntelligenceExternalReferenceArgs',
    'ThreatIntelligenceGranularMarkingModelArgs',
    'ThreatIntelligenceKillChainPhaseArgs',
    'ThreatIntelligenceParsedPatternTypeValueArgs',
    'ThreatIntelligenceParsedPatternArgs',
    'WatchlistUserInfoArgs',
]

@pulumi.input_type
class IncidentLabelArgs:
    def __init__(__self__, *,
                 label_name: pulumi.Input[str]):
        """
        Represents an incident label
        :param pulumi.Input[str] label_name: The name of the label
        """
        pulumi.set(__self__, "label_name", label_name)

    @property
    @pulumi.getter(name="labelName")
    def label_name(self) -> pulumi.Input[str]:
        """
        The name of the label
        """
        return pulumi.get(self, "label_name")

    @label_name.setter
    def label_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "label_name", value)


@pulumi.input_type
class IncidentOwnerInfoArgs:
    def __init__(__self__, *,
                 assigned_to: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 object_id: Optional[pulumi.Input[str]] = None,
                 user_principal_name: Optional[pulumi.Input[str]] = None):
        """
        Information on the user an incident is assigned to
        :param pulumi.Input[str] assigned_to: The name of the user the incident is assigned to.
        :param pulumi.Input[str] email: The email of the user the incident is assigned to.
        :param pulumi.Input[str] object_id: The object id of the user the incident is assigned to.
        :param pulumi.Input[str] user_principal_name: The user principal name of the user the incident is assigned to.
        """
        if assigned_to is not None:
            pulumi.set(__self__, "assigned_to", assigned_to)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if object_id is not None:
            pulumi.set(__self__, "object_id", object_id)
        if user_principal_name is not None:
            pulumi.set(__self__, "user_principal_name", user_principal_name)

    @property
    @pulumi.getter(name="assignedTo")
    def assigned_to(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user the incident is assigned to.
        """
        return pulumi.get(self, "assigned_to")

    @assigned_to.setter
    def assigned_to(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "assigned_to", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        The email of the user the incident is assigned to.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object id of the user the incident is assigned to.
        """
        return pulumi.get(self, "object_id")

    @object_id.setter
    def object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "object_id", value)

    @property
    @pulumi.getter(name="userPrincipalName")
    def user_principal_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user principal name of the user the incident is assigned to.
        """
        return pulumi.get(self, "user_principal_name")

    @user_principal_name.setter
    def user_principal_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_principal_name", value)


@pulumi.input_type
class ThreatIntelligenceExternalReferenceArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 external_id: Optional[pulumi.Input[str]] = None,
                 hashes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 source_name: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Describes external reference
        :param pulumi.Input[str] description: External reference description
        :param pulumi.Input[str] external_id: External reference ID
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] hashes: External reference hashes
        :param pulumi.Input[str] source_name: External reference source name
        :param pulumi.Input[str] url: External reference URL
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if external_id is not None:
            pulumi.set(__self__, "external_id", external_id)
        if hashes is not None:
            pulumi.set(__self__, "hashes", hashes)
        if source_name is not None:
            pulumi.set(__self__, "source_name", source_name)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        External reference description
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> Optional[pulumi.Input[str]]:
        """
        External reference ID
        """
        return pulumi.get(self, "external_id")

    @external_id.setter
    def external_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_id", value)

    @property
    @pulumi.getter
    def hashes(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        External reference hashes
        """
        return pulumi.get(self, "hashes")

    @hashes.setter
    def hashes(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "hashes", value)

    @property
    @pulumi.getter(name="sourceName")
    def source_name(self) -> Optional[pulumi.Input[str]]:
        """
        External reference source name
        """
        return pulumi.get(self, "source_name")

    @source_name.setter
    def source_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_name", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        External reference URL
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


@pulumi.input_type
class ThreatIntelligenceGranularMarkingModelArgs:
    def __init__(__self__, *,
                 language: Optional[pulumi.Input[str]] = None,
                 marking_ref: Optional[pulumi.Input[int]] = None,
                 selectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Describes threat granular marking model entity
        :param pulumi.Input[str] language: Language granular marking model
        :param pulumi.Input[int] marking_ref: marking reference granular marking model
        :param pulumi.Input[Sequence[pulumi.Input[str]]] selectors: granular marking model selectors
        """
        if language is not None:
            pulumi.set(__self__, "language", language)
        if marking_ref is not None:
            pulumi.set(__self__, "marking_ref", marking_ref)
        if selectors is not None:
            pulumi.set(__self__, "selectors", selectors)

    @property
    @pulumi.getter
    def language(self) -> Optional[pulumi.Input[str]]:
        """
        Language granular marking model
        """
        return pulumi.get(self, "language")

    @language.setter
    def language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "language", value)

    @property
    @pulumi.getter(name="markingRef")
    def marking_ref(self) -> Optional[pulumi.Input[int]]:
        """
        marking reference granular marking model
        """
        return pulumi.get(self, "marking_ref")

    @marking_ref.setter
    def marking_ref(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "marking_ref", value)

    @property
    @pulumi.getter
    def selectors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        granular marking model selectors
        """
        return pulumi.get(self, "selectors")

    @selectors.setter
    def selectors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "selectors", value)


@pulumi.input_type
class ThreatIntelligenceKillChainPhaseArgs:
    def __init__(__self__, *,
                 kill_chain_name: Optional[pulumi.Input[str]] = None,
                 phase_name: Optional[pulumi.Input[str]] = None):
        """
        Describes threat kill chain phase entity
        :param pulumi.Input[str] kill_chain_name: Kill chainName name
        :param pulumi.Input[str] phase_name: Phase name
        """
        if kill_chain_name is not None:
            pulumi.set(__self__, "kill_chain_name", kill_chain_name)
        if phase_name is not None:
            pulumi.set(__self__, "phase_name", phase_name)

    @property
    @pulumi.getter(name="killChainName")
    def kill_chain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Kill chainName name
        """
        return pulumi.get(self, "kill_chain_name")

    @kill_chain_name.setter
    def kill_chain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kill_chain_name", value)

    @property
    @pulumi.getter(name="phaseName")
    def phase_name(self) -> Optional[pulumi.Input[str]]:
        """
        Phase name
        """
        return pulumi.get(self, "phase_name")

    @phase_name.setter
    def phase_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "phase_name", value)


@pulumi.input_type
class ThreatIntelligenceParsedPatternTypeValueArgs:
    def __init__(__self__, *,
                 value: Optional[pulumi.Input[str]] = None,
                 value_type: Optional[pulumi.Input[str]] = None):
        """
        Describes threat kill chain phase entity
        :param pulumi.Input[str] value: Value of parsed pattern
        :param pulumi.Input[str] value_type: Type of the value
        """
        if value is not None:
            pulumi.set(__self__, "value", value)
        if value_type is not None:
            pulumi.set(__self__, "value_type", value_type)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Value of parsed pattern
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter(name="valueType")
    def value_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the value
        """
        return pulumi.get(self, "value_type")

    @value_type.setter
    def value_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value_type", value)


@pulumi.input_type
class ThreatIntelligenceParsedPatternArgs:
    def __init__(__self__, *,
                 pattern_type_key: Optional[pulumi.Input[str]] = None,
                 pattern_type_values: Optional[pulumi.Input[Sequence[pulumi.Input['ThreatIntelligenceParsedPatternTypeValueArgs']]]] = None):
        """
        Describes parsed pattern entity
        :param pulumi.Input[str] pattern_type_key: Pattern type key
        :param pulumi.Input[Sequence[pulumi.Input['ThreatIntelligenceParsedPatternTypeValueArgs']]] pattern_type_values: Pattern type keys
        """
        if pattern_type_key is not None:
            pulumi.set(__self__, "pattern_type_key", pattern_type_key)
        if pattern_type_values is not None:
            pulumi.set(__self__, "pattern_type_values", pattern_type_values)

    @property
    @pulumi.getter(name="patternTypeKey")
    def pattern_type_key(self) -> Optional[pulumi.Input[str]]:
        """
        Pattern type key
        """
        return pulumi.get(self, "pattern_type_key")

    @pattern_type_key.setter
    def pattern_type_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pattern_type_key", value)

    @property
    @pulumi.getter(name="patternTypeValues")
    def pattern_type_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ThreatIntelligenceParsedPatternTypeValueArgs']]]]:
        """
        Pattern type keys
        """
        return pulumi.get(self, "pattern_type_values")

    @pattern_type_values.setter
    def pattern_type_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ThreatIntelligenceParsedPatternTypeValueArgs']]]]):
        pulumi.set(self, "pattern_type_values", value)


@pulumi.input_type
class WatchlistUserInfoArgs:
    def __init__(__self__, *,
                 object_id: Optional[pulumi.Input[str]] = None):
        """
        User information that made some action
        :param pulumi.Input[str] object_id: The object id of the user.
        """
        if object_id is not None:
            pulumi.set(__self__, "object_id", object_id)

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object id of the user.
        """
        return pulumi.get(self, "object_id")

    @object_id.setter
    def object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "object_id", value)


