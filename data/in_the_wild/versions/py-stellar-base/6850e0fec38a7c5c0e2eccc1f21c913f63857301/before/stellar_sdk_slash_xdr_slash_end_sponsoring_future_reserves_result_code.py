# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__

__all__ = ["EndSponsoringFutureReservesResultCode"]


class EndSponsoringFutureReservesResultCode(IntEnum):
    """
    XDR Source Code::

        enum EndSponsoringFutureReservesResultCode
        {
            // codes considered as "success" for the operation
            END_SPONSORING_FUTURE_RESERVES_SUCCESS = 0,

            // codes considered as "failure" for the operation
            END_SPONSORING_FUTURE_RESERVES_NOT_SPONSORED = -1
        };
    """

    END_SPONSORING_FUTURE_RESERVES_SUCCESS = 0
    END_SPONSORING_FUTURE_RESERVES_NOT_SPONSORED = -1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "EndSponsoringFutureReservesResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "EndSponsoringFutureReservesResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "EndSponsoringFutureReservesResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
