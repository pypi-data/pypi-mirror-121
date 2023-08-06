#!/usr/bin/env python
import os
from setuptools import setup, Extension
sources = [
    'src/python/core.c',
    'src/libethash/io.c',
    'src/libethash/internal.c',
    'src/libethash/sha3.c']
if os.name == 'nt':
    sources += [
        'src/libethash/util_win32.c',
        'src/libethash/io_win32.c',
        'src/libethash/mmap_win32.c',
    ]
else:
    sources += [
        'src/libethash/io_posix.c'
    ]
depends = [
    'src/libethash/ethash.h',
    'src/libethash/compiler.h',
    'src/libethash/data_sizes.h',
    'src/libethash/endian.h',
    'src/libethash/ethash.h',
    'src/libethash/io.h',
    'src/libethash/fnv.h',
    'src/libethash/internal.h',
    'src/libethash/sha3.h',
    'src/libethash/util.h',
]
pyetchash = Extension('pyetchash',
                     sources=sources,
                     depends=depends,
                     extra_compile_args=["-Isrc/", "-std=gnu99", "-Wall"])

setup(
    name='pyetchash',
    author="Andrei Kondakov",
    author_email="and.kondakov94@gmail.com",
    license='GPL',
    version='0.1.26',
    url='https://github.com/andrei-kondakov/etchash',
    download_url='https://github.com/ethereum/ethash/tarball/v23',
    description=('Python wrappers for etchash'),
    ext_modules=[pyetchash],
)
