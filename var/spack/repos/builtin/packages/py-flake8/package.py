# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    url      = "https://github.com/PyCQA/flake8/archive/3.0.4.tar.gz"

    version('3.7.7', sha256='b3f76b02351008dc772276e74b09dd3d4b5c567ff8c6ab573352cb8fd7007444')
    version('3.7.6', sha256='2729990a3ec78ed17a2b6177bed2b18c6bfd152ca8ec20fff500a1e36ba761b4')
    version('3.7.5', sha256='64014a82b5d81d30393b505b71ec6457c7e8f2761d78bc1b27921bc9f0842580')
    version('3.7.4', sha256='eb27064b99d9f7d11a7e79c4265383d12fd912c44c605bc6a295d2fd7f5d4075')
    version('3.7.3', sha256='42af44b5da9fd5a4bd6f602f57e68b9f8f412aefcae3efc304ab4f862fbd24de')
    version('3.7.2', sha256='27f26794d0468383e186d387b41c677126c48416b9d2e1f354803843ca28a91f')
    version('3.7.1', sha256='b5da9b8cb1f54741c733150c6a898daffe9ef9d0373cf4dc7c082f39042d6931')
    version('3.7.0', sha256='9da2aa8e642a7d442ccf0a2594887a65f2079079d8b2c70f38fcaaf7c6e40a4e')
    version('3.6.0', sha256='c82a8b59c99e9c7862231b5739e8b1ceef6303cc1199bf508de654ad7a482ea8')
    version('3.5.0', sha256='60ffe2fdacce4ebe7cadc30f310cf1edfd8ff654ef79525d90cf0756e69de44e')
    version('3.0.4', sha256='87a2b642900a569fc2f27ab3b79573e0d02d2fee7445c6abab84eb33dcb60365')
    version('2.5.4', sha256='ce03cc1acbe1726775ca57b40fab1d177550debb2f2f6b7a3c860541f3971cf5')

    extends('python', ignore='bin/(pyflakes|pycodestyle)')
    depends_on('python@2.7:2.8,3.4:')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.
    depends_on('py-setuptools@30:', type=('build', 'run'))

    # entrypoints >= 0.3.0, < 0.4.0
    # FIXME @0.3.0:0.3.999 causes concretization to hang
    depends_on('py-entrypoints@0.3', when='@3.7.7', type=('build', 'run'))

    # pyflakes >= 2.1.0, < 2.2.0
    depends_on('py-pyflakes@2.1.0:2.1.999', when='@3.7.7', type=('build', 'run'))
    # pyflakes >= 1.5.0, < 1.7.0
    depends_on('py-pyflakes@1.5.0:1.6.999', when='@3.5.0', type=('build', 'run'))
    # pyflakes >= 0.8.1, != 1.2.0, != 1.2.1, != 1.2.2, < 1.3.0
    depends_on('py-pyflakes@0.8.1:1.1.0,1.2.3:1.2.3', when='@3.0.4', type=('build', 'run'))
    # pyflakes >= 0.8.1, < 1.1
    depends_on('py-pyflakes@0.8.1:1.0.0', when='@2.5.4', type=('build', 'run'))

    # pycodestyle >= 2.5.0, < 2.6.0
    depends_on('py-pycodestyle@2.5.0:2.5.999', when='@3.7.7', type=('build', 'run'))
    # pycodestyle >= 2.3.0, < 2.4.0
    depends_on('py-pycodestyle@2.3.0:2.3.999', when='@3.5.0', type=('build', 'run'))
    # pycodestyle >= 2.0.0, < 2.1.0
    depends_on('py-pycodestyle@2.0.0:2.0.999', when='@3.0.4', type=('build', 'run'))
    # pep8 >= 1.5.7, != 1.6.0, != 1.6.1, != 1.6.2
    depends_on('py-pycodestyle@1.5.7,1.7.0:', when='@2.5.4', type=('build', 'run'))

    # mccabe >= 0.6.0, < 0.7.0
    depends_on('py-mccabe@0.6.0:0.6.999', when='@3.5.0,3.7.7', type=('build', 'run'))
    # mccabe >= 0.5.0, < 0.6.0
    depends_on('py-mccabe@0.5.0:0.5.999', when='@3.0.4', type=('build', 'run'))
    # mccabe >= 0.2.1, < 0.5
    depends_on('py-mccabe@0.2.1:0.4.0', when='@2.5.4', type=('build', 'run'))

    depends_on('py-configparser', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-enum34', when='^python@:3.1', type=('build', 'run'))

    # py-enum34 provides enum module from Python 3.4 for Python
    # versions 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, and 3.3; use built-in enum
    # module for Python versions 3.4 and later
    depends_on('py-enum34', when='^python@2.4:2.7.999,3.1:3.3.999',
               type=('build', 'run'))

    depends_on('py-functools32', when='@3.7.7: ^python@:3.1.999', type=('build', 'run'))
    depends_on('py-typing', when='@3.7.7: ^python@:3.4.999', type=('build', 'run'))

    depends_on('py-nose', type='test')

    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", 'setup.py', string=True)
