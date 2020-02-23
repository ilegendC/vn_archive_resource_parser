meta:
  id: xp3
  application: xp3
  file-extension: xp3
  endian: le

seq:
  - id: header
    type: header
instances:
  index:
    pos: header.file_index_offset
    type: file_index
types:
  header:
    seq:
      - id: xp3signature
        contents: ["XP3\r\n \n", 0x1a , 0x8b , 0x67 , 0x01]
      - id: offset
        type: u8
      - id: ignored_bytes
        size: offset - 11 - 8
      - id: flag
        type: u1 # XP3FileIndexContinue == 0x80
      - id: padding
        type: u8
      - id: file_index_offset
        type: u8
  file_index:
    seq:
      - id: xp3fileindex_compressed_flag
        type: u1 # XP3FileIndexCompressed == 0x01, XP3FileIndexUncompressed == 0x00
      - id: compressed_size
        type: u8
        if: xp3fileindex_compressed_flag == 0x01
      - id: uncompressed_size
        type: u8
      - id: file_entries_compressed
        size: compressed_size
        process: zlib
        type: file_entries
        if: xp3fileindex_compressed_flag == 0x01
      - id: file_entries_uncompressed
        size: uncompressed_size
        type: file_entries
        if: xp3fileindex_compressed_flag == 0x00
  file_entries:
    seq:
      - id: file_entry
        type: file_entry
        repeat: eos
  file_entry:
    seq:
      - id: name  # first chunk should be 'File', if not most likely an encryption chunk
        type: str
        size: 4
        encoding: ascii
      - id: file_chunks_size
        type: u8
      - id: file_chunks
        type: file_chunks
        size: file_chunks_size
  file_chunks:
    seq:
      - id: file_chunk
        type: file_chunk
        repeat: eos
  file_chunk:
    seq:
      - id: key
        type: str
        size: 4
        encoding: ascii
      - id: values
        type:
          switch-on: key
          cases:
            '"time"': time_chunk
            '"adlr"': adlr_chunk
            '"segm"': segm_chunk
            '"info"': info_chunk
  time_chunk:
    seq:
      - id: size
        type: u8
      - id: timestamp
        type: u8
  adlr_chunk:
    seq:
      - id: size
        type: u8
      - id: adler32
        type: u4
  segm_chunk:
    seq:
      - id: size
        type: u8
      - id: is_compressed
        type: b1
      - id: padding
        size: 3
      - id: offset
        type: u8
      - id: uncompressed_size
        type: u8
      - id: compressed_size
        type: u8
  info_chunk:
    seq:
      - id: size
        type: u8
      - id: flags
        type: u4
      - id: uncompressed_size
        type: u8
      - id: compressed_size
        type: u8
      - id: file_path_length
        type: u2
      - id: file_path
        size: 2 + file_path_length * 2
        type: str
        encoding: utf-16le
