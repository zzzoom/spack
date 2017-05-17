##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mstk
#
# You can edit this file again by typing:
#
#     spack edit mstk
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Mstk(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/MeshToolkit/MSTK/archive/v2_27.tar.gz"

    version('2_27_rc3', 'feea4e200b802a58e6baf62538ffb18a')
    version('2_27_rc2', '100fe5b67f8bcf7647f974d9bb28e06b')
    version('2_27_rc1', '2d4222b8b113372277dce863be59cc30')
    version('2_27',     'ca1b56dd334fa7023d28df46de46a098')
    version('2_26_rc5', 'f46b05bbb2baaa1fd4bdfdd9a3c3341a')
    version('2_26_rc4', 'a3902cace339ce1669530f63722df6e2')
    version('2_26_rc3', 'ade95b5f26962aec655fdcf592b24943')
    version('2_26_rc2', 'e7bb01545c812b24b4dffd2a3e7562d5')
    version('2_26',     'be8c4c1d4f13b23d00ce2020d2354351')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
