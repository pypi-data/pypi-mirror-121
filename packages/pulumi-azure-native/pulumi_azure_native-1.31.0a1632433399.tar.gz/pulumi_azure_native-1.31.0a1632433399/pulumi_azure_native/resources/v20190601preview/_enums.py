# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'TemplateSpecArtifactKind',
]


class TemplateSpecArtifactKind(str, Enum):
    """
    The kind of artifact.
    """
    TEMPLATE = "template"
    """The artifact represents an embedded Azure Resource Manager template."""
