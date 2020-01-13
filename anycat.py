#!/usr/bin/env python
"""An elegant cat replacement for a more civilized age."""

import distutils.spawn
import io
import os
import subprocess
import sys

import smart_open

MAGIC_FLAG = '-__ANYCAT_MAGIC__'
CAT_BIN = distutils.spawn.find_executable('cat')


def parse_args():
    uris = []
    flags = []
    for x in sys.argv[1:]:
        if x.startswith('-') and len(x) > 1:
            flags.append(x)
        else:
            uris.append(x)

    return uris, flags


def read_config(uri):
    return {}, {}


def write_to_stdout(uri, stdout=sys.stdout.buffer):
    transport_params, kwargs = read_config(uri)

    if 'ignore_ext' not in kwargs:
        kwargs.update(ignore_ext=True)

    if uri == '-':
        fin = sys.stdin.buffer
    else:
        fin = smart_open.open(
            uri, 'rb',
            transport_params=transport_params, **kwargs,
        )

    while True:
        data = fin.read(io.DEFAULT_BUFFER_SIZE)
        if not data:
            break
        stdout.write(data)


def die():
    #
    # https://stackoverflow.com/questions/26692284/how-to-prevent-brokenpipeerror-when-doing-a-flush-in-python#26738736
    # Python flushes standard streams on exit; redirect remaining output
    # to devnull to avoid another BrokenPipeError at shutdown
    #
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)  # Python exits with error code 1 on EPIPE


def my_except_hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        pass
    else:
        sys.__excepthook__(exctype, value, traceback)


def wrapper_main():
    uris, flags = parse_args()

    if len(uris) == 0:
        subprocess.check_call(CAT_BIN)
    elif MAGIC_FLAG in flags:
        try:
            for uri in uris:
                write_to_stdout(uri)
        except BrokenPipeError:
            #
            # This happens when the reader of our stdout suddenly dies.
            #
            die()
    else:
        first_command = [sys.executable, __file__, MAGIC_FLAG] + uris
        first = subprocess.Popen(first_command, stdout=subprocess.PIPE)
        cat = subprocess.Popen([CAT_BIN] + flags, stdin=first.stdout)
        cat.wait()
        sys.exit(0)


def standalone_main():
    uris, flags = parse_args()
    try:
        for uri in uris:
            write_to_stdout(uri)
    except BrokenPipeError:
        die()


if __name__ == '__main__':
    sys.excepthook = my_except_hook

    if CAT_BIN:
        wrapper_main()
    else:
        #
        # Inferior O/S without cat.
        #
        standalone_main()
