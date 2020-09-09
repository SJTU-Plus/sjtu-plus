from abc import ABCMeta, abstractmethod
from binascii import unhexlify
from datetime import datetime

from Crypto.Hash import BLAKE2b
from base58 import b58decode, b58encode

from SJTUPlus.settings import ATTESTATION_SECRET

__all__ = ['attestation']


class AttestationBase(metaclass=ABCMeta):

    @abstractmethod
    def _generate(self, raw: bytes) -> bytes:
        raise Exception("AttestationBase abstract method called")

    @abstractmethod
    def _verify(self, raw: bytes, quote: bytes):
        raise Exception("AttestationBase abstract method called")

    @staticmethod
    def _normalize(qq_number) -> bytes:
        no = int(qq_number)
        return int.to_bytes(no, 8, 'little')

    def generate(self, qq_number):
        qq_number = self._normalize(qq_number)

        ts = int(datetime.now().timestamp())
        timestamp = int.to_bytes(ts, 4, 'little')

        quote = self._generate(timestamp + qq_number)
        return b58encode(timestamp + quote).decode()

    def verify(self, qq_number, quote) -> datetime or None:
        qq_number = self._normalize(qq_number)

        if not isinstance(quote, bytes):
            quote = b58decode(quote)

        try:
            self._verify(quote[:4] + qq_number, quote[4:])
        except ValueError:
            return None

        ts = int.from_bytes(quote[:4], 'little')
        return datetime.fromtimestamp(ts)


class Blake2Attestation(AttestationBase):
    def __init__(self, secret: bytes, digest_bits=192):
        self._secret = secret
        self._digest_bits = digest_bits

    @staticmethod
    def load(path, *args, **kwargs):
        from pathlib import Path
        key = Path(path).read_bytes()
        return Blake2Attestation(key, *args, **kwargs)

    def _common(self, raw: bytes):
        return BLAKE2b.new(data=raw, digest_bits=self._digest_bits, key=self._secret)

    def _generate(self, raw: bytes) -> bytes:
        h = self._common(raw)
        return h.digest()

    def _verify(self, raw: bytes, quote: bytes):
        h = self._common(raw)
        h.verify(quote)


attestation = Blake2Attestation(unhexlify(ATTESTATION_SECRET))
