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

"""Implement a class to simulate GCS object."""

import base64
import datetime
import hashlib
import json
import re
import socket
import struct
import time

import crc32c
import flask
from google.protobuf import field_mask_pb2, json_format

from google.storage.v2 import storage_pb2
import testbench


class Object:
    modifiable_fields = [
        "content_encoding",
        "content_disposition",
        "cache_control",
        "acl",
        "content_language",
        "content_type",
        "storage_class",
        "kms_key",
        "temporary_hold",
        "retention_expire_time",
        "metadata",
        "event_based_hold",
        "customer_encryption",
        "custom_time",
    ]

    def __init__(self, metadata, media, bucket):
        self.metadata = metadata
        self.media = media
        self.bucket = bucket

    @classmethod
    def __insert_predefined_acl(cls, metadata, bucket, predefined_acl, context):
        if predefined_acl == "" or predefined_acl is None:
            return
        if bucket.iam_config.uniform_bucket_level_access.enabled:
            testbench.error.invalid(
                "Predefined ACL with uniform bucket level access enabled", context
            )
        acls = testbench.acl.compute_predefined_object_acl(
            metadata.bucket, metadata.name, metadata.generation, predefined_acl, context
        )
        del metadata.acl[:]
        metadata.acl.extend(acls)

    @classmethod
    def __postprocess_customer_encryption(cls, metadata):
        # There is no need to base64 encode the data, because json_format.MessageToDict() already does.
        return testbench.common.rest_adjust(
            metadata,
            {"keySha256Bytes": lambda x: ("keySha256", x)},
        )

    @classmethod
    def __postprocess_object_metadata(cls, metadata):
        """The protos for storage/v2 renamed some fields in ways that require some custom coding."""
        # For some fields the storage/v2 name just needs to change slightly.
        bucket_id = testbench.common.bucket_name_from_proto(
            metadata.get("bucket", None)
        )
        metadata = testbench.common.rest_adjust(
            metadata,
            {
                "bucket": lambda x: ("bucket", bucket_id),
                "createTime": lambda x: ("timeCreated", x),
                "updateTime": lambda x: ("updated", x),
                "kmsKey": lambda x: ("kmsKeyName", x),
                "retentionExpireTime": lambda x: ("retentionExpirationTime", x),
                "deleteTime": lambda x: ("timeDeleted", x),
                "updateStorageClassTime": lambda x: ("timeStorageClassUpdated", x),
                "customerEncryption": lambda x: (
                    "customerEncryption",
                    cls.__postprocess_customer_encryption(x),
                ),
            },
        )
        metadata["kind"] = "storage#object"
        metadata["id"] = "%s/o/%s/%s" % (
            metadata["bucket"],
            metadata["name"],
            metadata["generation"],
        )
        # Checksums need special treatment
        cs = metadata.pop("checksums", None)
        if cs is not None:
            if "crc32c" in cs:
                metadata["crc32c"] = base64.b64encode(
                    struct.pack(">I", cs["crc32c"])
                ).decode("utf-8")
            if "md5Hash" in cs:
                metadata["md5Hash"] = cs["md5Hash"]
        # Finally the ACLs, if present, require additional fields
        if "acl" in metadata:
            for a in metadata["acl"]:
                a["kind"] = "storage#objectAccessControl"
                if bucket_id is not None:
                    a["bucket"] = bucket_id
                a["object"] = metadata.get("name", None)
                a["generation"] = metadata.get("generation", None)
        return metadata

    @classmethod
    def init(cls, request, metadata, media, bucket, is_destination, context):
        instruction = testbench.common.extract_instruction(request, context)
        if instruction == "inject-upload-data-error":
            media = testbench.common.corrupt_media(media)
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        metadata.bucket = bucket.name
        metadata.generation = int(timestamp.timestamp() * 1000)
        metadata.metageneration = 1
        metadata.size = len(media)
        actual_md5Hash = hashlib.md5(media).digest()
        actual_crc32c = crc32c.crc32c(media)
        if metadata.HasField("checksums"):
            cs = metadata.checksums
            if len(cs.md5_hash) != 0 and actual_md5Hash != cs.md5_hash:
                testbench.error.mismatch(
                    "md5Hash", cs.md5_hash, actual_md5Hash, context
                )
            if cs.HasField("crc32c") and actual_crc32c != cs.crc32c:
                testbench.error.mismatch("crc32c", cs.crc32c, actual_crc32c, context)
        metadata.checksums.md5_hash = actual_md5Hash
        metadata.checksums.crc32c = actual_crc32c
        metadata.create_time.FromDatetime(timestamp)
        metadata.update_time.FromDatetime(timestamp)
        if bucket.HasField("retention_policy"):
            retention_expiration_time = timestamp + datetime.timedelta(
                0, bucket.retention_policy.retention_period
            )
            metadata.retention_expire_time.FromDatetime(retention_expiration_time)
        metadata.owner.entity = testbench.acl.get_object_entity("OWNER", context)
        algorithm, key_b64, key_sha256_b64 = testbench.csek.extract(
            request, False, context
        )
        if algorithm != "":
            key_sha256 = base64.b64decode(key_sha256_b64)
            testbench.csek.check(algorithm, key_b64, key_sha256, context)
            metadata.customer_encryption.encryption_algorithm = algorithm
            metadata.customer_encryption.key_sha256_bytes = key_sha256
        default_projection = "noAcl"
        is_uniform = bucket.iam_config.uniform_bucket_level_access.enabled
        # TODO(#27) - this is probably a bug, cleanup once we move all the code
        bucket.iam_config.uniform_bucket_level_access.enabled = False
        if len(metadata.acl) != 0:
            default_projection = "full"
        else:
            predefined_acl = testbench.acl.extract_predefined_acl(
                request, is_destination, context
            )
            if predefined_acl is None or predefined_acl == "":
                predefined_acl = "projectPrivate"
            elif is_uniform:
                testbench.error.invalid(
                    "Predefined ACL with uniform bucket level access enabled", context
                )
            cls.__insert_predefined_acl(metadata, bucket, predefined_acl, context)
        # TODO(#27) - this is probably a bug, cleanup once we move all the code
        bucket.iam_config.uniform_bucket_level_access.enabled = is_uniform
        return (
            cls(metadata, media, bucket),
            testbench.common.extract_projection(request, default_projection, context),
        )

    @classmethod
    def init_dict(cls, request, metadata, media, bucket, is_destination):
        metadata = json_format.ParseDict(
            testbench.common.preprocess_object_metadata(metadata), storage_pb2.Object()
        )
        return cls.init(request, metadata, media, bucket, is_destination, None)

    @classmethod
    def init_media(cls, request, bucket):
        object_name = request.args.get("name", None)
        media = testbench.common.extract_media(request)
        if object_name is None:
            testbench.error.missing("name", None)
        metadata = {
            "bucket": testbench.common.bucket_name_from_proto(bucket.name),
            "name": object_name,
            "metadata": {"x_emulator_upload": "simple"},
        }
        return cls.init_dict(request, metadata, media, bucket, False)

    @classmethod
    def init_multipart(cls, request, bucket):
        metadata, media_headers, media = testbench.common.parse_multipart(request)
        metadata["name"] = request.args.get("name", metadata.get("name", None))
        if metadata["name"] is None:
            testbench.error.missing("name", None)
        if (
            metadata.get("contentType") is not None
            and media_headers.get("content-type") is not None
            and metadata.get("contentType") != media_headers.get("content-type")
        ):
            testbench.error.mismatch(
                "Content-Type",
                media_headers.get("content-type"),
                metadata.get("contentType"),
                None,
            )
        metadata["bucket"] = testbench.common.bucket_name_from_proto(bucket.name)
        if "contentType" not in metadata:
            metadata["contentType"] = media_headers.get("content-type")
        metadata["metadata"] = (
            {} if "metadata" not in metadata else metadata["metadata"]
        )
        metadata["metadata"]["x_emulator_upload"] = "multipart"
        if "md5Hash" in metadata:
            metadata["metadata"]["x_emulator_md5"] = metadata["md5Hash"]
        if "crc32c" in metadata:
            metadata["metadata"]["x_emulator_crc32c"] = metadata["crc32c"]
        return cls.init_dict(request, metadata, media, bucket, False)

    @classmethod
    def init_xml(cls, request, bucket, name):
        media = testbench.common.extract_media(request)
        metadata = {
            "bucket": bucket.name,
            "name": name,
            "metadata": {"x_emulator_upload": "xml"},
        }
        if "content-type" in request.headers:
            metadata["contentType"] = request.headers["content-type"]
        fake_request = testbench.common.FakeRequest.init_xml(request)
        x_goog_hash = fake_request.headers.get("x-goog-hash")
        if x_goog_hash is not None:
            for checksum in x_goog_hash.split(","):
                if checksum.startswith("md5="):
                    md5Hash = checksum[4:]
                    metadata["md5Hash"] = md5Hash
                if checksum.startswith("crc32c="):
                    crc32c_value = checksum[7:]
                    metadata["crc32c"] = crc32c_value
        blob, _ = cls.init_dict(fake_request, metadata, media, bucket, False)
        return blob, fake_request

    # === METADATA === #

    def __update_metadata(self, source, update_mask):
        if update_mask is None:
            update_mask = field_mask_pb2.FieldMask(paths=Object.modifiable_fields)
        update_mask.MergeMessage(source, self.metadata, True, True)
        self.metadata.metageneration += 1
        self.metadata.update_time.FromDatetime(datetime.datetime.now())

    def update(self, request, context):
        # Support for `Object: update` over gRPC is not needed (and not implemented).
        assert context is None
        data = json.loads(request.data)
        metadata = json_format.ParseDict(
            testbench.common.preprocess_object_metadata(data), storage_pb2.Object()
        )
        self.__update_metadata(metadata, None)
        self.__insert_predefined_acl(
            metadata,
            self.bucket,
            testbench.acl.extract_predefined_acl(request, False, context),
            context,
        )

    def patch(self, request, context):
        # Support for `Object: patch` over gRPC is not needed (and not implemented).
        assert context is None
        # The idea here is to convert the storage_pb2.Object proto to its REST
        # representation, apply the patch, and then convert it back to its
        # proto representation.
        rest = testbench.common.preprocess_object_metadata(
            testbench.common.rest_patch(
                Object.rest(self.metadata), json.loads(request.data)
            )
        )
        metadata = json_format.ParseDict(rest, storage_pb2.Object())
        self.__update_metadata(metadata, None)
        self.__insert_predefined_acl(
            metadata,
            self.bucket,
            testbench.acl.extract_predefined_acl(request, False, context),
            context,
        )

    # === ACL === #

    def __search_acl(self, entity, must_exist, context):
        entity = testbench.acl.get_canonical_entity(entity)
        for i in range(len(self.metadata.acl)):
            if self.metadata.acl[i].entity == entity:
                return i
        if must_exist:
            testbench.error.notfound("ACL %s" % entity, context)

    def __upsert_acl(self, entity, role, context):
        # For simplicity, we treat `insert`, `update` and `patch` ACL the same way.
        index = self.__search_acl(entity, False, context)
        acl = testbench.acl.create_object_acl(
            self.metadata.bucket,
            self.metadata.name,
            self.metadata.generation,
            entity,
            role,
            context,
        )
        if index is not None:
            self.metadata.acl[index].CopyFrom(acl)
            return self.metadata.acl[index]
        else:
            self.metadata.acl.append(acl)
            return acl

    def get_acl(self, entity, context):
        index = self.__search_acl(entity, True, context)
        return self.metadata.acl[index]

    def insert_acl(self, request, context):
        payload = json.loads(request.data)
        entity, role = payload["entity"], payload["role"]
        return self.__upsert_acl(entity, role, context)

    def update_acl(self, request, entity, context):
        payload = json.loads(request.data)
        role = payload["role"]
        return self.__upsert_acl(entity, role, context)

    def patch_acl(self, request, entity, context):
        payload = json.loads(request.data)
        role = payload["role"]
        return self.__upsert_acl(entity, role, context)

    def delete_acl(self, entity, context):
        del self.metadata.acl[self.__search_acl(entity, True, context)]

    # === RESPONSE === #

    @classmethod
    def rest(cls, metadata):
        response = cls.__postprocess_object_metadata(
            json_format.MessageToDict(metadata)
        )
        old_metadata = {}
        if "metadata" in response:
            for key, value in response["metadata"].items():
                if "emulator" in key:
                    old_key = key.replace("emulator", "testbench")
                    old_metadata[old_key] = value
            response["metadata"].update(old_metadata)
        return response

    def rest_metadata(self):
        return self.rest(self.metadata)

    def x_goog_hash_header(self):
        if not self.metadata.HasField("checksums"):
            return None
        hashes = []
        cs = self.metadata.checksums
        if cs.HasField("crc32c"):
            hashes.append(
                "crc32c=%s" % testbench.common.rest_crc32c_from_proto(cs.crc32c)
            )
        if len(cs.md5_hash) != 0:
            hashes.append("md5=%s" % testbench.common.rest_md5_from_proto(cs.md5_hash))
        return ",".join(hashes) if len(hashes) != 0 else None

    def rest_media(self, request, delay=time.sleep):
        range_header = request.headers.get("range")
        response_payload = self.media
        begin = 0
        end = len(response_payload)
        if range_header is not None:
            m = re.match("bytes=([0-9]+)-([0-9]+)", range_header)
            if m:
                begin = int(m.group(1))
                end = int(m.group(2))
                response_payload = response_payload[begin : end + 1]
            m = re.match("bytes=([0-9]+)-$", range_header)
            if m:
                begin = int(m.group(1))
                response_payload = response_payload[begin:]
            m = re.match("bytes=-([0-9]+)$", range_header)
            if m:
                last = int(m.group(1))
                response_payload = response_payload[-last:]

        streamer, length, headers = None, len(response_payload), {}
        content_range = "bytes %d-%d/%d" % (begin, end - 1, len(self.media))

        instructions = testbench.common.extract_instruction(request, None)
        if instructions == "return-broken-stream":
            request_socket = request.environ.get("gunicorn.socket", None)

            def streamer():
                chunk_size = 64 * 1024
                for r in range(0, len(response_payload), chunk_size):
                    if r >= 1024 * 1024:
                        if request_socket is not None:
                            request_socket.setsockopt(
                                socket.SOL_SOCKET,
                                socket.SO_LINGER,
                                struct.pack("ii", 1, 0),
                            )
                            request_socket.close()
                        # This exception is raised to abort the flow control. The
                        # connection has already been closed, causing the client to
                        # receive a "connection reset by peer" (or a similar error).
                        # The exception is useful in unit tests (where there is no
                        # socket to close), and stops the testbench from trying to
                        # complete a request that we intentionally aborted.
                        raise testbench.error.RestException(
                            "Injected 'connection reset by peer' fault", 500
                        )
                    delay(0.1)
                    chunk_end = min(r + chunk_size, len(response_payload))
                    yield response_payload[r:chunk_end]

        elif instructions == "return-corrupted-data":
            media = testbench.common.corrupt_media(response_payload)

            def streamer():
                yield media

        elif instructions is not None and instructions.startswith("stall-always"):

            def streamer():
                chunk_size = 16 * 1024
                for r in range(begin, end, chunk_size):
                    chunk_end = min(r + chunk_size, end)
                    if r == begin:
                        delay(10)
                    yield response_payload[r:chunk_end]

        elif instructions == "stall-at-256KiB" and begin == 0:

            def streamer():
                chunk_size = 16 * 1024
                for r in range(begin, end, chunk_size):
                    chunk_end = min(r + chunk_size, end)
                    if r == 256 * 1024:
                        time.sleep(10)
                    yield response_payload[r:chunk_end]

        elif instructions is not None and instructions.startswith(
            "return-503-after-256K"
        ):
            if begin == 0:
                request_socket = request.environ.get("gunicorn.socket", None)

                def streamer():
                    chunk_size = 4 * 1024
                    for r in range(0, len(response_payload), chunk_size):
                        if r >= 256 * 1024:
                            if request_socket is not None:
                                request_socket.setsockopt(
                                    socket.SOL_SOCKET,
                                    socket.SO_LINGER,
                                    struct.pack("ii", 1, 0),
                                )
                                request_socket.close()
                            # This exception is raised to abort the flow control. The
                            # connection has already been closed, causing the client to
                            # receive a "connection reset by peer" (or a similar error).
                            # The exception is useful in unit tests (where there is no
                            # socket to close), and stops the testbench from trying to
                            # complete a request that we intentionally aborted.
                            raise testbench.error.RestException(
                                "Injected 'connection reset by peer' fault", 503
                            )
                        time.sleep(0.01)
                        chunk_end = min(r + chunk_size, len(response_payload))
                        yield response_payload[r:chunk_end]

            elif instructions.endswith("/retry-1"):
                print("## Return error for retry 1")
                return flask.Response("Service Unavailable", status=503)
            elif instructions.endswith("/retry-2"):
                print("## Return error for retry 2")
                return flask.Response("Service Unavailable", status=503)
            else:
                print("## Return success for %s" % instructions)
                return flask.Response(response_payload, status=200, headers=headers)
        else:

            def streamer():
                yield response_payload

        headers["Content-Range"] = content_range
        headers["x-goog-hash"] = self.x_goog_hash_header()
        headers["x-goog-generation"] = self.metadata.generation
        headers["x-goog-metageneration"] = self.metadata.metageneration
        headers["x-goog-storage-class"] = self.metadata.storage_class
        return flask.Response(streamer(), status=200, headers=headers)
