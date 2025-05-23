# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation as ga_operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.aiplatform_v1beta1.services.job_service import pagers
from google.cloud.aiplatform_v1beta1.types import batch_prediction_job
from google.cloud.aiplatform_v1beta1.types import (
    batch_prediction_job as gca_batch_prediction_job,
)
from google.cloud.aiplatform_v1beta1.types import completion_stats
from google.cloud.aiplatform_v1beta1.types import custom_job
from google.cloud.aiplatform_v1beta1.types import custom_job as gca_custom_job
from google.cloud.aiplatform_v1beta1.types import data_labeling_job
from google.cloud.aiplatform_v1beta1.types import (
    data_labeling_job as gca_data_labeling_job,
)
from google.cloud.aiplatform_v1beta1.types import hyperparameter_tuning_job
from google.cloud.aiplatform_v1beta1.types import (
    hyperparameter_tuning_job as gca_hyperparameter_tuning_job,
)
from google.cloud.aiplatform_v1beta1.types import job_service
from google.cloud.aiplatform_v1beta1.types import job_state
from google.cloud.aiplatform_v1beta1.types import machine_resources
from google.cloud.aiplatform_v1beta1.types import manual_batch_tuning_parameters
from google.cloud.aiplatform_v1beta1.types import operation as gca_operation
from google.cloud.aiplatform_v1beta1.types import study
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore
from google.type import money_pb2 as money  # type: ignore

from .transports.base import JobServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import JobServiceGrpcTransport
from .transports.grpc_asyncio import JobServiceGrpcAsyncIOTransport


class JobServiceClientMeta(type):
    """Metaclass for the JobService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[JobServiceTransport]]
    _transport_registry["grpc"] = JobServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = JobServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[JobServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class JobServiceClient(metaclass=JobServiceClientMeta):
    """A service for creating and managing AI Platform's jobs."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "aiplatform.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def batch_prediction_job_path(
        project: str, location: str, batch_prediction_job: str,
    ) -> str:
        """Return a fully-qualified batch_prediction_job string."""
        return "projects/{project}/locations/{location}/batchPredictionJobs/{batch_prediction_job}".format(
            project=project,
            location=location,
            batch_prediction_job=batch_prediction_job,
        )

    @staticmethod
    def parse_batch_prediction_job_path(path: str) -> Dict[str, str]:
        """Parse a batch_prediction_job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/batchPredictionJobs/(?P<batch_prediction_job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def custom_job_path(project: str, location: str, custom_job: str,) -> str:
        """Return a fully-qualified custom_job string."""
        return "projects/{project}/locations/{location}/customJobs/{custom_job}".format(
            project=project, location=location, custom_job=custom_job,
        )

    @staticmethod
    def parse_custom_job_path(path: str) -> Dict[str, str]:
        """Parse a custom_job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/customJobs/(?P<custom_job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def data_labeling_job_path(
        project: str, location: str, data_labeling_job: str,
    ) -> str:
        """Return a fully-qualified data_labeling_job string."""
        return "projects/{project}/locations/{location}/dataLabelingJobs/{data_labeling_job}".format(
            project=project, location=location, data_labeling_job=data_labeling_job,
        )

    @staticmethod
    def parse_data_labeling_job_path(path: str) -> Dict[str, str]:
        """Parse a data_labeling_job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/dataLabelingJobs/(?P<data_labeling_job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def hyperparameter_tuning_job_path(
        project: str, location: str, hyperparameter_tuning_job: str,
    ) -> str:
        """Return a fully-qualified hyperparameter_tuning_job string."""
        return "projects/{project}/locations/{location}/hyperparameterTuningJobs/{hyperparameter_tuning_job}".format(
            project=project,
            location=location,
            hyperparameter_tuning_job=hyperparameter_tuning_job,
        )

    @staticmethod
    def parse_hyperparameter_tuning_job_path(path: str) -> Dict[str, str]:
        """Parse a hyperparameter_tuning_job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/hyperparameterTuningJobs/(?P<hyperparameter_tuning_job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, JobServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the job service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.JobServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (client_options_lib.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, JobServiceTransport):
            # transport is a JobServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                ssl_channel_credentials=ssl_credentials,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_custom_job(
        self,
        request: job_service.CreateCustomJobRequest = None,
        *,
        parent: str = None,
        custom_job: gca_custom_job.CustomJob = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_custom_job.CustomJob:
        r"""Creates a CustomJob. A created CustomJob right away
        will be attempted to be run.

        Args:
            request (:class:`~.job_service.CreateCustomJobRequest`):
                The request object. Request message for
                [JobService.CreateCustomJob][google.cloud.aiplatform.v1beta1.JobService.CreateCustomJob].
            parent (:class:`str`):
                Required. The resource name of the Location to create
                the CustomJob in. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_job (:class:`~.gca_custom_job.CustomJob`):
                Required. The CustomJob to create.
                This corresponds to the ``custom_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gca_custom_job.CustomJob:
                Represents a job that runs custom
                workloads such as a Docker container or
                a Python package. A CustomJob can have
                multiple worker pools and each worker
                pool can have its own machine and input
                spec. A CustomJob will be cleaned up
                once the job enters terminal state
                (failed or succeeded).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, custom_job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CreateCustomJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CreateCustomJobRequest):
            request = job_service.CreateCustomJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if custom_job is not None:
                request.custom_job = custom_job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_custom_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_custom_job(
        self,
        request: job_service.GetCustomJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> custom_job.CustomJob:
        r"""Gets a CustomJob.

        Args:
            request (:class:`~.job_service.GetCustomJobRequest`):
                The request object. Request message for
                [JobService.GetCustomJob][google.cloud.aiplatform.v1beta1.JobService.GetCustomJob].
            name (:class:`str`):
                Required. The name of the CustomJob resource. Format:
                ``projects/{project}/locations/{location}/customJobs/{custom_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.custom_job.CustomJob:
                Represents a job that runs custom
                workloads such as a Docker container or
                a Python package. A CustomJob can have
                multiple worker pools and each worker
                pool can have its own machine and input
                spec. A CustomJob will be cleaned up
                once the job enters terminal state
                (failed or succeeded).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.GetCustomJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.GetCustomJobRequest):
            request = job_service.GetCustomJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_custom_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_custom_jobs(
        self,
        request: job_service.ListCustomJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomJobsPager:
        r"""Lists CustomJobs in a Location.

        Args:
            request (:class:`~.job_service.ListCustomJobsRequest`):
                The request object. Request message for
                [JobService.ListCustomJobs][google.cloud.aiplatform.v1beta1.JobService.ListCustomJobs].
            parent (:class:`str`):
                Required. The resource name of the Location to list the
                CustomJobs from. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListCustomJobsPager:
                Response message for
                [JobService.ListCustomJobs][google.cloud.aiplatform.v1beta1.JobService.ListCustomJobs]

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.ListCustomJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.ListCustomJobsRequest):
            request = job_service.ListCustomJobsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_custom_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCustomJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_custom_job(
        self,
        request: job_service.DeleteCustomJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Deletes a CustomJob.

        Args:
            request (:class:`~.job_service.DeleteCustomJobRequest`):
                The request object. Request message for
                [JobService.DeleteCustomJob][google.cloud.aiplatform.v1beta1.JobService.DeleteCustomJob].
            name (:class:`str`):
                Required. The name of the CustomJob resource to be
                deleted. Format:
                ``projects/{project}/locations/{location}/customJobs/{custom_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.DeleteCustomJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.DeleteCustomJobRequest):
            request = job_service.DeleteCustomJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_custom_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def cancel_custom_job(
        self,
        request: job_service.CancelCustomJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Cancels a CustomJob. Starts asynchronous cancellation on the
        CustomJob. The server makes a best effort to cancel the job, but
        success is not guaranteed. Clients can use
        [JobService.GetCustomJob][google.cloud.aiplatform.v1beta1.JobService.GetCustomJob]
        or other methods to check whether the cancellation succeeded or
        whether the job completed despite cancellation. On successful
        cancellation, the CustomJob is not deleted; instead it becomes a
        job with a
        [CustomJob.error][google.cloud.aiplatform.v1beta1.CustomJob.error]
        value with a [google.rpc.Status.code][google.rpc.Status.code] of
        1, corresponding to ``Code.CANCELLED``, and
        [CustomJob.state][google.cloud.aiplatform.v1beta1.CustomJob.state]
        is set to ``CANCELLED``.

        Args:
            request (:class:`~.job_service.CancelCustomJobRequest`):
                The request object. Request message for
                [JobService.CancelCustomJob][google.cloud.aiplatform.v1beta1.JobService.CancelCustomJob].
            name (:class:`str`):
                Required. The name of the CustomJob to cancel. Format:
                ``projects/{project}/locations/{location}/customJobs/{custom_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CancelCustomJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CancelCustomJobRequest):
            request = job_service.CancelCustomJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_custom_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_data_labeling_job(
        self,
        request: job_service.CreateDataLabelingJobRequest = None,
        *,
        parent: str = None,
        data_labeling_job: gca_data_labeling_job.DataLabelingJob = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_data_labeling_job.DataLabelingJob:
        r"""Creates a DataLabelingJob.

        Args:
            request (:class:`~.job_service.CreateDataLabelingJobRequest`):
                The request object. Request message for
                [DataLabelingJobService.CreateDataLabelingJob][].
            parent (:class:`str`):
                Required. The parent of the DataLabelingJob. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            data_labeling_job (:class:`~.gca_data_labeling_job.DataLabelingJob`):
                Required. The DataLabelingJob to
                create.
                This corresponds to the ``data_labeling_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gca_data_labeling_job.DataLabelingJob:
                DataLabelingJob is used to trigger a
                human labeling job on unlabeled data
                from the following Dataset:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, data_labeling_job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CreateDataLabelingJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CreateDataLabelingJobRequest):
            request = job_service.CreateDataLabelingJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if data_labeling_job is not None:
                request.data_labeling_job = data_labeling_job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_data_labeling_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_data_labeling_job(
        self,
        request: job_service.GetDataLabelingJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> data_labeling_job.DataLabelingJob:
        r"""Gets a DataLabelingJob.

        Args:
            request (:class:`~.job_service.GetDataLabelingJobRequest`):
                The request object. Request message for
                [DataLabelingJobService.GetDataLabelingJob][].
            name (:class:`str`):
                Required. The name of the DataLabelingJob. Format:

                ``projects/{project}/locations/{location}/dataLabelingJobs/{data_labeling_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.data_labeling_job.DataLabelingJob:
                DataLabelingJob is used to trigger a
                human labeling job on unlabeled data
                from the following Dataset:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.GetDataLabelingJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.GetDataLabelingJobRequest):
            request = job_service.GetDataLabelingJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_data_labeling_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_data_labeling_jobs(
        self,
        request: job_service.ListDataLabelingJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataLabelingJobsPager:
        r"""Lists DataLabelingJobs in a Location.

        Args:
            request (:class:`~.job_service.ListDataLabelingJobsRequest`):
                The request object. Request message for
                [DataLabelingJobService.ListDataLabelingJobs][].
            parent (:class:`str`):
                Required. The parent of the DataLabelingJob. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListDataLabelingJobsPager:
                Response message for
                [JobService.ListDataLabelingJobs][google.cloud.aiplatform.v1beta1.JobService.ListDataLabelingJobs].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.ListDataLabelingJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.ListDataLabelingJobsRequest):
            request = job_service.ListDataLabelingJobsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_data_labeling_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDataLabelingJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_data_labeling_job(
        self,
        request: job_service.DeleteDataLabelingJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Deletes a DataLabelingJob.

        Args:
            request (:class:`~.job_service.DeleteDataLabelingJobRequest`):
                The request object. Request message for
                [JobService.DeleteDataLabelingJob][google.cloud.aiplatform.v1beta1.JobService.DeleteDataLabelingJob].
            name (:class:`str`):
                Required. The name of the DataLabelingJob to be deleted.
                Format:

                ``projects/{project}/locations/{location}/dataLabelingJobs/{data_labeling_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.DeleteDataLabelingJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.DeleteDataLabelingJobRequest):
            request = job_service.DeleteDataLabelingJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_data_labeling_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def cancel_data_labeling_job(
        self,
        request: job_service.CancelDataLabelingJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Cancels a DataLabelingJob. Success of cancellation is
        not guaranteed.

        Args:
            request (:class:`~.job_service.CancelDataLabelingJobRequest`):
                The request object. Request message for
                [DataLabelingJobService.CancelDataLabelingJob][].
            name (:class:`str`):
                Required. The name of the DataLabelingJob. Format:

                ``projects/{project}/locations/{location}/dataLabelingJobs/{data_labeling_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CancelDataLabelingJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CancelDataLabelingJobRequest):
            request = job_service.CancelDataLabelingJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_data_labeling_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_hyperparameter_tuning_job(
        self,
        request: job_service.CreateHyperparameterTuningJobRequest = None,
        *,
        parent: str = None,
        hyperparameter_tuning_job: gca_hyperparameter_tuning_job.HyperparameterTuningJob = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_hyperparameter_tuning_job.HyperparameterTuningJob:
        r"""Creates a HyperparameterTuningJob

        Args:
            request (:class:`~.job_service.CreateHyperparameterTuningJobRequest`):
                The request object. Request message for
                [JobService.CreateHyperparameterTuningJob][google.cloud.aiplatform.v1beta1.JobService.CreateHyperparameterTuningJob].
            parent (:class:`str`):
                Required. The resource name of the Location to create
                the HyperparameterTuningJob in. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            hyperparameter_tuning_job (:class:`~.gca_hyperparameter_tuning_job.HyperparameterTuningJob`):
                Required. The HyperparameterTuningJob
                to create.
                This corresponds to the ``hyperparameter_tuning_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gca_hyperparameter_tuning_job.HyperparameterTuningJob:
                Represents a HyperparameterTuningJob.
                A HyperparameterTuningJob has a Study
                specification and multiple CustomJobs
                with identical CustomJob specification.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, hyperparameter_tuning_job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CreateHyperparameterTuningJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CreateHyperparameterTuningJobRequest):
            request = job_service.CreateHyperparameterTuningJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if hyperparameter_tuning_job is not None:
                request.hyperparameter_tuning_job = hyperparameter_tuning_job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_hyperparameter_tuning_job
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_hyperparameter_tuning_job(
        self,
        request: job_service.GetHyperparameterTuningJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> hyperparameter_tuning_job.HyperparameterTuningJob:
        r"""Gets a HyperparameterTuningJob

        Args:
            request (:class:`~.job_service.GetHyperparameterTuningJobRequest`):
                The request object. Request message for
                [JobService.GetHyperparameterTuningJob][google.cloud.aiplatform.v1beta1.JobService.GetHyperparameterTuningJob].
            name (:class:`str`):
                Required. The name of the HyperparameterTuningJob
                resource. Format:

                ``projects/{project}/locations/{location}/hyperparameterTuningJobs/{hyperparameter_tuning_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.hyperparameter_tuning_job.HyperparameterTuningJob:
                Represents a HyperparameterTuningJob.
                A HyperparameterTuningJob has a Study
                specification and multiple CustomJobs
                with identical CustomJob specification.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.GetHyperparameterTuningJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.GetHyperparameterTuningJobRequest):
            request = job_service.GetHyperparameterTuningJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_hyperparameter_tuning_job
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_hyperparameter_tuning_jobs(
        self,
        request: job_service.ListHyperparameterTuningJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListHyperparameterTuningJobsPager:
        r"""Lists HyperparameterTuningJobs in a Location.

        Args:
            request (:class:`~.job_service.ListHyperparameterTuningJobsRequest`):
                The request object. Request message for
                [JobService.ListHyperparameterTuningJobs][google.cloud.aiplatform.v1beta1.JobService.ListHyperparameterTuningJobs].
            parent (:class:`str`):
                Required. The resource name of the Location to list the
                HyperparameterTuningJobs from. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListHyperparameterTuningJobsPager:
                Response message for
                [JobService.ListHyperparameterTuningJobs][google.cloud.aiplatform.v1beta1.JobService.ListHyperparameterTuningJobs]

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.ListHyperparameterTuningJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.ListHyperparameterTuningJobsRequest):
            request = job_service.ListHyperparameterTuningJobsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_hyperparameter_tuning_jobs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListHyperparameterTuningJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_hyperparameter_tuning_job(
        self,
        request: job_service.DeleteHyperparameterTuningJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Deletes a HyperparameterTuningJob.

        Args:
            request (:class:`~.job_service.DeleteHyperparameterTuningJobRequest`):
                The request object. Request message for
                [JobService.DeleteHyperparameterTuningJob][google.cloud.aiplatform.v1beta1.JobService.DeleteHyperparameterTuningJob].
            name (:class:`str`):
                Required. The name of the HyperparameterTuningJob
                resource to be deleted. Format:

                ``projects/{project}/locations/{location}/hyperparameterTuningJobs/{hyperparameter_tuning_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.DeleteHyperparameterTuningJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.DeleteHyperparameterTuningJobRequest):
            request = job_service.DeleteHyperparameterTuningJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_hyperparameter_tuning_job
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def cancel_hyperparameter_tuning_job(
        self,
        request: job_service.CancelHyperparameterTuningJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Cancels a HyperparameterTuningJob. Starts asynchronous
        cancellation on the HyperparameterTuningJob. The server makes a
        best effort to cancel the job, but success is not guaranteed.
        Clients can use
        [JobService.GetHyperparameterTuningJob][google.cloud.aiplatform.v1beta1.JobService.GetHyperparameterTuningJob]
        or other methods to check whether the cancellation succeeded or
        whether the job completed despite cancellation. On successful
        cancellation, the HyperparameterTuningJob is not deleted;
        instead it becomes a job with a
        [HyperparameterTuningJob.error][google.cloud.aiplatform.v1beta1.HyperparameterTuningJob.error]
        value with a [google.rpc.Status.code][google.rpc.Status.code] of
        1, corresponding to ``Code.CANCELLED``, and
        [HyperparameterTuningJob.state][google.cloud.aiplatform.v1beta1.HyperparameterTuningJob.state]
        is set to ``CANCELLED``.

        Args:
            request (:class:`~.job_service.CancelHyperparameterTuningJobRequest`):
                The request object. Request message for
                [JobService.CancelHyperparameterTuningJob][google.cloud.aiplatform.v1beta1.JobService.CancelHyperparameterTuningJob].
            name (:class:`str`):
                Required. The name of the HyperparameterTuningJob to
                cancel. Format:

                ``projects/{project}/locations/{location}/hyperparameterTuningJobs/{hyperparameter_tuning_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CancelHyperparameterTuningJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CancelHyperparameterTuningJobRequest):
            request = job_service.CancelHyperparameterTuningJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.cancel_hyperparameter_tuning_job
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_batch_prediction_job(
        self,
        request: job_service.CreateBatchPredictionJobRequest = None,
        *,
        parent: str = None,
        batch_prediction_job: gca_batch_prediction_job.BatchPredictionJob = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_batch_prediction_job.BatchPredictionJob:
        r"""Creates a BatchPredictionJob. A BatchPredictionJob
        once created will right away be attempted to start.

        Args:
            request (:class:`~.job_service.CreateBatchPredictionJobRequest`):
                The request object. Request message for
                [JobService.CreateBatchPredictionJob][google.cloud.aiplatform.v1beta1.JobService.CreateBatchPredictionJob].
            parent (:class:`str`):
                Required. The resource name of the Location to create
                the BatchPredictionJob in. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            batch_prediction_job (:class:`~.gca_batch_prediction_job.BatchPredictionJob`):
                Required. The BatchPredictionJob to
                create.
                This corresponds to the ``batch_prediction_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gca_batch_prediction_job.BatchPredictionJob:
                A job that uses a
                [Model][google.cloud.aiplatform.v1beta1.BatchPredictionJob.model]
                to produce predictions on multiple [input
                instances][google.cloud.aiplatform.v1beta1.BatchPredictionJob.input_config].
                If predictions for significant portion of the instances
                fail, the job may finish without attempting predictions
                for all remaining instances.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, batch_prediction_job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CreateBatchPredictionJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CreateBatchPredictionJobRequest):
            request = job_service.CreateBatchPredictionJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if batch_prediction_job is not None:
                request.batch_prediction_job = batch_prediction_job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_batch_prediction_job
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_batch_prediction_job(
        self,
        request: job_service.GetBatchPredictionJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> batch_prediction_job.BatchPredictionJob:
        r"""Gets a BatchPredictionJob

        Args:
            request (:class:`~.job_service.GetBatchPredictionJobRequest`):
                The request object. Request message for
                [JobService.GetBatchPredictionJob][google.cloud.aiplatform.v1beta1.JobService.GetBatchPredictionJob].
            name (:class:`str`):
                Required. The name of the BatchPredictionJob resource.
                Format:

                ``projects/{project}/locations/{location}/batchPredictionJobs/{batch_prediction_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.batch_prediction_job.BatchPredictionJob:
                A job that uses a
                [Model][google.cloud.aiplatform.v1beta1.BatchPredictionJob.model]
                to produce predictions on multiple [input
                instances][google.cloud.aiplatform.v1beta1.BatchPredictionJob.input_config].
                If predictions for significant portion of the instances
                fail, the job may finish without attempting predictions
                for all remaining instances.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.GetBatchPredictionJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.GetBatchPredictionJobRequest):
            request = job_service.GetBatchPredictionJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_batch_prediction_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_batch_prediction_jobs(
        self,
        request: job_service.ListBatchPredictionJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBatchPredictionJobsPager:
        r"""Lists BatchPredictionJobs in a Location.

        Args:
            request (:class:`~.job_service.ListBatchPredictionJobsRequest`):
                The request object. Request message for
                [JobService.ListBatchPredictionJobs][google.cloud.aiplatform.v1beta1.JobService.ListBatchPredictionJobs].
            parent (:class:`str`):
                Required. The resource name of the Location to list the
                BatchPredictionJobs from. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListBatchPredictionJobsPager:
                Response message for
                [JobService.ListBatchPredictionJobs][google.cloud.aiplatform.v1beta1.JobService.ListBatchPredictionJobs]

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.ListBatchPredictionJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.ListBatchPredictionJobsRequest):
            request = job_service.ListBatchPredictionJobsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_batch_prediction_jobs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBatchPredictionJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_batch_prediction_job(
        self,
        request: job_service.DeleteBatchPredictionJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Deletes a BatchPredictionJob. Can only be called on
        jobs that already finished.

        Args:
            request (:class:`~.job_service.DeleteBatchPredictionJobRequest`):
                The request object. Request message for
                [JobService.DeleteBatchPredictionJob][google.cloud.aiplatform.v1beta1.JobService.DeleteBatchPredictionJob].
            name (:class:`str`):
                Required. The name of the BatchPredictionJob resource to
                be deleted. Format:

                ``projects/{project}/locations/{location}/batchPredictionJobs/{batch_prediction_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.DeleteBatchPredictionJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.DeleteBatchPredictionJobRequest):
            request = job_service.DeleteBatchPredictionJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_batch_prediction_job
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def cancel_batch_prediction_job(
        self,
        request: job_service.CancelBatchPredictionJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Cancels a BatchPredictionJob.

        Starts asynchronous cancellation on the BatchPredictionJob. The
        server makes the best effort to cancel the job, but success is
        not guaranteed. Clients can use
        [JobService.GetBatchPredictionJob][google.cloud.aiplatform.v1beta1.JobService.GetBatchPredictionJob]
        or other methods to check whether the cancellation succeeded or
        whether the job completed despite cancellation. On a successful
        cancellation, the BatchPredictionJob is not deleted;instead its
        [BatchPredictionJob.state][google.cloud.aiplatform.v1beta1.BatchPredictionJob.state]
        is set to ``CANCELLED``. Any files already outputted by the job
        are not deleted.

        Args:
            request (:class:`~.job_service.CancelBatchPredictionJobRequest`):
                The request object. Request message for
                [JobService.CancelBatchPredictionJob][google.cloud.aiplatform.v1beta1.JobService.CancelBatchPredictionJob].
            name (:class:`str`):
                Required. The name of the BatchPredictionJob to cancel.
                Format:

                ``projects/{project}/locations/{location}/batchPredictionJobs/{batch_prediction_job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CancelBatchPredictionJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CancelBatchPredictionJobRequest):
            request = job_service.CancelBatchPredictionJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.cancel_batch_prediction_job
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-aiplatform",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("JobServiceClient",)
