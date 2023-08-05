"""
Type annotations for inspector service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_inspector import InspectorClient
    from mypy_boto3_inspector.paginator import (
        ListAssessmentRunAgentsPaginator,
        ListAssessmentRunsPaginator,
        ListAssessmentTargetsPaginator,
        ListAssessmentTemplatesPaginator,
        ListEventSubscriptionsPaginator,
        ListExclusionsPaginator,
        ListFindingsPaginator,
        ListRulesPackagesPaginator,
        PreviewAgentsPaginator,
    )

    client: InspectorClient = boto3.client("inspector")

    list_assessment_run_agents_paginator: ListAssessmentRunAgentsPaginator = client.get_paginator("list_assessment_run_agents")
    list_assessment_runs_paginator: ListAssessmentRunsPaginator = client.get_paginator("list_assessment_runs")
    list_assessment_targets_paginator: ListAssessmentTargetsPaginator = client.get_paginator("list_assessment_targets")
    list_assessment_templates_paginator: ListAssessmentTemplatesPaginator = client.get_paginator("list_assessment_templates")
    list_event_subscriptions_paginator: ListEventSubscriptionsPaginator = client.get_paginator("list_event_subscriptions")
    list_exclusions_paginator: ListExclusionsPaginator = client.get_paginator("list_exclusions")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_rules_packages_paginator: ListRulesPackagesPaginator = client.get_paginator("list_rules_packages")
    preview_agents_paginator: PreviewAgentsPaginator = client.get_paginator("preview_agents")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    AgentFilterTypeDef,
    AssessmentRunFilterTypeDef,
    AssessmentTargetFilterTypeDef,
    AssessmentTemplateFilterTypeDef,
    FindingFilterTypeDef,
    ListAssessmentRunAgentsResponseTypeDef,
    ListAssessmentRunsResponseTypeDef,
    ListAssessmentTargetsResponseTypeDef,
    ListAssessmentTemplatesResponseTypeDef,
    ListEventSubscriptionsResponseTypeDef,
    ListExclusionsResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListRulesPackagesResponseTypeDef,
    PaginatorConfigTypeDef,
    PreviewAgentsResponseTypeDef,
)

__all__ = (
    "ListAssessmentRunAgentsPaginator",
    "ListAssessmentRunsPaginator",
    "ListAssessmentTargetsPaginator",
    "ListAssessmentTemplatesPaginator",
    "ListEventSubscriptionsPaginator",
    "ListExclusionsPaginator",
    "ListFindingsPaginator",
    "ListRulesPackagesPaginator",
    "PreviewAgentsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssessmentRunAgentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRunAgents)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmentrunagentspaginator)
    """

    def paginate(
        self,
        *,
        assessmentRunArn: str,
        filter: "AgentFilterTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListAssessmentRunAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRunAgents.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmentrunagentspaginator)
        """


class ListAssessmentRunsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRuns)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmentrunspaginator)
    """

    def paginate(
        self,
        *,
        assessmentTemplateArns: Sequence[str] = None,
        filter: "AssessmentRunFilterTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListAssessmentRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRuns.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmentrunspaginator)
        """


class ListAssessmentTargetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTargets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmenttargetspaginator)
    """

    def paginate(
        self,
        *,
        filter: "AssessmentTargetFilterTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListAssessmentTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTargets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmenttargetspaginator)
        """


class ListAssessmentTemplatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTemplates)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmenttemplatespaginator)
    """

    def paginate(
        self,
        *,
        assessmentTargetArns: Sequence[str] = None,
        filter: "AssessmentTemplateFilterTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListAssessmentTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTemplates.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listassessmenttemplatespaginator)
        """


class ListEventSubscriptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListEventSubscriptions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listeventsubscriptionspaginator)
    """

    def paginate(
        self, *, resourceArn: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListEventSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListEventSubscriptions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listeventsubscriptionspaginator)
        """


class ListExclusionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListExclusions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listexclusionspaginator)
    """

    def paginate(
        self, *, assessmentRunArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListExclusionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListExclusions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listexclusionspaginator)
        """


class ListFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListFindings)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listfindingspaginator)
    """

    def paginate(
        self,
        *,
        assessmentRunArns: Sequence[str] = None,
        filter: "FindingFilterTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListFindings.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listfindingspaginator)
        """


class ListRulesPackagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListRulesPackages)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listrulespackagespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListRulesPackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.ListRulesPackages.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#listrulespackagespaginator)
        """


class PreviewAgentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.PreviewAgents)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#previewagentspaginator)
    """

    def paginate(
        self, *, previewAgentsArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[PreviewAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/inspector.html#Inspector.Paginator.PreviewAgents.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators.html#previewagentspaginator)
        """
