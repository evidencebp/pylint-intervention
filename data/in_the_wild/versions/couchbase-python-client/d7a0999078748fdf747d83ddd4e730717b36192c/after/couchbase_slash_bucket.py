from typing import (TYPE_CHECKING,
                    Any,
                    Dict)

from couchbase.collection import Collection
from couchbase.exceptions import ErrorMapper
from couchbase.exceptions import exception as BaseCouchbaseException
from couchbase.logic import BlockingWrapper
from couchbase.logic.bucket import BucketLogic
from couchbase.logic.supportability import Supportability
from couchbase.management.collections import CollectionManager
from couchbase.management.views import ViewIndexManager
from couchbase.result import PingResult, ViewResult
from couchbase.scope import Scope
from couchbase.views import ViewQuery, ViewRequest

if TYPE_CHECKING:
    from couchbase.cluster import Cluster
    from couchbase.options import PingOptions, ViewOptions


class Bucket(BucketLogic):
    """Create a Couchbase Bucket instance.

    Exposes the operations which are available to be performed against a bucket. Namely the ability to
    access to Collections as well as performing management operations against the bucket.

    Args:
        cluster (:class:`~.Cluster`): A :class:`~.Cluster` instance.
        bucket_name (str): Name of the bucket.

    Raises:
        :class:`~.exceptions.BucketNotFoundException`: If provided `bucket_name` cannot be found.

    """

    def __init__(self,
                 cluster,  # type: Cluster
                 bucket_name  # type: str
                 ):
        super().__init__(cluster, bucket_name)
        self._open_bucket()

    @BlockingWrapper.block(True)
    def _open_bucket(self, **kwargs):
        ret = super()._open_or_close_bucket(open_bucket=True, **kwargs)
        if isinstance(ret, BaseCouchbaseException):
            raise ErrorMapper.build_exception(ret)
        self._set_connected(ret)

    @BlockingWrapper.block(True)
    def _close_bucket(self, **kwargs):
        super()._open_or_close_bucket(open_bucket=False, **kwargs)
        self._destroy_connection()

    def close(self):
        """Shuts down this bucket instance. Cleaning up all resources associated with it.

        .. warning::
            Use of this method is almost *always* unnecessary.  Bucket resources should be cleaned
            up once the bucket instance falls out of scope.  However, in some applications tuning resources
            is necessary and in those types of applications, this method might be beneficial.

        """
        # only close if we are connected
        if self.connected:
            self._close_bucket()

    def default_scope(self) -> Scope:
        """Creates a :class:`~.scope.Scope` instance of the default scope.

        Returns:
            :class:`~.scope.Scope`: A :class:`~.scope.Scope` instance of the default scope.

        """
        return self.scope(Scope.default_name())

    def scope(self, name  # type: str
              ) -> Scope:
        """Creates a :class:`~.scope.Scope` instance of the specified scope.

        Args:
            name (str): Name of the scope to reference.

        Returns:
            :class:`~.scope.Scope`: A :class:`~.scope.Scope` instance of the specified scope.

        """
        return Scope(self, name)

    def collection(self, collection_name  # type: str
                   ) -> Collection:
        """Creates a :class:`~.collection.Collection` instance of the specified collection.

        Args:
            collection_name (str): Name of the collection to reference.

        Returns:
            :class:`~.collection.Collection`: A :class:`~.collection.Collection` instance of the specified collection.

        """
        scope = self.default_scope()
        return scope.collection(collection_name)

    def default_collection(self) -> Collection:
        """Creates a :class:`~.collection.Collection` instance of the default collection.

        Returns:
            :class:`~.collection.Collection`: A :class:`~.collection.Collection` instance of the default collection.
        """
        scope = self.default_scope()
        return scope.collection(Collection.default_name())

    @BlockingWrapper.block(PingResult)
    def ping(self,
             *opts,  # type: PingOptions
             **kwargs  # type: Dict[str, Any]
             ) -> PingResult:
        """Performs a ping operation against the bucket.

        The ping operation pings the services which are specified
        (or all services if none are specified). Returns a report which describes the outcome of
        the ping operations which were performed.

        Args:
            opts (:class:`~.options.PingOptions`): Optional parameters for this operation.

        Returns:
            :class:`~.result.PingResult`: A report which describes the outcome of the ping operations
            which were performed.

        """
        return super().ping(*opts, **kwargs)

    def view_query(self,
                   design_doc,      # type: str
                   view_name,       # type: str
                   *view_options,   # type: ViewOptions
                   **kwargs         # type: Dict[str, Any]
                   ) -> ViewResult:
        """Executes a View query against the bucket.

        .. note::

            The query is executed lazily in that it is executed once iteration over the
            :class:`~.result.ViewResult` begins.

        .. seealso::
            * :class:`~.management.ViewIndexManager`: for how to manage query indexes

        Args:
            design_doc (str): The name of the design document containing the view to execute.
            view_name (str): The name of the view to execute.
            view_options (:class:`~.options.ViewOptions`): Optional parameters for the view query operation.
            **kwargs (Dict[str, Any]): keyword arguments that can be used in place or to
                override provided :class:`~.options.ViewOptions`

        Returns:
            :class:`~.result.ViewResult`: An instance of a :class:`~.result.ViewResult` which
            provides access to iterate over the query results and access metadata about the query.

        Examples:
            Simple view query::

                from couchbase.management.views import DesignDocumentNamespace

                # ... other code ...

                view_result = bucket.view_query('ddoc-name',
                                                'view-name',
                                                limit=10,
                                                namespace=DesignDocumentNamespace.DEVELOPMENT)

                for row in view_result.rows():
                    print(f'Found row: {row}')

        """

        query = ViewQuery.create_view_query_object(
            self.name, design_doc, view_name, *view_options, **kwargs
        )
        return ViewResult(ViewRequest.generate_view_request(self.connection,
                                                            query.as_encodable(),
                                                            default_serializer=self.default_serializer))

    def collections(self) -> CollectionManager:
        """
        Get a :class:`.~.CollectionManager` which can be used to manage the scopes and collections
        of this bucket.

        Returns:
            :class:`~.CollectionManager`: A :class:`~.CollectionManager` instance.
        """
        return CollectionManager(self.connection, self.name)

    def view_indexes(self) -> ViewIndexManager:
        """
        Get a :class:`~.ViewIndexManager` which can be used to manage the view design documents
        and views of this bucket.

        Returns:
            :class:`~.ViewIndexManager`: A :class:`~.ViewIndexManager` instance.
        """
        return ViewIndexManager(self.connection, self.name)


"""
** DEPRECATION NOTICE **

The classes below are deprecated for 3.x compatibility.  They should not be used.
Instead use:
    * All options should be imported from `couchbase.options`.
    * All view Enums should be imported from `couchbase.views`.

"""

from couchbase.logic.options import PingOptionsBase  # nopep8 # isort:skip # noqa: E402
from couchbase.logic.options import ViewOptionsBase  # nopep8 # isort:skip # noqa: E402


@Supportability.import_deprecated('couchbase.bucket', 'couchbase.options')
class PingOptions(PingOptionsBase):  # noqa: F811
    pass


@Supportability.import_deprecated('couchbase.bucket', 'couchbase.options')
class ViewOptions(ViewOptionsBase):  # noqa: F811
    pass


from couchbase.views import ViewScanConsistency  # nopep8 # isort:skip # noqa: E402, F401
from couchbase.views import ViewOrdering  # nopep8 # isort:skip # noqa: E402, F401
from couchbase.views import ViewErrorMode  # nopep8 # isort:skip # noqa: E402, F401
