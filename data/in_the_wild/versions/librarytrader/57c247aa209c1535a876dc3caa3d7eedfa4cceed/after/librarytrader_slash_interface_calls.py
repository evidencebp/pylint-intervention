#!/usr/bin/env python3
#
# Copyright 2018, Andreas Ziegler <andreas.ziegler@fau.de>
#
# This file is part of librarytrader.
#
# librarytrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# librarytrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with librarytrader.  If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict
import logging
import multiprocessing
import os
import re
import subprocess
import sys
import time

import capstone
from elftools.common.exceptions import ELFError

# In order to be able to use librarytrader from git without having installed it,
# add top level directory to PYTHONPATH
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))

from librarytrader.library import Library

CALL_REGEX = re.compile(r'^call[q]?\s+([0-9a-f]+).*$')
JMP_REGEX = re.compile(r'^jmp[q]?\s+([0-9a-f]+).*$')
JNE_REGEX = re.compile(r'^j[n]?e\s+([0-9a-f]+).*$')

def disassemble_objdump(library, start, length, obj=None):
    disassembly = []
    if length == 0:
        return (disassembly, find_calls_from_objdump)

    # objdump requires addresses, not offsets
    start += library.load_offset

    cmdline = ['objdump', '-d', '--no-show-raw-insn',
               '--start-address={}'.format(hex(start)),
               '--stop-address={}'.format(hex(start + length)),
               library.fullname]
    proc = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
    out, _ = proc.communicate()
    instrs = out.decode().split('\n')[7:-1]
    for instr in instrs:
        try:
            pre, post = instr.split('\t')
            addr = pre[:-1].lstrip()
            decoded = post
            disassembly.append((addr, decoded))
        except ValueError as err:
            logging.error('%s %s %d %d %s', library.fullname, instr, start,
                                            length, err)

    return (disassembly, find_calls_from_objdump)

def find_calls_from_objdump(library, disas):
    calls_to_exports = set()
    calls_to_imports = set()
    calls_to_locals = set()

    for _, decoded in disas:
        match = CALL_REGEX.match(decoded)
        if not match:
            match = JMP_REGEX.match(decoded)
        if not match:
            match = JNE_REGEX.match(decoded)

        if match:
            # Symbols are offsets into the file, so we need to subtract the
            # load_offset from the call target again to properly match it
            target = int(match.group(1), 16) - library.load_offset
            if target in library.exported_addrs:
                calls_to_exports.add(target)
            elif target in library.exports_plt:
                calls_to_exports.add(library.exports_plt[target])
            elif target in library.imports_plt:
                calls_to_imports.add(library.imports_plt[target])
            elif target in library.local_functions:
                calls_to_locals.add(target)

    return (calls_to_exports, calls_to_imports, calls_to_locals)

def disassemble_capstone(library, start, length, cs_obj):
    disassembly = []
    if length == 0:
        return (disassembly, find_calls_from_capstone)

    # Seek to right address and get code bytes
    library.fd.seek(start)
    code = library.fd.read(length)

    disas = list(cs_obj.disasm(code, start))

    # If capstone didn't disassemble everything, try objdump instead
    if len(code) != sum(instr.size for instr in disas):
        logging.warning('incomplete disassembly for %s:%x: %d/%d bytes!',
                        library.fullname, start,
                        sum(instr.size for instr in disas), len(code))
        return disassemble_objdump(library, start, length)

    return (disas, find_calls_from_capstone)

def find_calls_from_capstone(library, disas):
    calls_to_exports = set()
    calls_to_imports = set()
    calls_to_locals = set()
    for instr in disas:
        if instr.group(capstone.x86_const.X86_GRP_CALL) \
                or instr.group(capstone.x86_const.X86_GRP_JUMP):
            try:
                target = int(instr.op_str, 16)
            except ValueError:
                continue
            if target in library.exported_addrs:
                calls_to_exports.add(target)
            elif target in library.exports_plt:
                calls_to_exports.add(library.exports_plt[target])
            elif target in library.imports_plt:
                calls_to_imports.add(library.imports_plt[target])
            elif target in library.local_functions:
                calls_to_locals.add(target)

    return (calls_to_exports, calls_to_imports, calls_to_locals)

def resolve_calls_in_library(library, disas_function=disassemble_capstone):
    logging.debug('Processing %s', library.fullname)
    before = time.time()
    internal_calls = defaultdict(set)
    external_calls = defaultdict(set)
    local_calls = defaultdict(set)
    ranges = library.get_function_ranges()

    # Disassemble with the right machine type
    arch = capstone.CS_MODE_64
    if library.elfheader['e_machine'] == 'EM_386':
        arch = capstone.CS_MODE_32
    cs_obj = capstone.Cs(capstone.CS_ARCH_X86, arch)
    cs_obj.detail = True

    for start, size in ranges:
        disas, resolution_function = disas_function(library, start, size, cs_obj)
        calls_to_exports, calls_to_imports, calls_to_locals = resolution_function(library, disas)
        if calls_to_exports:
            internal_calls[start] = calls_to_exports
        if calls_to_imports:
            external_calls[start] = calls_to_imports
        if calls_to_locals:
            local_calls[start] = calls_to_locals

    after = time.time()
    duration = after - before
    logging.info('Thread %d: %s took %.3f s', os.getpid(),
                                              library.fullname,
                                              duration)
    return (internal_calls, external_calls, local_calls, (after - before))

def map_wrapper(path):
    try:
        lib = Library(path, parse=True)
    except (OSError, ELFError) as err:
        logging.error('%s: %s', path, err)
        return (None, None, None, 0)
    internal_calls, external_calls, local_calls, duration = resolve_calls_in_library(lib)
    return (lib.fullname, internal_calls, external_calls, local_calls, duration)

def resolve_calls(store, n_procs=int(multiprocessing.cpu_count() * 1.5)):
    libs = [lib.fullname for lib in sorted(store.get_library_objects(),
                                           key=lambda x: -len(x.exported_addrs))]
    logging.info('Searching for calls in %d libraries...', len(libs))
    pool = multiprocessing.Pool(n_procs)
    result = pool.map(map_wrapper, libs, chunksize=1)
    pool.close()

    for fullname, internal_calls, external_calls, local_calls, _ in result:
        store[fullname].internal_calls = internal_calls
        store[fullname].external_calls = external_calls
        store[fullname].local_calls = local_calls

    logging.info('... done!')
    longest = [(v[0], v[4]) for v in sorted(result, key=lambda x: -x[4])]
    logging.info(longest[:20])
    logging.info('total number of calls: %d', sum(len(v[3].values()) +
                                                  len(v[2].values()) +
                                                  len(v[1].values())
                                                  for v in result))
    return result
