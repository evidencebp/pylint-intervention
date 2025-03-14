from __future__ import annotations

from typing import (TYPE_CHECKING,
                    Any,
                    Dict,
                    Iterable,
                    Optional)

from couchbase.exceptions import InvalidArgumentException
from couchbase.management.logic.analytics_logic import AnalyticsEncryptionLevel  # noqa: F401
from couchbase.management.logic.analytics_logic import AnalyticsLinkType  # noqa: F401
from couchbase.management.logic.analytics_logic import AzureBlobExternalAnalyticsLink  # noqa: F401
from couchbase.management.logic.analytics_logic import CouchbaseAnalyticsEncryptionSettings  # noqa: F401
from couchbase.management.logic.analytics_logic import CouchbaseRemoteAnalyticsLink  # noqa: F401
from couchbase.management.logic.analytics_logic import S3ExternalAnalyticsLink  # noqa: F401
from couchbase.management.logic.analytics_logic import (AnalyticsDataset,
                                                        AnalyticsDataType,
                                                        AnalyticsIndex,
                                                        AnalyticsLink,
                                                        AnalyticsManagerLogic)
from couchbase.management.logic.wrappers import AnalyticsMgmtWrapper

if TYPE_CHECKING:
    from couchbase.management.options import (ConnectLinkOptions,
                                              CreateAnalyticsIndexOptions,
                                              CreateDatasetOptions,
                                              CreateDataverseOptions,
                                              CreateLinkAnalyticsOptions,
                                              DisconnectLinkOptions,
                                              DropAnalyticsIndexOptions,
                                              DropDatasetOptions,
                                              DropDataverseOptions,
                                              DropLinkAnalyticsOptions,
                                              GetAllAnalyticsIndexesOptions,
                                              GetAllDatasetOptions,
                                              GetLinksAnalyticsOptions,
                                              GetPendingMutationsOptions,
                                              ReplaceLinkAnalyticsOptions)


class AnalyticsIndexManager(AnalyticsManagerLogic):

    def __init__(self, connection):
        super().__init__(connection)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def create_dataverse(self,
                         dataverse_name,    # type: str
                         options=None,      # type: Optional[CreateDataverseOptions]
                         **kwargs           # type: Dict[str, Any]
                         ) -> None:

        if not isinstance(dataverse_name, str):
            raise ValueError("dataverse_name must be provided when creating an analytics dataverse.")

        return super().create_dataverse(dataverse_name, options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def drop_dataverse(self,
                       dataverse_name,    # type: str
                       options=None,      # type: Optional[DropDataverseOptions]
                       **kwargs           # type: Dict[str, Any]
                       ) -> None:

        if not isinstance(dataverse_name, str):
            raise ValueError("dataverse_name must be provided when dropping an analytics dataverse.")

        return super().drop_dataverse(dataverse_name, options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def create_dataset(self,
                       dataset_name,    # type: str
                       bucket_name,     # type: str
                       options=None,    # type: Optional[CreateDatasetOptions]
                       **kwargs         # type: Dict[str, Any]
                       ) -> None:

        if not isinstance(dataset_name, str):
            raise ValueError("dataset_name must be provided when creating an analytics dataset.")

        if not isinstance(bucket_name, str):
            raise ValueError("bucket_name must be provided when creating an analytics dataset.")

        return super().create_dataset(dataset_name, bucket_name, options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def drop_dataset(self,
                     dataset_name,  # type: str
                     options=None,  # type: Optional[DropDatasetOptions]
                     **kwargs       # type: Dict[str, Any]
                     ) -> None:

        if not isinstance(dataset_name, str):
            raise ValueError("dataset_name must be provided when dropping an analytics dataset.")

        return super().drop_dataset(dataset_name, options, **kwargs)

    @AnalyticsMgmtWrapper.block(AnalyticsDataset, AnalyticsManagerLogic._ERROR_MAPPING)
    def get_all_datasets(self,
                         options=None,   # type: Optional[GetAllDatasetOptions]
                         **kwargs   # type: Dict[str, Any]
                         ) -> Iterable[AnalyticsDataset]:

        return super().get_all_datasets(options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def create_index(self,
                     index_name,    # type: str
                     dataset_name,  # type: str
                     fields,        # type: Dict[str, AnalyticsDataType]
                     options=None,  # type: Optional[CreateAnalyticsIndexOptions]
                     **kwargs       # type: Dict[str, Any]
                     ) -> None:

        if not isinstance(index_name, str):
            raise ValueError("index_name must be provided when creating an analytics index.")

        if not isinstance(dataset_name, str):
            raise ValueError("dataset_name must be provided when creating an analytics index.")

        if fields is not None:
            if not isinstance(fields, dict):
                raise ValueError("fields must be provided when creating an analytics index.")

            if not all(map(lambda v: isinstance(v, AnalyticsDataType), fields.values())):
                raise InvalidArgumentException("fields must all be an AnalyticsDataType.")

        return super().create_index(index_name, dataset_name, fields, options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def drop_index(self,
                   index_name,    # type: str
                   dataset_name,  # type: str
                   options=None,  # type: Optional[DropAnalyticsIndexOptions]
                   **kwargs       # type: Dict[str, Any]
                   ) -> None:

        if not isinstance(index_name, str):
            raise ValueError("index_name must be provided when dropping an analytics index.")

        if not isinstance(dataset_name, str):
            raise ValueError("dataset_name must be provided when dropping an analytics index.")

        return super().drop_index(index_name, dataset_name, options, **kwargs)

    @AnalyticsMgmtWrapper.block(AnalyticsIndex, AnalyticsManagerLogic._ERROR_MAPPING)
    def get_all_indexes(self,
                        options=None,   # type: Optional[GetAllAnalyticsIndexesOptions]
                        **kwargs   # type: Dict[str, Any]
                        ) -> Iterable[AnalyticsIndex]:

        return super().get_all_indexes(options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def connect_link(self,
                     options=None,  # type: Optional[ConnectLinkOptions]
                     **kwargs   # type: Dict[str, Any]
                     ) -> None:
        return super().connect_link(options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def disconnect_link(self,
                        options=None,  # type: Optional[DisconnectLinkOptions]
                        **kwargs   # type: Dict[str, Any]
                        ) -> None:
        return super().disconnect_link(options, **kwargs)

    @AnalyticsMgmtWrapper.block(dict, AnalyticsManagerLogic._ERROR_MAPPING)
    def get_pending_mutations(self,
                              options=None,     # type: Optional[GetPendingMutationsOptions]
                              **kwargs     # type: Dict[str, Any]
                              ) -> Dict[str, int]:

        return super().get_pending_mutations(options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def create_link(
        self,
        link,  # type: AnalyticsLink
        options=None,     # type: Optional[CreateLinkAnalyticsOptions]
        **kwargs           # type: Dict[str, Any]
    ) -> None:
        return super().create_link(link, options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def replace_link(
        self,
        link,  # type: AnalyticsLink
        options=None,     # type: Optional[ReplaceLinkAnalyticsOptions]
        **kwargs           # type: Dict[str, Any]
    ) -> None:
        return super().replace_link(link, options, **kwargs)

    @AnalyticsMgmtWrapper.block(None, AnalyticsManagerLogic._ERROR_MAPPING)
    def drop_link(
        self,
        link_name,  # type: str
        dataverse_name,  # type: str
        options=None,     # type: Optional[DropLinkAnalyticsOptions]
        **kwargs        # type: Dict[str, Any]
    ) -> None:

        if not isinstance(link_name, str):
            raise ValueError("link_name must be provided when dropping an analytics link.")

        if not isinstance(dataverse_name, str):
            raise ValueError("dataverse_name must be provided when dropping an analytics link.")

        return super().drop_link(link_name, dataverse_name, options, **kwargs)

    @AnalyticsMgmtWrapper.block((CouchbaseRemoteAnalyticsLink,
                                 S3ExternalAnalyticsLink,
                                 AzureBlobExternalAnalyticsLink), AnalyticsManagerLogic._ERROR_MAPPING)
    def get_links(
        self,
        options=None,  # type: Optional[GetLinksAnalyticsOptions]
        **kwargs        # type: Dict[str, Any]
    ) -> Iterable[AnalyticsLink]:
        return super().get_links(options, **kwargs)
