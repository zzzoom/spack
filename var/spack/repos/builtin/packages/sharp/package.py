# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sharp(Package):
    """NVIDIA® Mellanox® Scalable Hierarchical Aggregation and Reduction
    Protocol (SHARP)™ technology improves upon the performance of MPI and
    Machine Learning collective operation, by offloading collective operations
    from the CPU to the network and eliminating the need to send data multiple
    times between endpoints."""

    homepage = "https://docs.nvidia.com/networking/category/mlnxsharp"
    has_code = False

    # To get the version number
    # grep SHARP_VERNO_STRING path/include/sharp/api/version.h
    version("3.3")
    version("3.2")
    version("3.1")

    # SHARP needs to be added as an external package to SPACK. For this, the
    # config file packages.yaml needs to be adjusted:
    #
    # packages:
    #   sharp:
    #     buildable: False
    #     externals:
    #     - spec: sharp@3.1
    #       prefix: /opt/mellanox/sharp (path to your HCOLL installation)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
