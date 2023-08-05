"""
Type annotations for rds service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_rds import RDSClient
    from mypy_boto3_rds.paginator import (
        DescribeCertificatesPaginator,
        DescribeCustomAvailabilityZonesPaginator,
        DescribeDBClusterBacktracksPaginator,
        DescribeDBClusterEndpointsPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstanceAutomatedBackupsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBLogFilesPaginator,
        DescribeDBParameterGroupsPaginator,
        DescribeDBParametersPaginator,
        DescribeDBProxiesPaginator,
        DescribeDBProxyEndpointsPaginator,
        DescribeDBProxyTargetGroupsPaginator,
        DescribeDBProxyTargetsPaginator,
        DescribeDBSecurityGroupsPaginator,
        DescribeDBSnapshotsPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEngineDefaultClusterParametersPaginator,
        DescribeEngineDefaultParametersPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeExportTasksPaginator,
        DescribeGlobalClustersPaginator,
        DescribeInstallationMediaPaginator,
        DescribeOptionGroupOptionsPaginator,
        DescribeOptionGroupsPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
        DescribeReservedDBInstancesPaginator,
        DescribeReservedDBInstancesOfferingsPaginator,
        DescribeSourceRegionsPaginator,
        DownloadDBLogFilePortionPaginator,
    )

    client: RDSClient = boto3.client("rds")

    describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
    describe_custom_availability_zones_paginator: DescribeCustomAvailabilityZonesPaginator = client.get_paginator("describe_custom_availability_zones")
    describe_db_cluster_backtracks_paginator: DescribeDBClusterBacktracksPaginator = client.get_paginator("describe_db_cluster_backtracks")
    describe_db_cluster_endpoints_paginator: DescribeDBClusterEndpointsPaginator = client.get_paginator("describe_db_cluster_endpoints")
    describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
    describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
    describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
    describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
    describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
    describe_db_instance_automated_backups_paginator: DescribeDBInstanceAutomatedBackupsPaginator = client.get_paginator("describe_db_instance_automated_backups")
    describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
    describe_db_log_files_paginator: DescribeDBLogFilesPaginator = client.get_paginator("describe_db_log_files")
    describe_db_parameter_groups_paginator: DescribeDBParameterGroupsPaginator = client.get_paginator("describe_db_parameter_groups")
    describe_db_parameters_paginator: DescribeDBParametersPaginator = client.get_paginator("describe_db_parameters")
    describe_db_proxies_paginator: DescribeDBProxiesPaginator = client.get_paginator("describe_db_proxies")
    describe_db_proxy_endpoints_paginator: DescribeDBProxyEndpointsPaginator = client.get_paginator("describe_db_proxy_endpoints")
    describe_db_proxy_target_groups_paginator: DescribeDBProxyTargetGroupsPaginator = client.get_paginator("describe_db_proxy_target_groups")
    describe_db_proxy_targets_paginator: DescribeDBProxyTargetsPaginator = client.get_paginator("describe_db_proxy_targets")
    describe_db_security_groups_paginator: DescribeDBSecurityGroupsPaginator = client.get_paginator("describe_db_security_groups")
    describe_db_snapshots_paginator: DescribeDBSnapshotsPaginator = client.get_paginator("describe_db_snapshots")
    describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
    describe_engine_default_cluster_parameters_paginator: DescribeEngineDefaultClusterParametersPaginator = client.get_paginator("describe_engine_default_cluster_parameters")
    describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
    describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
    describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
    describe_installation_media_paginator: DescribeInstallationMediaPaginator = client.get_paginator("describe_installation_media")
    describe_option_group_options_paginator: DescribeOptionGroupOptionsPaginator = client.get_paginator("describe_option_group_options")
    describe_option_groups_paginator: DescribeOptionGroupsPaginator = client.get_paginator("describe_option_groups")
    describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
    describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
    describe_reserved_db_instances_paginator: DescribeReservedDBInstancesPaginator = client.get_paginator("describe_reserved_db_instances")
    describe_reserved_db_instances_offerings_paginator: DescribeReservedDBInstancesOfferingsPaginator = client.get_paginator("describe_reserved_db_instances_offerings")
    describe_source_regions_paginator: DescribeSourceRegionsPaginator = client.get_paginator("describe_source_regions")
    download_db_log_file_portion_paginator: DownloadDBLogFilePortionPaginator = client.get_paginator("download_db_log_file_portion")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import SourceTypeType
from .type_defs import (
    CertificateMessageTypeDef,
    CustomAvailabilityZoneMessageTypeDef,
    DBClusterBacktrackMessageTypeDef,
    DBClusterEndpointMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceAutomatedBackupMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBParameterGroupDetailsTypeDef,
    DBParameterGroupsMessageTypeDef,
    DBSecurityGroupMessageTypeDef,
    DBSnapshotMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DescribeDBLogFilesResponseTypeDef,
    DescribeDBProxiesResponseTypeDef,
    DescribeDBProxyEndpointsResponseTypeDef,
    DescribeDBProxyTargetGroupsResponseTypeDef,
    DescribeDBProxyTargetsResponseTypeDef,
    DescribeEngineDefaultClusterParametersResultTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DownloadDBLogFilePortionDetailsTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    ExportTasksMessageTypeDef,
    FilterTypeDef,
    GlobalClustersMessageTypeDef,
    InstallationMediaMessageTypeDef,
    OptionGroupOptionsMessageTypeDef,
    OptionGroupsTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PaginatorConfigTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
    ReservedDBInstanceMessageTypeDef,
    ReservedDBInstancesOfferingMessageTypeDef,
    SourceRegionMessageTypeDef,
)

__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeCustomAvailabilityZonesPaginator",
    "DescribeDBClusterBacktracksPaginator",
    "DescribeDBClusterEndpointsPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstanceAutomatedBackupsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBLogFilesPaginator",
    "DescribeDBParameterGroupsPaginator",
    "DescribeDBParametersPaginator",
    "DescribeDBProxiesPaginator",
    "DescribeDBProxyEndpointsPaginator",
    "DescribeDBProxyTargetGroupsPaginator",
    "DescribeDBProxyTargetsPaginator",
    "DescribeDBSecurityGroupsPaginator",
    "DescribeDBSnapshotsPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEngineDefaultClusterParametersPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeInstallationMediaPaginator",
    "DescribeOptionGroupOptionsPaginator",
    "DescribeOptionGroupsPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
    "DescribeReservedDBInstancesPaginator",
    "DescribeReservedDBInstancesOfferingsPaginator",
    "DescribeSourceRegionsPaginator",
    "DownloadDBLogFilePortionPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeCertificates)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describecertificatespaginator)
    """

    def paginate(
        self,
        *,
        CertificateIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeCertificates.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describecertificatespaginator)
        """


class DescribeCustomAvailabilityZonesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeCustomAvailabilityZones)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describecustomavailabilityzonespaginator)
    """

    def paginate(
        self,
        *,
        CustomAvailabilityZoneId: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[CustomAvailabilityZoneMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeCustomAvailabilityZones.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describecustomavailabilityzonespaginator)
        """


class DescribeDBClusterBacktracksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterBacktracks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterbacktrackspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str,
        BacktrackIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBClusterBacktrackMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterBacktracks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterbacktrackspaginator)
        """


class DescribeDBClusterEndpointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterEndpoints)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterendpointspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = None,
        DBClusterEndpointIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBClusterEndpointMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterEndpoints.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterendpointspaginator)
        """


class DescribeDBClusterParameterGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameterGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterparametergroupspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterParameterGroupName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterparametergroupspaginator)
        """


class DescribeDBClusterParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterParameterGroupName: str,
        Source: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterparameterspaginator)
        """


class DescribeDBClusterSnapshotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterSnapshots)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclustersnapshotspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = None,
        DBClusterSnapshotIdentifier: str = None,
        SnapshotType: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        IncludeShared: bool = None,
        IncludePublic: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclustersnapshotspaginator)
        """


class DescribeDBClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        IncludeShared: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBClusters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterspaginator)
        """


class DescribeDBEngineVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBEngineVersions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbengineversionspaginator)
    """

    def paginate(
        self,
        *,
        Engine: str = None,
        EngineVersion: str = None,
        DBParameterGroupFamily: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        DefaultOnly: bool = None,
        ListSupportedCharacterSets: bool = None,
        ListSupportedTimezones: bool = None,
        IncludeAll: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBEngineVersions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbengineversionspaginator)
        """


class DescribeDBInstanceAutomatedBackupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBInstanceAutomatedBackups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbinstanceautomatedbackupspaginator)
    """

    def paginate(
        self,
        *,
        DbiResourceId: str = None,
        DBInstanceIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        DBInstanceAutomatedBackupsArn: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBInstanceAutomatedBackupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBInstanceAutomatedBackups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbinstanceautomatedbackupspaginator)
        """


class DescribeDBInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBInstances)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbinstancespaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBInstances.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbinstancespaginator)
        """


class DescribeDBLogFilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBLogFiles)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedblogfilespaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str,
        FilenameContains: str = None,
        FileLastWritten: int = None,
        FileSize: int = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DescribeDBLogFilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBLogFiles.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedblogfilespaginator)
        """


class DescribeDBParameterGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBParameterGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbparametergroupspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBParameterGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbparametergroupspaginator)
        """


class DescribeDBParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBParameters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupName: str,
        Source: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBParameters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbparameterspaginator)
        """


class DescribeDBProxiesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxies)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxiespaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DescribeDBProxiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxies.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxiespaginator)
        """


class DescribeDBProxyEndpointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxyEndpoints)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxyendpointspaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str = None,
        DBProxyEndpointName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DescribeDBProxyEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxyEndpoints.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxyendpointspaginator)
        """


class DescribeDBProxyTargetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargetGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxytargetgroupspaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DescribeDBProxyTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargetGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxytargetgroupspaginator)
        """


class DescribeDBProxyTargetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxytargetspaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DescribeDBProxyTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxytargetspaginator)
        """


class DescribeDBSecurityGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBSecurityGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsecuritygroupspaginator)
    """

    def paginate(
        self,
        *,
        DBSecurityGroupName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBSecurityGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsecuritygroupspaginator)
        """


class DescribeDBSnapshotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBSnapshots)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsnapshotspaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str = None,
        DBSnapshotIdentifier: str = None,
        SnapshotType: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        IncludeShared: bool = None,
        IncludePublic: bool = None,
        DbiResourceId: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBSnapshots.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsnapshotspaginator)
        """


class DescribeDBSubnetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBSubnetGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsubnetgroupspaginator)
    """

    def paginate(
        self,
        *,
        DBSubnetGroupName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeDBSubnetGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsubnetgroupspaginator)
        """


class DescribeEngineDefaultClusterParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultClusterParameters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeenginedefaultclusterparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DescribeEngineDefaultClusterParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultClusterParameters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeenginedefaultclusterparameterspaginator)
        """


class DescribeEngineDefaultParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultParameters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeenginedefaultparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeenginedefaultparameterspaginator)
        """


class DescribeEventSubscriptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEventSubscriptions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeeventsubscriptionspaginator)
    """

    def paginate(
        self,
        *,
        SubscriptionName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEventSubscriptions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeeventsubscriptionspaginator)
        """


class DescribeEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEvents)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeeventspaginator)
    """

    def paginate(
        self,
        *,
        SourceIdentifier: str = None,
        SourceType: SourceTypeType = None,
        StartTime: Union[datetime, str] = None,
        EndTime: Union[datetime, str] = None,
        Duration: int = None,
        EventCategories: Sequence[str] = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeeventspaginator)
        """


class DescribeExportTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeExportTasks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeexporttaskspaginator)
    """

    def paginate(
        self,
        *,
        ExportTaskIdentifier: str = None,
        SourceArn: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ExportTasksMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeExportTasks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeexporttaskspaginator)
        """


class DescribeGlobalClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeGlobalClusters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeglobalclusterspaginator)
    """

    def paginate(
        self,
        *,
        GlobalClusterIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeGlobalClusters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeglobalclusterspaginator)
        """


class DescribeInstallationMediaPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeInstallationMedia)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeinstallationmediapaginator)
    """

    def paginate(
        self,
        *,
        InstallationMediaId: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[InstallationMediaMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeInstallationMedia.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeinstallationmediapaginator)
        """


class DescribeOptionGroupOptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeOptionGroupOptions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeoptiongroupoptionspaginator)
    """

    def paginate(
        self,
        *,
        EngineName: str,
        MajorEngineVersion: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[OptionGroupOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeOptionGroupOptions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeoptiongroupoptionspaginator)
        """


class DescribeOptionGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeOptionGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeoptiongroupspaginator)
    """

    def paginate(
        self,
        *,
        OptionGroupName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        EngineName: str = None,
        MajorEngineVersion: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[OptionGroupsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeOptionGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeoptiongroupspaginator)
        """


class DescribeOrderableDBInstanceOptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeOrderableDBInstanceOptions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeorderabledbinstanceoptionspaginator)
    """

    def paginate(
        self,
        *,
        Engine: str,
        EngineVersion: str = None,
        DBInstanceClass: str = None,
        LicenseModel: str = None,
        AvailabilityZoneGroup: str = None,
        Vpc: bool = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeorderabledbinstanceoptionspaginator)
        """


class DescribePendingMaintenanceActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribePendingMaintenanceActions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describependingmaintenanceactionspaginator)
    """

    def paginate(
        self,
        *,
        ResourceIdentifier: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describependingmaintenanceactionspaginator)
        """


class DescribeReservedDBInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstances)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describereserveddbinstancespaginator)
    """

    def paginate(
        self,
        *,
        ReservedDBInstanceId: str = None,
        ReservedDBInstancesOfferingId: str = None,
        DBInstanceClass: str = None,
        Duration: str = None,
        ProductDescription: str = None,
        OfferingType: str = None,
        MultiAZ: bool = None,
        LeaseId: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ReservedDBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstances.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describereserveddbinstancespaginator)
        """


class DescribeReservedDBInstancesOfferingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstancesOfferings)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describereserveddbinstancesofferingspaginator)
    """

    def paginate(
        self,
        *,
        ReservedDBInstancesOfferingId: str = None,
        DBInstanceClass: str = None,
        Duration: str = None,
        ProductDescription: str = None,
        OfferingType: str = None,
        MultiAZ: bool = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ReservedDBInstancesOfferingMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstancesOfferings.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describereserveddbinstancesofferingspaginator)
        """


class DescribeSourceRegionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeSourceRegions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describesourceregionspaginator)
    """

    def paginate(
        self,
        *,
        RegionName: str = None,
        Filters: Sequence["FilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[SourceRegionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DescribeSourceRegions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describesourceregionspaginator)
        """


class DownloadDBLogFilePortionPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DownloadDBLogFilePortion)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#downloaddblogfileportionpaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str,
        LogFileName: str,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[DownloadDBLogFilePortionDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/rds.html#RDS.Paginator.DownloadDBLogFilePortion.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#downloaddblogfileportionpaginator)
        """
