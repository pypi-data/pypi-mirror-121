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
    'ConnectToSourceSqlServerTaskInputArgs',
    'ConnectToSourceSqlServerTaskPropertiesArgs',
    'ConnectToTargetSqlDbTaskInputArgs',
    'ConnectToTargetSqlDbTaskPropertiesArgs',
    'DatabaseInfoArgs',
    'GetUserTablesSqlTaskInputArgs',
    'GetUserTablesSqlTaskPropertiesArgs',
    'MigrateSqlServerSqlDbDatabaseInputArgs',
    'MigrateSqlServerSqlDbTaskInputArgs',
    'MigrateSqlServerSqlDbTaskPropertiesArgs',
    'MigrationValidationOptionsArgs',
    'ServiceSkuArgs',
    'SqlConnectionInfoArgs',
]

@pulumi.input_type
class ConnectToSourceSqlServerTaskInputArgs:
    def __init__(__self__, *,
                 source_connection_info: pulumi.Input['SqlConnectionInfoArgs'],
                 check_permissions_group: Optional[pulumi.Input['ServerLevelPermissionsGroup']] = None):
        """
        Input for the task that validates connection to SQL Server and also validates source server requirements
        :param pulumi.Input['SqlConnectionInfoArgs'] source_connection_info: Connection information for Source SQL Server
        :param pulumi.Input['ServerLevelPermissionsGroup'] check_permissions_group: Permission group for validations
        """
        pulumi.set(__self__, "source_connection_info", source_connection_info)
        if check_permissions_group is not None:
            pulumi.set(__self__, "check_permissions_group", check_permissions_group)

    @property
    @pulumi.getter(name="sourceConnectionInfo")
    def source_connection_info(self) -> pulumi.Input['SqlConnectionInfoArgs']:
        """
        Connection information for Source SQL Server
        """
        return pulumi.get(self, "source_connection_info")

    @source_connection_info.setter
    def source_connection_info(self, value: pulumi.Input['SqlConnectionInfoArgs']):
        pulumi.set(self, "source_connection_info", value)

    @property
    @pulumi.getter(name="checkPermissionsGroup")
    def check_permissions_group(self) -> Optional[pulumi.Input['ServerLevelPermissionsGroup']]:
        """
        Permission group for validations
        """
        return pulumi.get(self, "check_permissions_group")

    @check_permissions_group.setter
    def check_permissions_group(self, value: Optional[pulumi.Input['ServerLevelPermissionsGroup']]):
        pulumi.set(self, "check_permissions_group", value)


@pulumi.input_type
class ConnectToSourceSqlServerTaskPropertiesArgs:
    def __init__(__self__, *,
                 task_type: pulumi.Input[str],
                 input: Optional[pulumi.Input['ConnectToSourceSqlServerTaskInputArgs']] = None):
        """
        Properties for the task that validates connection to SQL Server and also validates source server requirements
        :param pulumi.Input[str] task_type: Task type.
               Expected value is 'ConnectToSource.SqlServer'.
        :param pulumi.Input['ConnectToSourceSqlServerTaskInputArgs'] input: Task input
        """
        pulumi.set(__self__, "task_type", 'ConnectToSource.SqlServer')
        if input is not None:
            pulumi.set(__self__, "input", input)

    @property
    @pulumi.getter(name="taskType")
    def task_type(self) -> pulumi.Input[str]:
        """
        Task type.
        Expected value is 'ConnectToSource.SqlServer'.
        """
        return pulumi.get(self, "task_type")

    @task_type.setter
    def task_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "task_type", value)

    @property
    @pulumi.getter
    def input(self) -> Optional[pulumi.Input['ConnectToSourceSqlServerTaskInputArgs']]:
        """
        Task input
        """
        return pulumi.get(self, "input")

    @input.setter
    def input(self, value: Optional[pulumi.Input['ConnectToSourceSqlServerTaskInputArgs']]):
        pulumi.set(self, "input", value)


@pulumi.input_type
class ConnectToTargetSqlDbTaskInputArgs:
    def __init__(__self__, *,
                 target_connection_info: pulumi.Input['SqlConnectionInfoArgs']):
        """
        Input for the task that validates connection to SQL DB and target server requirements
        :param pulumi.Input['SqlConnectionInfoArgs'] target_connection_info: Connection information for target SQL DB
        """
        pulumi.set(__self__, "target_connection_info", target_connection_info)

    @property
    @pulumi.getter(name="targetConnectionInfo")
    def target_connection_info(self) -> pulumi.Input['SqlConnectionInfoArgs']:
        """
        Connection information for target SQL DB
        """
        return pulumi.get(self, "target_connection_info")

    @target_connection_info.setter
    def target_connection_info(self, value: pulumi.Input['SqlConnectionInfoArgs']):
        pulumi.set(self, "target_connection_info", value)


@pulumi.input_type
class ConnectToTargetSqlDbTaskPropertiesArgs:
    def __init__(__self__, *,
                 task_type: pulumi.Input[str],
                 input: Optional[pulumi.Input['ConnectToTargetSqlDbTaskInputArgs']] = None):
        """
        Properties for the task that validates connection to SQL DB and target server requirements
        :param pulumi.Input[str] task_type: Task type.
               Expected value is 'ConnectToTarget.SqlDb'.
        :param pulumi.Input['ConnectToTargetSqlDbTaskInputArgs'] input: Task input
        """
        pulumi.set(__self__, "task_type", 'ConnectToTarget.SqlDb')
        if input is not None:
            pulumi.set(__self__, "input", input)

    @property
    @pulumi.getter(name="taskType")
    def task_type(self) -> pulumi.Input[str]:
        """
        Task type.
        Expected value is 'ConnectToTarget.SqlDb'.
        """
        return pulumi.get(self, "task_type")

    @task_type.setter
    def task_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "task_type", value)

    @property
    @pulumi.getter
    def input(self) -> Optional[pulumi.Input['ConnectToTargetSqlDbTaskInputArgs']]:
        """
        Task input
        """
        return pulumi.get(self, "input")

    @input.setter
    def input(self, value: Optional[pulumi.Input['ConnectToTargetSqlDbTaskInputArgs']]):
        pulumi.set(self, "input", value)


@pulumi.input_type
class DatabaseInfoArgs:
    def __init__(__self__, *,
                 source_database_name: pulumi.Input[str]):
        """
        Project Database Details
        :param pulumi.Input[str] source_database_name: Name of the database
        """
        pulumi.set(__self__, "source_database_name", source_database_name)

    @property
    @pulumi.getter(name="sourceDatabaseName")
    def source_database_name(self) -> pulumi.Input[str]:
        """
        Name of the database
        """
        return pulumi.get(self, "source_database_name")

    @source_database_name.setter
    def source_database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_database_name", value)


@pulumi.input_type
class GetUserTablesSqlTaskInputArgs:
    def __init__(__self__, *,
                 connection_info: pulumi.Input['SqlConnectionInfoArgs'],
                 selected_databases: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        Input for the task that collects user tables for the given list of databases
        :param pulumi.Input['SqlConnectionInfoArgs'] connection_info: Connection information for SQL Server
        :param pulumi.Input[Sequence[pulumi.Input[str]]] selected_databases: List of database names to collect tables for
        """
        pulumi.set(__self__, "connection_info", connection_info)
        pulumi.set(__self__, "selected_databases", selected_databases)

    @property
    @pulumi.getter(name="connectionInfo")
    def connection_info(self) -> pulumi.Input['SqlConnectionInfoArgs']:
        """
        Connection information for SQL Server
        """
        return pulumi.get(self, "connection_info")

    @connection_info.setter
    def connection_info(self, value: pulumi.Input['SqlConnectionInfoArgs']):
        pulumi.set(self, "connection_info", value)

    @property
    @pulumi.getter(name="selectedDatabases")
    def selected_databases(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of database names to collect tables for
        """
        return pulumi.get(self, "selected_databases")

    @selected_databases.setter
    def selected_databases(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "selected_databases", value)


@pulumi.input_type
class GetUserTablesSqlTaskPropertiesArgs:
    def __init__(__self__, *,
                 task_type: pulumi.Input[str],
                 input: Optional[pulumi.Input['GetUserTablesSqlTaskInputArgs']] = None):
        """
        Properties for the task that collects user tables for the given list of databases
        :param pulumi.Input[str] task_type: Task type.
               Expected value is 'GetUserTables.Sql'.
        :param pulumi.Input['GetUserTablesSqlTaskInputArgs'] input: Task input
        """
        pulumi.set(__self__, "task_type", 'GetUserTables.Sql')
        if input is not None:
            pulumi.set(__self__, "input", input)

    @property
    @pulumi.getter(name="taskType")
    def task_type(self) -> pulumi.Input[str]:
        """
        Task type.
        Expected value is 'GetUserTables.Sql'.
        """
        return pulumi.get(self, "task_type")

    @task_type.setter
    def task_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "task_type", value)

    @property
    @pulumi.getter
    def input(self) -> Optional[pulumi.Input['GetUserTablesSqlTaskInputArgs']]:
        """
        Task input
        """
        return pulumi.get(self, "input")

    @input.setter
    def input(self, value: Optional[pulumi.Input['GetUserTablesSqlTaskInputArgs']]):
        pulumi.set(self, "input", value)


@pulumi.input_type
class MigrateSqlServerSqlDbDatabaseInputArgs:
    def __init__(__self__, *,
                 make_source_db_read_only: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 table_map: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_database_name: Optional[pulumi.Input[str]] = None):
        """
        Database specific information for SQL to Azure SQL DB migration task inputs
        :param pulumi.Input[bool] make_source_db_read_only: Whether to set database read only before migration
        :param pulumi.Input[str] name: Name of the database
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] table_map: Mapping of source to target tables
        :param pulumi.Input[str] target_database_name: Name of target database. Note: Target database will be truncated before starting migration.
        """
        if make_source_db_read_only is not None:
            pulumi.set(__self__, "make_source_db_read_only", make_source_db_read_only)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if table_map is not None:
            pulumi.set(__self__, "table_map", table_map)
        if target_database_name is not None:
            pulumi.set(__self__, "target_database_name", target_database_name)

    @property
    @pulumi.getter(name="makeSourceDbReadOnly")
    def make_source_db_read_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to set database read only before migration
        """
        return pulumi.get(self, "make_source_db_read_only")

    @make_source_db_read_only.setter
    def make_source_db_read_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "make_source_db_read_only", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the database
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="tableMap")
    def table_map(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Mapping of source to target tables
        """
        return pulumi.get(self, "table_map")

    @table_map.setter
    def table_map(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "table_map", value)

    @property
    @pulumi.getter(name="targetDatabaseName")
    def target_database_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of target database. Note: Target database will be truncated before starting migration.
        """
        return pulumi.get(self, "target_database_name")

    @target_database_name.setter
    def target_database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_database_name", value)


@pulumi.input_type
class MigrateSqlServerSqlDbTaskInputArgs:
    def __init__(__self__, *,
                 selected_databases: pulumi.Input[Sequence[pulumi.Input['MigrateSqlServerSqlDbDatabaseInputArgs']]],
                 source_connection_info: pulumi.Input['SqlConnectionInfoArgs'],
                 target_connection_info: pulumi.Input['SqlConnectionInfoArgs'],
                 validation_options: Optional[pulumi.Input['MigrationValidationOptionsArgs']] = None):
        """
        Input for the task that migrates on-prem SQL Server databases to Azure SQL Database
        :param pulumi.Input[Sequence[pulumi.Input['MigrateSqlServerSqlDbDatabaseInputArgs']]] selected_databases: Databases to migrate
        :param pulumi.Input['SqlConnectionInfoArgs'] source_connection_info: Information for connecting to source
        :param pulumi.Input['SqlConnectionInfoArgs'] target_connection_info: Information for connecting to target
        :param pulumi.Input['MigrationValidationOptionsArgs'] validation_options: Options for enabling various post migration validations. Available options, 
                1.) Data Integrity Check: Performs a checksum based comparison on source and target tables after the migration to ensure the correctness of the data. 
                2.) Schema Validation: Performs a thorough schema comparison between the source and target tables and provides a list of differences between the source and target database, 3.) Query Analysis: Executes a set of queries picked up automatically either from the Query Plan Cache or Query Store and execute them and compares the execution time between the source and target database.
        """
        pulumi.set(__self__, "selected_databases", selected_databases)
        pulumi.set(__self__, "source_connection_info", source_connection_info)
        pulumi.set(__self__, "target_connection_info", target_connection_info)
        if validation_options is not None:
            pulumi.set(__self__, "validation_options", validation_options)

    @property
    @pulumi.getter(name="selectedDatabases")
    def selected_databases(self) -> pulumi.Input[Sequence[pulumi.Input['MigrateSqlServerSqlDbDatabaseInputArgs']]]:
        """
        Databases to migrate
        """
        return pulumi.get(self, "selected_databases")

    @selected_databases.setter
    def selected_databases(self, value: pulumi.Input[Sequence[pulumi.Input['MigrateSqlServerSqlDbDatabaseInputArgs']]]):
        pulumi.set(self, "selected_databases", value)

    @property
    @pulumi.getter(name="sourceConnectionInfo")
    def source_connection_info(self) -> pulumi.Input['SqlConnectionInfoArgs']:
        """
        Information for connecting to source
        """
        return pulumi.get(self, "source_connection_info")

    @source_connection_info.setter
    def source_connection_info(self, value: pulumi.Input['SqlConnectionInfoArgs']):
        pulumi.set(self, "source_connection_info", value)

    @property
    @pulumi.getter(name="targetConnectionInfo")
    def target_connection_info(self) -> pulumi.Input['SqlConnectionInfoArgs']:
        """
        Information for connecting to target
        """
        return pulumi.get(self, "target_connection_info")

    @target_connection_info.setter
    def target_connection_info(self, value: pulumi.Input['SqlConnectionInfoArgs']):
        pulumi.set(self, "target_connection_info", value)

    @property
    @pulumi.getter(name="validationOptions")
    def validation_options(self) -> Optional[pulumi.Input['MigrationValidationOptionsArgs']]:
        """
        Options for enabling various post migration validations. Available options, 
         1.) Data Integrity Check: Performs a checksum based comparison on source and target tables after the migration to ensure the correctness of the data. 
         2.) Schema Validation: Performs a thorough schema comparison between the source and target tables and provides a list of differences between the source and target database, 3.) Query Analysis: Executes a set of queries picked up automatically either from the Query Plan Cache or Query Store and execute them and compares the execution time between the source and target database.
        """
        return pulumi.get(self, "validation_options")

    @validation_options.setter
    def validation_options(self, value: Optional[pulumi.Input['MigrationValidationOptionsArgs']]):
        pulumi.set(self, "validation_options", value)


@pulumi.input_type
class MigrateSqlServerSqlDbTaskPropertiesArgs:
    def __init__(__self__, *,
                 task_type: pulumi.Input[str],
                 input: Optional[pulumi.Input['MigrateSqlServerSqlDbTaskInputArgs']] = None):
        """
        Properties for the task that migrates on-prem SQL Server databases to Azure SQL Database
        :param pulumi.Input[str] task_type: Task type.
               Expected value is 'Migrate.SqlServer.SqlDb'.
        :param pulumi.Input['MigrateSqlServerSqlDbTaskInputArgs'] input: Task input
        """
        pulumi.set(__self__, "task_type", 'Migrate.SqlServer.SqlDb')
        if input is not None:
            pulumi.set(__self__, "input", input)

    @property
    @pulumi.getter(name="taskType")
    def task_type(self) -> pulumi.Input[str]:
        """
        Task type.
        Expected value is 'Migrate.SqlServer.SqlDb'.
        """
        return pulumi.get(self, "task_type")

    @task_type.setter
    def task_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "task_type", value)

    @property
    @pulumi.getter
    def input(self) -> Optional[pulumi.Input['MigrateSqlServerSqlDbTaskInputArgs']]:
        """
        Task input
        """
        return pulumi.get(self, "input")

    @input.setter
    def input(self, value: Optional[pulumi.Input['MigrateSqlServerSqlDbTaskInputArgs']]):
        pulumi.set(self, "input", value)


@pulumi.input_type
class MigrationValidationOptionsArgs:
    def __init__(__self__, *,
                 enable_data_integrity_validation: Optional[pulumi.Input[bool]] = None,
                 enable_query_analysis_validation: Optional[pulumi.Input[bool]] = None,
                 enable_schema_validation: Optional[pulumi.Input[bool]] = None):
        """
        Types of validations to run after the migration
        :param pulumi.Input[bool] enable_data_integrity_validation: Allows to perform a checksum based data integrity validation between source and target for the selected database / tables .
        :param pulumi.Input[bool] enable_query_analysis_validation: Allows to perform a quick and intelligent query analysis by retrieving queries from the source database and executes them in the target. The result will have execution statistics for executions in source and target databases for the extracted queries.
        :param pulumi.Input[bool] enable_schema_validation: Allows to compare the schema information between source and target.
        """
        if enable_data_integrity_validation is not None:
            pulumi.set(__self__, "enable_data_integrity_validation", enable_data_integrity_validation)
        if enable_query_analysis_validation is not None:
            pulumi.set(__self__, "enable_query_analysis_validation", enable_query_analysis_validation)
        if enable_schema_validation is not None:
            pulumi.set(__self__, "enable_schema_validation", enable_schema_validation)

    @property
    @pulumi.getter(name="enableDataIntegrityValidation")
    def enable_data_integrity_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        Allows to perform a checksum based data integrity validation between source and target for the selected database / tables .
        """
        return pulumi.get(self, "enable_data_integrity_validation")

    @enable_data_integrity_validation.setter
    def enable_data_integrity_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_data_integrity_validation", value)

    @property
    @pulumi.getter(name="enableQueryAnalysisValidation")
    def enable_query_analysis_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        Allows to perform a quick and intelligent query analysis by retrieving queries from the source database and executes them in the target. The result will have execution statistics for executions in source and target databases for the extracted queries.
        """
        return pulumi.get(self, "enable_query_analysis_validation")

    @enable_query_analysis_validation.setter
    def enable_query_analysis_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_query_analysis_validation", value)

    @property
    @pulumi.getter(name="enableSchemaValidation")
    def enable_schema_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        Allows to compare the schema information between source and target.
        """
        return pulumi.get(self, "enable_schema_validation")

    @enable_schema_validation.setter
    def enable_schema_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_schema_validation", value)


@pulumi.input_type
class ServiceSkuArgs:
    def __init__(__self__, *,
                 capacity: Optional[pulumi.Input[int]] = None,
                 family: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[str]] = None):
        """
        An Azure SKU instance
        :param pulumi.Input[int] capacity: The capacity of the SKU, if it supports scaling
        :param pulumi.Input[str] family: The SKU family, used when the service has multiple performance classes within a tier, such as 'A', 'D', etc. for virtual machines
        :param pulumi.Input[str] name: The unique name of the SKU, such as 'P3'
        :param pulumi.Input[str] size: The size of the SKU, used when the name alone does not denote a service size or when a SKU has multiple performance classes within a family, e.g. 'A1' for virtual machines
        :param pulumi.Input[str] tier: The tier of the SKU, such as 'Free', 'Basic', 'Standard', or 'Premium'
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The capacity of the SKU, if it supports scaling
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def family(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU family, used when the service has multiple performance classes within a tier, such as 'A', 'D', etc. for virtual machines
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The unique name of the SKU, such as 'P3'
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        The size of the SKU, used when the name alone does not denote a service size or when a SKU has multiple performance classes within a family, e.g. 'A1' for virtual machines
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[str]]:
        """
        The tier of the SKU, such as 'Free', 'Basic', 'Standard', or 'Premium'
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class SqlConnectionInfoArgs:
    def __init__(__self__, *,
                 data_source: pulumi.Input[str],
                 type: pulumi.Input[str],
                 additional_settings: Optional[pulumi.Input[str]] = None,
                 authentication: Optional[pulumi.Input['AuthenticationType']] = None,
                 encrypt_connection: Optional[pulumi.Input[bool]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 trust_server_certificate: Optional[pulumi.Input[bool]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        Information for connecting to SQL database server
        :param pulumi.Input[str] data_source: Data source in the format Protocol:MachineName\SQLServerInstanceName,PortNumber
        :param pulumi.Input[str] type: Type of connection info
               Expected value is 'SqlConnectionInfo'.
        :param pulumi.Input[str] additional_settings: Additional connection settings
        :param pulumi.Input['AuthenticationType'] authentication: Authentication type to use for connection
        :param pulumi.Input[bool] encrypt_connection: Whether to encrypt the connection
        :param pulumi.Input[str] password: Password credential.
        :param pulumi.Input[bool] trust_server_certificate: Whether to trust the server certificate
        :param pulumi.Input[str] user_name: User name
        """
        pulumi.set(__self__, "data_source", data_source)
        pulumi.set(__self__, "type", 'SqlConnectionInfo')
        if additional_settings is not None:
            pulumi.set(__self__, "additional_settings", additional_settings)
        if authentication is not None:
            pulumi.set(__self__, "authentication", authentication)
        if encrypt_connection is None:
            encrypt_connection = True
        if encrypt_connection is not None:
            pulumi.set(__self__, "encrypt_connection", encrypt_connection)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if trust_server_certificate is None:
            trust_server_certificate = False
        if trust_server_certificate is not None:
            pulumi.set(__self__, "trust_server_certificate", trust_server_certificate)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="dataSource")
    def data_source(self) -> pulumi.Input[str]:
        """
        Data source in the format Protocol:MachineName\SQLServerInstanceName,PortNumber
        """
        return pulumi.get(self, "data_source")

    @data_source.setter
    def data_source(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_source", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of connection info
        Expected value is 'SqlConnectionInfo'.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="additionalSettings")
    def additional_settings(self) -> Optional[pulumi.Input[str]]:
        """
        Additional connection settings
        """
        return pulumi.get(self, "additional_settings")

    @additional_settings.setter
    def additional_settings(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "additional_settings", value)

    @property
    @pulumi.getter
    def authentication(self) -> Optional[pulumi.Input['AuthenticationType']]:
        """
        Authentication type to use for connection
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: Optional[pulumi.Input['AuthenticationType']]):
        pulumi.set(self, "authentication", value)

    @property
    @pulumi.getter(name="encryptConnection")
    def encrypt_connection(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to encrypt the connection
        """
        return pulumi.get(self, "encrypt_connection")

    @encrypt_connection.setter
    def encrypt_connection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypt_connection", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Password credential.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="trustServerCertificate")
    def trust_server_certificate(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to trust the server certificate
        """
        return pulumi.get(self, "trust_server_certificate")

    @trust_server_certificate.setter
    def trust_server_certificate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "trust_server_certificate", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        User name
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


