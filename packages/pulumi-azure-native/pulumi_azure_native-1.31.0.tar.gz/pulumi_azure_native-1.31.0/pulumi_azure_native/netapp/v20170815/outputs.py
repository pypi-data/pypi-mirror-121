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

__all__ = [
    'ActiveDirectoryResponse',
    'ExportPolicyRuleResponse',
    'VolumePropertiesResponseExportPolicy',
]

@pulumi.output_type
class ActiveDirectoryResponse(dict):
    """
    Active Directory
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "activeDirectoryId":
            suggest = "active_directory_id"
        elif key == "dNS":
            suggest = "d_ns"
        elif key == "organizationalUnit":
            suggest = "organizational_unit"
        elif key == "sMBServerName":
            suggest = "s_mb_server_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ActiveDirectoryResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ActiveDirectoryResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ActiveDirectoryResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 active_directory_id: Optional[str] = None,
                 d_ns: Optional[str] = None,
                 domain: Optional[str] = None,
                 organizational_unit: Optional[str] = None,
                 password: Optional[str] = None,
                 s_mb_server_name: Optional[str] = None,
                 status: Optional[str] = None,
                 username: Optional[str] = None):
        """
        Active Directory
        :param str active_directory_id: Id of the Active Directory
        :param str d_ns: Comma separated list of DNS server IP addresses for the Active Directory domain
        :param str domain: Name of the Active Directory domain
        :param str organizational_unit: The Organizational Unit (OU) within the Windows Active Directory
        :param str password: Plain text password of Active Directory domain administrator
        :param str s_mb_server_name: NetBIOS name of the SMB server. This name will be registered as a computer account in the AD and used to mount volumes
        :param str status: Status of the Active Directory
        :param str username: Username of Active Directory domain administrator
        """
        if active_directory_id is not None:
            pulumi.set(__self__, "active_directory_id", active_directory_id)
        if d_ns is not None:
            pulumi.set(__self__, "d_ns", d_ns)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if organizational_unit is not None:
            pulumi.set(__self__, "organizational_unit", organizational_unit)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if s_mb_server_name is not None:
            pulumi.set(__self__, "s_mb_server_name", s_mb_server_name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="activeDirectoryId")
    def active_directory_id(self) -> Optional[str]:
        """
        Id of the Active Directory
        """
        return pulumi.get(self, "active_directory_id")

    @property
    @pulumi.getter(name="dNS")
    def d_ns(self) -> Optional[str]:
        """
        Comma separated list of DNS server IP addresses for the Active Directory domain
        """
        return pulumi.get(self, "d_ns")

    @property
    @pulumi.getter
    def domain(self) -> Optional[str]:
        """
        Name of the Active Directory domain
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="organizationalUnit")
    def organizational_unit(self) -> Optional[str]:
        """
        The Organizational Unit (OU) within the Windows Active Directory
        """
        return pulumi.get(self, "organizational_unit")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        Plain text password of Active Directory domain administrator
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="sMBServerName")
    def s_mb_server_name(self) -> Optional[str]:
        """
        NetBIOS name of the SMB server. This name will be registered as a computer account in the AD and used to mount volumes
        """
        return pulumi.get(self, "s_mb_server_name")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Status of the Active Directory
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username of Active Directory domain administrator
        """
        return pulumi.get(self, "username")


@pulumi.output_type
class ExportPolicyRuleResponse(dict):
    """
    Volume Export Policy Rule
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "allowedClients":
            suggest = "allowed_clients"
        elif key == "ruleIndex":
            suggest = "rule_index"
        elif key == "unixReadOnly":
            suggest = "unix_read_only"
        elif key == "unixReadWrite":
            suggest = "unix_read_write"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExportPolicyRuleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExportPolicyRuleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExportPolicyRuleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allowed_clients: Optional[str] = None,
                 cifs: Optional[bool] = None,
                 nfsv3: Optional[bool] = None,
                 nfsv4: Optional[bool] = None,
                 rule_index: Optional[int] = None,
                 unix_read_only: Optional[bool] = None,
                 unix_read_write: Optional[bool] = None):
        """
        Volume Export Policy Rule
        :param str allowed_clients: Client ingress specification as comma separated string with IPv4 CIDRs, IPv4 host addresses and host names
        :param bool cifs: Allows CIFS protocol
        :param bool nfsv3: Allows NFSv3 protocol
        :param bool nfsv4: Allows NFSv4 protocol
        :param int rule_index: Order index
        :param bool unix_read_only: Read only access
        :param bool unix_read_write: Read and write access
        """
        if allowed_clients is not None:
            pulumi.set(__self__, "allowed_clients", allowed_clients)
        if cifs is not None:
            pulumi.set(__self__, "cifs", cifs)
        if nfsv3 is not None:
            pulumi.set(__self__, "nfsv3", nfsv3)
        if nfsv4 is not None:
            pulumi.set(__self__, "nfsv4", nfsv4)
        if rule_index is not None:
            pulumi.set(__self__, "rule_index", rule_index)
        if unix_read_only is not None:
            pulumi.set(__self__, "unix_read_only", unix_read_only)
        if unix_read_write is not None:
            pulumi.set(__self__, "unix_read_write", unix_read_write)

    @property
    @pulumi.getter(name="allowedClients")
    def allowed_clients(self) -> Optional[str]:
        """
        Client ingress specification as comma separated string with IPv4 CIDRs, IPv4 host addresses and host names
        """
        return pulumi.get(self, "allowed_clients")

    @property
    @pulumi.getter
    def cifs(self) -> Optional[bool]:
        """
        Allows CIFS protocol
        """
        return pulumi.get(self, "cifs")

    @property
    @pulumi.getter
    def nfsv3(self) -> Optional[bool]:
        """
        Allows NFSv3 protocol
        """
        return pulumi.get(self, "nfsv3")

    @property
    @pulumi.getter
    def nfsv4(self) -> Optional[bool]:
        """
        Allows NFSv4 protocol
        """
        return pulumi.get(self, "nfsv4")

    @property
    @pulumi.getter(name="ruleIndex")
    def rule_index(self) -> Optional[int]:
        """
        Order index
        """
        return pulumi.get(self, "rule_index")

    @property
    @pulumi.getter(name="unixReadOnly")
    def unix_read_only(self) -> Optional[bool]:
        """
        Read only access
        """
        return pulumi.get(self, "unix_read_only")

    @property
    @pulumi.getter(name="unixReadWrite")
    def unix_read_write(self) -> Optional[bool]:
        """
        Read and write access
        """
        return pulumi.get(self, "unix_read_write")


@pulumi.output_type
class VolumePropertiesResponseExportPolicy(dict):
    """
    Export policy rule
    """
    def __init__(__self__, *,
                 rules: Optional[Sequence['outputs.ExportPolicyRuleResponse']] = None):
        """
        Export policy rule
        """
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.ExportPolicyRuleResponse']]:
        return pulumi.get(self, "rules")


