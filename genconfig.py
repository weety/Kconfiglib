#!/usr/bin/env python

# Copyright (c) 2018, Ulf Magnusson
# SPDX-License-Identifier: ISC

# Generates a C header from the configuration, matching the format of
# include/generated/autoconf.h in the kernel.
#
# Optionally generates a directory structure with one file per symbol that can
# be used to implement incremental builds. See the docstring for
# Kconfig.sync_deps() in Kconfiglib.
#
# Usage (see argument help texts for more information):
#
#   genconfig.py [-h] [--header-path HEADER_FILE] [--sync-deps [OUTPUT_DIR]] [KCONFIG_FILENAME]

import argparse

import kconfiglib

DESCRIPTION = """
Generates a header file with defines from the configuration. Optionally
creates/updates a directory with incremental build information as well (see the
docstring for the Kconfig.sync_deps() function in Kconfiglib). The .config file
to generate the configuration from can be specified by setting the
KCONFIG_CONFIG environment variable.
"""

DEFAULT_HEADER_PATH = "config.h"
DEFAULT_SYNC_DEPS_PATH = "deps/"

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        "--header-path",
        metavar="HEADER_FILE",
        default=DEFAULT_HEADER_PATH,
        help="path for the generated header file (default: {})"
             .format(DEFAULT_HEADER_PATH))

    parser.add_argument(
        "--sync-deps",
        dest="sync_deps_path",
        metavar="OUTPUT_DIR",
        nargs="?",
        default=None,
        const=DEFAULT_SYNC_DEPS_PATH,
        help="enable generation of build dependency information for "
             "incremental builds, optionally specifying the output path "
             "(default: {})".format(DEFAULT_SYNC_DEPS_PATH))

    parser.add_argument(
        "kconfig_filename",
        metavar="KCONFIG_FILENAME",
        nargs="?",
        default="Kconfig",
        help="top-level Kconfig file (default: Kconfig)")

    args = parser.parse_args()


    kconf = kconfiglib.Kconfig(args.kconfig_filename)

    kconf.load_config(kconfiglib.standard_config_filename())

    kconf.write_autoconf(args.header_path)
    if args.sync_deps_path is not None:
        kconf.sync_deps(args.sync_deps_path)

if __name__ == "__main__":
    main()
