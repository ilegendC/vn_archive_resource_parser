#!/usr/bin/env python3

import kaitaistruct
from xp3 import *
import os.path, os, sys, zlib

if len(sys.argv) < 2:
    print('Usage: parse.py input.xp3 [output_dir]')
    exit(0)

if len(sys.argv) < 3:
    sys.argv.append('output')

output_dir = os.path.join(os.getcwd(), sys.argv[2])
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

error_count = 0
file = Xp3.from_file(sys.argv[1])
file_entries = file.index.file_entries_compressed if hasattr(file.index, 'file_entries_compressed') else file.index.file_entries_uncompressed
if os.path.exists(sys.argv[1]):
    with open(sys.argv[1], 'rb') as r:
        for file_entry in file_entries.file_entry:
            is_compressed = False
            offset = -1
            size = -1
            file_path = 'temp.file'
            for file_chunk in file_entry.file_chunks.file_chunk:
                if file_chunk.key == 'segm':
                    is_compressed = file_chunk.values.is_compressed
                    offset = file_chunk.values.offset
                    size = file_chunk.values.compressed_size if is_compressed else file_chunk.values.uncompressed_size
                elif file_chunk.key == 'info':
                    file_path = file_chunk.values.file_path
                    file_path = file_path[:-1] if file_path[-1] == '\x00' else file_path

            dest_path = os.path.join(output_dir, file_path)
            dest_dirpath = os.path.dirname(dest_path)
            os.makedirs(dest_dirpath, exist_ok=True)

            try:
                with open(dest_path, 'wb') as f:
                    r.seek(offset)
                    raw_data = r.read(size)
                    if is_compressed:
                        raw_data = zlib.decompress(raw_data)
                    written_bytes = f.write(raw_data)
                    assert written_bytes == len(raw_data)
                print('Extracted', file_path)
            except Exception as e:
                print(e)
