"""
Type annotations for importexport service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_importexport import ImportExportClient
    from mypy_boto3_importexport.paginator import (
        ListJobsPaginator,
    )

    client: ImportExportClient = boto3.client("importexport")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListJobsOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListJobsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/importexport.html#ImportExport.Paginator.ListJobs)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators.html#listjobspaginator)
    """

    def paginate(
        self, *, APIVersion: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> _PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.47/reference/services/importexport.html#ImportExport.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators.html#listjobspaginator)
        """
