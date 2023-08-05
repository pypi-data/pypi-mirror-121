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
    'GetPolicyAssignmentArtifactResult',
    'AwaitableGetPolicyAssignmentArtifactResult',
    'get_policy_assignment_artifact',
]

@pulumi.output_type
class GetPolicyAssignmentArtifactResult:
    """
    Blueprint artifact applies Policy assignments.
    """
    def __init__(__self__, depends_on=None, description=None, display_name=None, id=None, kind=None, name=None, parameters=None, policy_definition_id=None, resource_group=None, type=None):
        if depends_on and not isinstance(depends_on, list):
            raise TypeError("Expected argument 'depends_on' to be a list")
        pulumi.set(__self__, "depends_on", depends_on)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if policy_definition_id and not isinstance(policy_definition_id, str):
            raise TypeError("Expected argument 'policy_definition_id' to be a str")
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        if resource_group and not isinstance(resource_group, str):
            raise TypeError("Expected argument 'resource_group' to be a str")
        pulumi.set(__self__, "resource_group", resource_group)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dependsOn")
    def depends_on(self) -> Optional[Sequence[str]]:
        """
        Artifacts which need to be deployed before the specified artifact.
        """
        return pulumi.get(self, "depends_on")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Multi-line explain this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        One-liner string explain this resource.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        String Id used to locate any resource on Azure.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Specifies the kind of Blueprint artifact.
        Expected value is 'policyAssignment'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of this resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Mapping[str, 'outputs.ParameterValueBaseResponse']:
        """
        Parameter values for the policy definition.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> str:
        """
        Azure resource ID of the policy definition.
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> Optional[str]:
        """
        Name of the resource group placeholder to which the policy will be assigned.
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of this resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetPolicyAssignmentArtifactResult(GetPolicyAssignmentArtifactResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyAssignmentArtifactResult(
            depends_on=self.depends_on,
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            kind=self.kind,
            name=self.name,
            parameters=self.parameters,
            policy_definition_id=self.policy_definition_id,
            resource_group=self.resource_group,
            type=self.type)


def get_policy_assignment_artifact(artifact_name: Optional[str] = None,
                                   blueprint_name: Optional[str] = None,
                                   management_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyAssignmentArtifactResult:
    """
    Blueprint artifact applies Policy assignments.


    :param str artifact_name: name of the artifact.
    :param str blueprint_name: name of the blueprint.
    :param str management_group_name: ManagementGroup where blueprint stores.
    """
    __args__ = dict()
    __args__['artifactName'] = artifact_name
    __args__['blueprintName'] = blueprint_name
    __args__['managementGroupName'] = management_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:blueprint/v20171111preview:getPolicyAssignmentArtifact', __args__, opts=opts, typ=GetPolicyAssignmentArtifactResult).value

    return AwaitableGetPolicyAssignmentArtifactResult(
        depends_on=__ret__.depends_on,
        description=__ret__.description,
        display_name=__ret__.display_name,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        parameters=__ret__.parameters,
        policy_definition_id=__ret__.policy_definition_id,
        resource_group=__ret__.resource_group,
        type=__ret__.type)
