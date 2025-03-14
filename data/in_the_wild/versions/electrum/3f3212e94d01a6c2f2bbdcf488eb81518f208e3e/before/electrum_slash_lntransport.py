# Copyright (C) 2018 Adam Gibson (waxwing)
# Copyright (C) 2018 The Electrum developers
# Distributed under the MIT software license, see the accompanying
# file LICENCE or http://www.opensource.org/licenses/mit-license.php

# Derived from https://gist.github.com/AdamISZ/046d05c156aaeb56cc897f85eecb3eb8

import hashlib
import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Optional

from .crypto import sha256, hmac_oneshot, chacha20_poly1305_encrypt, chacha20_poly1305_decrypt
from .lnutil import (get_ecdh, privkey_to_pubkey, LightningPeerConnectionClosed,
                     HandshakeFailed, LNPeerAddr)
from . import ecc
from .util import bh2u, MySocksProxy


class HandshakeState(object):
    prologue = b"lightning"
    protocol_name = b"Noise_XK_secp256k1_ChaChaPoly_SHA256"
    handshake_version = b"\x00"

    def __init__(self, responder_pub):
        self.responder_pub = responder_pub
        self.h = sha256(self.protocol_name)
        self.ck = self.h
        self.update(self.prologue)
        self.update(self.responder_pub)

    def update(self, data):
        self.h = sha256(self.h + data)
        return self.h

def get_nonce_bytes(n):
    """BOLT 8 requires the nonce to be 12 bytes, 4 bytes leading
    zeroes and 8 bytes little endian encoded 64 bit integer.
    """
    return b"\x00"*4 + n.to_bytes(8, 'little')

def aead_encrypt(key: bytes, nonce: int, associated_data: bytes, data: bytes) -> bytes:
    nonce_bytes = get_nonce_bytes(nonce)
    return chacha20_poly1305_encrypt(key=key,
                                     nonce=nonce_bytes,
                                     associated_data=associated_data,
                                     data=data)

def aead_decrypt(key: bytes, nonce: int, associated_data: bytes, data: bytes) -> bytes:
    nonce_bytes = get_nonce_bytes(nonce)
    return chacha20_poly1305_decrypt(key=key,
                                     nonce=nonce_bytes,
                                     associated_data=associated_data,
                                     data=data)

def get_bolt8_hkdf(salt, ikm):
    """RFC5869 HKDF instantiated in the specific form
    used in Lightning BOLT 8:
    Extract and expand to 64 bytes using HMAC-SHA256,
    with info field set to a zero length string as per BOLT8
    Return as two 32 byte fields.
    """
    #Extract
    prk = hmac_oneshot(salt, msg=ikm, digest=hashlib.sha256)
    assert len(prk) == 32
    #Expand
    info = b""
    T0 = b""
    T1 = hmac_oneshot(prk, T0 + info + b"\x01", digest=hashlib.sha256)
    T2 = hmac_oneshot(prk, T1 + info + b"\x02", digest=hashlib.sha256)
    assert len(T1 + T2) == 64
    return T1, T2

def act1_initiator_message(hs, epriv, epub):
    ss = get_ecdh(epriv, hs.responder_pub)
    ck2, temp_k1 = get_bolt8_hkdf(hs.ck, ss)
    hs.ck = ck2
    c = aead_encrypt(temp_k1, 0, hs.update(epub), b"")
    #for next step if we do it
    hs.update(c)
    msg = hs.handshake_version + epub + c
    assert len(msg) == 50
    return msg, temp_k1


def create_ephemeral_key() -> (bytes, bytes):
    privkey = ecc.ECPrivkey.generate_random_key()
    return privkey.get_secret_bytes(), privkey.get_public_key_bytes()


class LNTransportBase:
    reader: StreamReader
    writer: StreamWriter
    privkey: bytes

    def name(self) -> str:
        raise NotImplementedError()

    def send_bytes(self, msg: bytes) -> None:
        l = len(msg).to_bytes(2, 'big')
        lc = aead_encrypt(self.sk, self.sn(), b'', l)
        c = aead_encrypt(self.sk, self.sn(), b'', msg)
        assert len(lc) == 18
        assert len(c) == len(msg) + 16
        self.writer.write(lc+c)

    async def read_messages(self):
        buffer = bytearray()
        while True:
            rn_l, rk_l = self.rn()
            rn_m, rk_m = self.rn()
            while True:
                if len(buffer) >= 18:
                    lc = bytes(buffer[:18])
                    l = aead_decrypt(rk_l, rn_l, b'', lc)
                    length = int.from_bytes(l, 'big')
                    offset = 18 + length + 16
                    if len(buffer) >= offset:
                        c = bytes(buffer[18:offset])
                        del buffer[:offset]  # much faster than: buffer=buffer[offset:]
                        msg = aead_decrypt(rk_m, rn_m, b'', c)
                        yield msg
                        break
                try:
                    s = await self.reader.read(2**10)
                except asyncio.CancelledError:
                    raise
                except Exception:
                    s = None
                if not s:
                    raise LightningPeerConnectionClosed()
                buffer += s

    def rn(self):
        o = self._rn, self.rk
        self._rn += 1
        if self._rn == 1000:
            self.r_ck, self.rk = get_bolt8_hkdf(self.r_ck, self.rk)
            self._rn = 0
        return o

    def sn(self):
        o = self._sn
        self._sn += 1
        if self._sn == 1000:
            self.s_ck, self.sk = get_bolt8_hkdf(self.s_ck, self.sk)
            self._sn = 0
        return o

    def init_counters(self, ck):
        # init counters
        self._sn = 0
        self._rn = 0
        self.r_ck = ck
        self.s_ck = ck

    def close(self):
        self.writer.close()

    def remote_pubkey(self) -> Optional[bytes]:
        raise NotImplementedError()


class LNResponderTransport(LNTransportBase):
    """Transport initiated by remote party."""

    def __init__(self, privkey: bytes, reader: StreamReader, writer: StreamWriter):
        LNTransportBase.__init__(self)
        self.reader = reader
        self.writer = writer
        self.privkey = privkey
        self._pubkey = None  # remote pubkey

    def name(self):
        pubkey = self.remote_pubkey()
        pubkey_hex = pubkey.hex() if pubkey else pubkey
        return f"{pubkey_hex}(in)"

    async def handshake(self, **kwargs):
        hs = HandshakeState(privkey_to_pubkey(self.privkey))
        act1 = b''
        while len(act1) < 50:
            buf = await self.reader.read(50 - len(act1))
            if not buf:
                raise HandshakeFailed('responder disconnected')
            act1 += buf
        if len(act1) != 50:
            raise HandshakeFailed('responder: short act 1 read, length is ' + str(len(act1)))
        if bytes([act1[0]]) != HandshakeState.handshake_version:
            raise HandshakeFailed('responder: bad handshake version in act 1')
        c = act1[-16:]
        re = act1[1:34]
        h = hs.update(re)
        ss = get_ecdh(self.privkey, re)
        ck, temp_k1 = get_bolt8_hkdf(sha256(HandshakeState.protocol_name), ss)
        _p = aead_decrypt(temp_k1, 0, h, c)
        hs.update(c)

        # act 2
        if 'epriv' not in kwargs:
            epriv, epub = create_ephemeral_key()
        else:
            epriv = kwargs['epriv']
            epub = ecc.ECPrivkey(epriv).get_public_key_bytes()
        hs.ck = ck
        hs.responder_pub = re

        msg, temp_k2 = act1_initiator_message(hs, epriv, epub)
        self.writer.write(msg)

        # act 3
        act3 = b''
        while len(act3) < 66:
            buf = await self.reader.read(66 - len(act3))
            if not buf:
                raise HandshakeFailed('responder disconnected')
            act3 += buf
        if len(act3) != 66:
            raise HandshakeFailed('responder: short act 3 read, length is ' + str(len(act3)))
        if bytes([act3[0]]) != HandshakeState.handshake_version:
            raise HandshakeFailed('responder: bad handshake version in act 3')
        c = act3[1:50]
        t = act3[-16:]
        rs = aead_decrypt(temp_k2, 1, hs.h, c)
        ss = get_ecdh(epriv, rs)
        ck, temp_k3 = get_bolt8_hkdf(hs.ck, ss)
        _p = aead_decrypt(temp_k3, 0, hs.update(c), t)
        self.rk, self.sk = get_bolt8_hkdf(ck, b'')
        self.init_counters(ck)
        self._pubkey = rs
        return rs

    def remote_pubkey(self) -> Optional[bytes]:
        return self._pubkey


class LNTransport(LNTransportBase):
    """Transport initiated by local party."""

    def __init__(self, privkey: bytes, peer_addr: LNPeerAddr, *,
                 proxy: Optional[dict]):
        LNTransportBase.__init__(self)
        assert type(privkey) is bytes and len(privkey) == 32
        self.privkey = privkey
        self.peer_addr = peer_addr
        self.proxy = MySocksProxy.from_proxy_dict(proxy)

    def name(self):
        return self.peer_addr.net_addr_str()

    async def handshake(self):
        if not self.proxy:
            self.reader, self.writer = await asyncio.open_connection(self.peer_addr.host, self.peer_addr.port)
        else:
            self.reader, self.writer = await self.proxy.open_connection(self.peer_addr.host, self.peer_addr.port)
        hs = HandshakeState(self.peer_addr.pubkey)
        # Get a new ephemeral key
        epriv, epub = create_ephemeral_key()

        msg, _temp_k1 = act1_initiator_message(hs, epriv, epub)
        # act 1
        self.writer.write(msg)
        rspns = await self.reader.read(2**10)
        if len(rspns) != 50:
            raise HandshakeFailed(f"Lightning handshake act 1 response has bad length, "
                                  f"are you sure this is the right pubkey? {self.peer_addr}")
        hver, alice_epub, tag = rspns[0], rspns[1:34], rspns[34:]
        if bytes([hver]) != hs.handshake_version:
            raise HandshakeFailed("unexpected handshake version: {}".format(hver))
        # act 2
        hs.update(alice_epub)
        ss = get_ecdh(epriv, alice_epub)
        ck, temp_k2 = get_bolt8_hkdf(hs.ck, ss)
        hs.ck = ck
        p = aead_decrypt(temp_k2, 0, hs.h, tag)
        hs.update(tag)
        # act 3
        my_pubkey = privkey_to_pubkey(self.privkey)
        c = aead_encrypt(temp_k2, 1, hs.h, my_pubkey)
        hs.update(c)
        ss = get_ecdh(self.privkey[:32], alice_epub)
        ck, temp_k3 = get_bolt8_hkdf(hs.ck, ss)
        hs.ck = ck
        t = aead_encrypt(temp_k3, 0, hs.h, b'')
        msg = hs.handshake_version + c + t
        self.writer.write(msg)
        self.sk, self.rk = get_bolt8_hkdf(hs.ck, b'')
        self.init_counters(ck)

    def remote_pubkey(self) -> Optional[bytes]:
        return self.peer_addr.pubkey
