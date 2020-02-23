# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
import zlib


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Xp3(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._root.Header(self._io, self, self._root)

    class FileIndex(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xp3fileindex_compressed_flag = self._io.read_u1()
            if self.xp3fileindex_compressed_flag == 1:
                self.compressed_size = self._io.read_u8le()

            self.uncompressed_size = self._io.read_u8le()
            if self.xp3fileindex_compressed_flag == 1:
                self._raw__raw_file_entries_compressed = self._io.read_bytes(self.compressed_size)
                self._raw_file_entries_compressed = zlib.decompress(self._raw__raw_file_entries_compressed)
                _io__raw_file_entries_compressed = KaitaiStream(BytesIO(self._raw_file_entries_compressed))
                self.file_entries_compressed = self._root.FileEntries(_io__raw_file_entries_compressed, self, self._root)

            if self.xp3fileindex_compressed_flag == 0:
                self._raw_file_entries_uncompressed = self._io.read_bytes(self.uncompressed_size)
                _io__raw_file_entries_uncompressed = KaitaiStream(BytesIO(self._raw_file_entries_uncompressed))
                self.file_entries_uncompressed = self._root.FileEntries(_io__raw_file_entries_uncompressed, self, self._root)



    class FileEntries(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_entry = []
            i = 0
            while not self._io.is_eof():
                self.file_entry.append(self._root.FileEntry(self._io, self, self._root))
                i += 1



    class InfoChunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()
            self.flags = self._io.read_u4le()
            self.uncompressed_size = self._io.read_u8le()
            self.compressed_size = self._io.read_u8le()
            self.file_path_length = self._io.read_u2le()
            self.file_path = (self._io.read_bytes((2 + (self.file_path_length * 2)))).decode(u"utf-16le")


    class AdlrChunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()
            self.adler32 = self._io.read_u4le()


    class FileChunks(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_chunk = []
            i = 0
            while not self._io.is_eof():
                self.file_chunk.append(self._root.FileChunk(self._io, self, self._root))
                i += 1



    class SegmChunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()
            self.is_compressed = self._io.read_bits_int(1) != 0
            self._io.align_to_byte()
            self.padding = self._io.read_bytes(3)
            self.offset = self._io.read_u8le()
            self.uncompressed_size = self._io.read_u8le()
            self.compressed_size = self._io.read_u8le()


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xp3signature = self._io.ensure_fixed_contents(b"\x58\x50\x33\x0D\x0A\x20\x0A\x1A\x8B\x67\x01")
            self.offset = self._io.read_u8le()
            self.ignored_bytes = self._io.read_bytes(((self.offset - 11) - 8))
            self.flag = self._io.read_u1()
            self.padding = self._io.read_u8le()
            self.file_index_offset = self._io.read_u8le()


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes(4)).decode(u"ascii")
            self.file_chunks_size = self._io.read_u8le()
            self._raw_file_chunks = self._io.read_bytes(self.file_chunks_size)
            _io__raw_file_chunks = KaitaiStream(BytesIO(self._raw_file_chunks))
            self.file_chunks = self._root.FileChunks(_io__raw_file_chunks, self, self._root)


    class FileChunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.key = (self._io.read_bytes(4)).decode(u"ascii")
            _on = self.key
            if _on == u"time":
                self.values = self._root.TimeChunk(self._io, self, self._root)
            elif _on == u"adlr":
                self.values = self._root.AdlrChunk(self._io, self, self._root)
            elif _on == u"segm":
                self.values = self._root.SegmChunk(self._io, self, self._root)
            elif _on == u"info":
                self.values = self._root.InfoChunk(self._io, self, self._root)


    class TimeChunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()
            self.timestamp = self._io.read_u8le()


    @property
    def index(self):
        if hasattr(self, '_m_index'):
            return self._m_index if hasattr(self, '_m_index') else None

        _pos = self._io.pos()
        self._io.seek(self.header.file_index_offset)
        self._m_index = self._root.FileIndex(self._io, self, self._root)
        self._io.seek(_pos)
        return self._m_index if hasattr(self, '_m_index') else None


