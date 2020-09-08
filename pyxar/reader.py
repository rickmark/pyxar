from typing import BinaryIO, List
import zlib
from xml.etree.ElementTree import *
from enum import *


XAR_SIGNATURE = 0x78617221


class XarChecksumAlgorithm(Enum):
    NONE = 0
    SHA1 = 1
    MD5 = 2
    SHA256 = 3
    SHA512 = 4


class XarFileExtendedItem(object):
    _name: str


class XarFile(object):
    _file: Element

    def __init__(self, e):
        self._file = e

    @property
    def id(self) -> int:
        return int(self._file.attrib['id'])

    @property
    def name(self) -> str:
        return self._file.find('name').text

    def extended_items(self) -> List[XarFileExtendedItem]:
        pass


class XarSignature(object):
    _style: str


class XarChecksum(object):
    _style: str
    _value: bytes

    def __init__(self, style: str, value: bytes):
        self._style = style
        self._value = value


class XarHeader(object):
    _version: int
    _toc_compressed_size: int
    _toc_size: int
    _header_size: int
    _checksum: XarChecksumAlgorithm

    def __init__(self, fp: BinaryIO):
        header = int.from_bytes(fp.read(4), "big", signed=False)
        if header != XAR_SIGNATURE:
            raise IOError("Signature mismatch")
        self._header_size = int.from_bytes(fp.read(2), "big", signed=False)
        self._version = int.from_bytes(fp.read(2), "big", signed=False)
        self._toc_compressed_size = int.from_bytes(fp.read(8), "big", signed=False)
        self._toc_size = int.from_bytes(fp.read(8), "big", signed=False)
        self._checksum = XarChecksumAlgorithm(int.from_bytes(fp.read(4), "big", signed=False))

    @property
    def header_size(self) -> int:
        return self._header_size

    @property
    def toc_compressed_size(self) -> int:
        return self._toc_compressed_size

    @property
    def toc_size(self) -> int:
        return self._toc_size


class XarReader(object):
    _file: BinaryIO
    _toc: Element

    def __init__(self, fp: BinaryIO):
        self._file = fp
        self._header = XarHeader(fp)
        fp.seek(self._header.header_size)
        toc_data = zlib.decompress(fp.read(self._header.toc_compressed_size))
        if len(toc_data) != self._header.toc_size:
            raise IOError("Invalid TOC")
        self._toc = fromstring(toc_data)

    @property
    def files(self) -> List[XarFile]:
        for file_item in self._toc.findall('.//file'):
            yield XarFile(file_item)

    def signatures(self) -> List[XarSignature]:
        pass

    def checksums(self) -> List[XarChecksum]:
        pass
