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
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation as ga_operation
from google.cloud.aiplatform_v1beta1.services.model_service import pagers
from google.cloud.aiplatform_v1beta1.types import deployed_model_ref
from google.cloud.aiplatform_v1beta1.types import explanation
from google.cloud.aiplatform_v1beta1.types import model
from google.cloud.aiplatform_v1beta1.types import model as gca_model
from google.cloud.aiplatform_v1beta1.types import model_evaluation
from google.cloud.aiplatform_v1beta1.types import model_evaluation_slice
from google.cloud.aiplatform_v1beta1.types import model_service
from google.cloud.aiplatform_v1beta1.types import operation as gca_operation
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import ModelServiceTransport
from .transports.grpc import ModelServiceGrpcTransport


class ModelServiceClientMeta(type):
    """Metaclass for the ModelService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[ModelServiceTransport]]
    _transport_registry["grpc"] = ModelServiceGrpcTransport

    def get_transport_class(cls, label: str = None,) -> Type[ModelServiceTransport]:
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


class ModelServiceClient(metaclass=ModelServiceClientMeta):
    """A service for managing AI Platform's machine learning Models."""

    DEFAULT_OPTIONS = ClientOptions.ClientOptions(
        api_endpoint="aiplatform.googleapis.com"
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
    def model_path(project: str, location: str, model: str,) -> str:
        """Return a fully-qualified model string."""
        return "projects/{project}/locations/{location}/models/{model}".format(
            project=project, location=location, model=model,
        )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, ModelServiceTransport] = None,
        client_options: ClientOptions.ClientOptions = DEFAULT_OPTIONS,
    ) -> None:
        """Instantiate the model service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ModelServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ModelServiceTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                host=client_options.api_endpoint or "aiplatform.googleapis.com",
            )

    def upload_model(
        self,
        request: model_service.UploadModelRequest = None,
        *,
        parent: str = None,
        model: gca_model.Model = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Uploads a Model artifact into AI Platform.

        Args:
            request (:class:`~.model_service.UploadModelRequest`):
                The request object. Request message for
                [ModelService.UploadModel][google.cloud.aiplatform.v1beta1.ModelService.UploadModel].
            parent (:class:`str`):
                Required. The resource name of the Location into which
                to upload the Model. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            model (:class:`~.gca_model.Model`):
                Required. The Model to create.
                This corresponds to the ``model`` field
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
                :class:``~.model_service.UploadModelResponse``: Response
                message of
                [ModelService.UploadModel][google.cloud.aiplatform.v1beta1.ModelService.UploadModel]
                operation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, model]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.UploadModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if model is not None:
            request.model = model

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.upload_model,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            model_service.UploadModelResponse,
            metadata_type=model_service.UploadModelOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_model(
        self,
        request: model_service.GetModelRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> model.Model:
        r"""Gets a Model.

        Args:
            request (:class:`~.model_service.GetModelRequest`):
                The request object. Request message for
                [ModelService.GetModel][google.cloud.aiplatform.v1beta1.ModelService.GetModel].
            name (:class:`str`):
                Required. The name of the Model resource. Format:
                ``projects/{project}/locations/{location}/models/{model}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.model.Model:
                A trained machine learning Model.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.GetModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_model, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_models(
        self,
        request: model_service.ListModelsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListModelsPager:
        r"""Lists Models in a Location.

        Args:
            request (:class:`~.model_service.ListModelsRequest`):
                The request object. Request message for
                [ModelService.ListModels][google.cloud.aiplatform.v1beta1.ModelService.ListModels].
            parent (:class:`str`):
                Required. The resource name of the Location to list the
                Models from. Format:
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
            ~.pagers.ListModelsPager:
                Response message for
                [ModelService.ListModels][google.cloud.aiplatform.v1beta1.ModelService.ListModels]

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.ListModelsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_models, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListModelsPager(
            method=rpc, request=request, response=response,
        )

        # Done; return the response.
        return response

    def update_model(
        self,
        request: model_service.UpdateModelRequest = None,
        *,
        model: gca_model.Model = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_model.Model:
        r"""Updates a Model.

        Args:
            request (:class:`~.model_service.UpdateModelRequest`):
                The request object. Request message for
                [ModelService.UpdateModel][google.cloud.aiplatform.v1beta1.ModelService.UpdateModel].
            model (:class:`~.gca_model.Model`):
                Required. The Model which replaces
                the resource on the server.
                This corresponds to the ``model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see

                [FieldMask](https:
                //developers.google.com/protocol-buffers //
                /docs/reference/google.protobuf#fieldmask).
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gca_model.Model:
                A trained machine learning Model.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([model, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.UpdateModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if model is not None:
            request.model = model
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_model,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_model(
        self,
        request: model_service.DeleteModelRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Deletes a Model.
        Note: Model can only be deleted if there are no
        DeployedModels created from it.

        Args:
            request (:class:`~.model_service.DeleteModelRequest`):
                The request object. Request message for
                [ModelService.DeleteModel][google.cloud.aiplatform.v1beta1.ModelService.DeleteModel].
            name (:class:`str`):
                Required. The name of the Model resource to be deleted.
                Format:
                ``projects/{project}/locations/{location}/models/{model}``
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
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.DeleteModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_model,
            default_timeout=None,
            client_info=_client_info,
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

    def export_model(
        self,
        request: model_service.ExportModelRequest = None,
        *,
        name: str = None,
        output_config: model_service.ExportModelRequest.OutputConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Exports a trained, exportable, Model to a location specified by
        the user. A Model is considered to be exportable if it has at
        least one [supported export
        format][google.cloud.aiplatform.v1beta1.Model.supported_export_formats].

        Args:
            request (:class:`~.model_service.ExportModelRequest`):
                The request object. Request message for
                [ModelService.ExportModel][google.cloud.aiplatform.v1beta1.ModelService.ExportModel].
            name (:class:`str`):
                Required. The resource name of the Model to export.
                Format:
                ``projects/{project}/locations/{location}/models/{model}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (:class:`~.model_service.ExportModelRequest.OutputConfig`):
                Required. The desired output location
                and configuration.
                This corresponds to the ``output_config`` field
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
                :class:``~.model_service.ExportModelResponse``: Response
                message of
                [ModelService.ExportModel][google.cloud.aiplatform.v1beta1.ModelService.ExportModel]
                operation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, output_config]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.ExportModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name
        if output_config is not None:
            request.output_config = output_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.export_model,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            model_service.ExportModelResponse,
            metadata_type=model_service.ExportModelOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_model_evaluation(
        self,
        request: model_service.GetModelEvaluationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> model_evaluation.ModelEvaluation:
        r"""Gets a ModelEvaluation.

        Args:
            request (:class:`~.model_service.GetModelEvaluationRequest`):
                The request object. Request message for
                [ModelService.GetModelEvaluation][google.cloud.aiplatform.v1beta1.ModelService.GetModelEvaluation].
            name (:class:`str`):
                Required. The name of the ModelEvaluation resource.
                Format:

                ``projects/{project}/locations/{location}/models/{model}/evaluations/{evaluation}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.model_evaluation.ModelEvaluation:
                A collection of metrics calculated by
                comparing Model's predictions on all of
                the test data against annotations from
                the test data.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.GetModelEvaluationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_model_evaluation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_model_evaluations(
        self,
        request: model_service.ListModelEvaluationsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListModelEvaluationsPager:
        r"""Lists ModelEvaluations in a Model.

        Args:
            request (:class:`~.model_service.ListModelEvaluationsRequest`):
                The request object. Request message for
                [ModelService.ListModelEvaluations][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluations].
            parent (:class:`str`):
                Required. The resource name of the Model to list the
                ModelEvaluations from. Format:
                ``projects/{project}/locations/{location}/models/{model}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListModelEvaluationsPager:
                Response message for
                [ModelService.ListModelEvaluations][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluations].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.ListModelEvaluationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_model_evaluations,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListModelEvaluationsPager(
            method=rpc, request=request, response=response,
        )

        # Done; return the response.
        return response

    def get_model_evaluation_slice(
        self,
        request: model_service.GetModelEvaluationSliceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> model_evaluation_slice.ModelEvaluationSlice:
        r"""Gets a ModelEvaluationSlice.

        Args:
            request (:class:`~.model_service.GetModelEvaluationSliceRequest`):
                The request object. Request message for
                [ModelService.GetModelEvaluationSlice][google.cloud.aiplatform.v1beta1.ModelService.GetModelEvaluationSlice].
            name (:class:`str`):
                Required. The name of the ModelEvaluationSlice resource.
                Format:

                ``projects/{project}/locations/{location}/models/{model}/evaluations/{evaluation}/slices/{slice}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.model_evaluation_slice.ModelEvaluationSlice:
                A collection of metrics calculated by
                comparing Model's predictions on a slice
                of the test data against ground truth
                annotations.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.GetModelEvaluationSliceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_model_evaluation_slice,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_model_evaluation_slices(
        self,
        request: model_service.ListModelEvaluationSlicesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListModelEvaluationSlicesPager:
        r"""Lists ModelEvaluationSlices in a ModelEvaluation.

        Args:
            request (:class:`~.model_service.ListModelEvaluationSlicesRequest`):
                The request object. Request message for
                [ModelService.ListModelEvaluationSlices][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluationSlices].
            parent (:class:`str`):
                Required. The resource name of the ModelEvaluation to
                list the ModelEvaluationSlices from. Format:

                ``projects/{project}/locations/{location}/models/{model}/evaluations/{evaluation}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListModelEvaluationSlicesPager:
                Response message for
                [ModelService.ListModelEvaluationSlices][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluationSlices].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = model_service.ListModelEvaluationSlicesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_model_evaluation_slices,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListModelEvaluationSlicesPager(
            method=rpc, request=request, response=response,
        )

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-aiplatform",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("ModelServiceClient",)
