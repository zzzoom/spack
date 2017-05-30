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
from spack import *


class Amanzi(CMakePackage):
    """Amanzi is a parallel flow and reactive transport simulator that 
    supports transient and steady-state saturated and unsaturated flows, 
    and wide variety of geochemical reactions."""

    homepage = "https://software.lanl.gov/ascem/amanzi"
    url      = "https://github.com/amanzi/amanzi/archive/ats-amanzi-0.86.p2.tar.gz"

    version('ideas', git='https://github.com/amanzi/amanzi.git', branch='amanzi-ideas')
    version('0.86.p2', 'bcb9f10de6bf3866ba63be7a8a362e2d')

    variant('debug', default=False,
            description='Builds a debug version of the librarires')
    variant('shared', default=False,
            description='Enables the build of shared libraries')
    variant('structured', default=False,
            description='')
    variant('unstructured', default=False,
            description='')

    depends_on('mpi')
    depends_on('boost')
    depends_on('hdf5')
    depends_on('trilinos~tpetra')
    depends_on('exodusii')
    depends_on('xerces-c')
    depends_on('unittest-cpp')
    depends_on('ascem-io')
    depends_on('netcdf')
    depends_on('boxlib@1.3.4', when='+structured')
    depends_on('petsc@3.5.2~superlu-dist',  when='+structured')
    depends_on('mstk')
#    depends_on('metis')

    def cmake_args(self):
        spec = self.spec
        args = []

        args.extend(['-DCMAKE_BUILD_TYPE:STRING=%s' %
            ('DEBUG' if '+debug' in spec else 'RELEASE')])

        args.extend(['-DBUILD_SHARED_LIBS:BOOL=%s' %
            ('ON' if '+shared' in spec else 'OFF')])
        
        args.extend(['-DENABLE_Structured:BOOL=%s' %
            ('ON' if '+structured' in spec else 'OFF')])

        args.extend(['-DENABLE_Unstructured:BOOL=%s' %
            ('ON' if '+unstructured' in spec else 'OFF')])

        args.extend(['-DAMANZI_PRECISION=DOUBLE'])

        # Add MPI
        args.extend(['-DENABLE_MPI:BOOL=ON',
                     '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                     '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                     '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
        ])

        # Add HDF5
        args.extend(['-DHDF5_ROOT=%s' % spec['hdf5'].prefix])

        # Add Trilinos
        args.extend(['-DTrilinos_INSTALL_PREFIX=%s' % spec['trilinos'].prefix])

        # Add NetCDF
        args.extend(['-DNetCDF_DIR=%s' % spec['netcdf'].prefix])

        # Add ExodusII
        args.extend(['-DExodusII_DIR=%s' % spec['exodusii'].prefix])

        # Add XERCES
        args.extend(['-DXERCES_DIR=%s' % spec['xerces-c'].prefix])

        # Add UnitTest
        args.extend(['-DUnitTest_DIR=%s' % spec['unittest-cpp'].prefix])

        # Add boost
        args.extend(['-DBOOST_ROOT=%s' % spec['boost'].prefix])

        # Add ASCEM-IO
        args.extend(['-DASCEMIO_DIR=%s' % spec['ascem-io'].prefix])

        if '+structured' in spec:
            args.extend(['-DCCSE_DIR=%s' % spec['boxlib'].prefix,
                         '-DAMANZI_SPACEDIM:INT=3',
                         '-DCMAKE_EXE_LINKER_FLAGS=-lgfortran -lmpi_mpifh'])
            
            args.extend(['-DPETSC_DIR=%s' % spec['petsc'].prefix])

        if '+unstructured' in spec:
            args.extend(['-DENABLE_MSTK_Mesh:BOOL=ON',
                         '-DMSTK_DIR=%s' % spec['mstk'].prefix,
                         '-DMSTK_VERSION=2',
                         '-DMSTK_VERSION_MINOR:STRING=27'])
#
#        args.extend(['-DMETIS_DIR=%s' % spec['metis'].prefix])

        return args
