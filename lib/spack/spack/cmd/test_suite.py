##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse
import spack
import pytest

from llnl.util.filesystem import *
from spack.util.sandboxtestsuite import  sandbox_test_suite  

description = "test installation of a suite of packages; generate cdash output"


def setup_parser(subparser):
    subparser.add_argument(
        '--log-format', choices=['cdash', 'cdash-simple'],
        default='cdash-simple', help="format to use for log files")
    subparser.add_argument(
        '--site', action='store', help='Location where testing occurred.')
    subparser.add_argument(
        '--cdash', action='store', default=None,
        help='URL of a cdash server (default spack.io/cdash)')
    subparser.add_argument(
        '--project', action='store', default=None,
        help='project name on cdash (default spack)')
    subparser.add_argument(
        '-o', '--output', metavar='dir', action='store', default=None,
        help='output directory for test data')
    subparser.add_argument(
        '--dry-run', action='store_true',
        help='only print specs that would be installed')
    subparser.add_argument(
        '-gt', '--generate-tests', action='store_true',
        help='generate tests')
    subparser.add_argument(
        '--gt-type', choices=['all-tests', 'days', 'xsdk'],
        default='all-tests',
        help='type of tests to generate. Default is all-tests')
    subparser.add_argument(
        '--gt-by-compiler', action='store_true',
        help='Seperate file per compiler')
    subparser.add_argument(
        '--gt-system-compilers', action='store_true',
        help='Use compilers found on system.')
    subparser.add_argument(
        '-p', '--performance', action='store_true',
        help='sorts specs for better performance')
    subparser.add_argument(
        'yaml_files', nargs=argparse.REMAINDER,
        help="YAML test suite files, or a directory of them")

def test_suite(parser, args):
    with working_dir(spack.prefix):
        return pytest.main([sandbox_test_suite(args)]) 
