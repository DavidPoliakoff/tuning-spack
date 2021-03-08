# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TuningPlayground(CMakePackage):
    """Set of apps to test tuning"""

    homepage = "https://github.com/DavidPoliakoff/tuning-playground"
    url      = ""
    git      = "https://github.com/DavidPoliakoff/tuning-playground"

    maintainers = ['DavidPoliakoff']

    version('main', branch='main')

    # ArborX relies on Kokkos to provide devices, providing one-to-one matching
    # variants. The only way to disable those devices is to make sure Kokkos
    # does not provide them.
    kokkos_backends = {
        'serial': (True,  "enable Serial backend (default)"),
        'cuda': (False,  "enable Cuda backend"),
        'openmp': (False,  "enable OpenMP backend"),
        'hip': (False,  "enable HIP backend")
    }

    variant('mpi', default=False, description='enable MPI')
    for backend in kokkos_backends:
        deflt, descr = kokkos_backends[backend]
        variant(backend.lower(), default=deflt, description=descr)
    variant('trilinos', default=False, description='use Kokkos from Trilinos')

    depends_on('cmake@3.17:', type='build')
    depends_on('mpi', when='+mpi')

    # Standalone Kokkos
    depends_on('kokkos@3.1.00:', when='~trilinos')
    for backend in kokkos_backends:
        depends_on('kokkos+%s' % backend.lower(), when='~trilinos+%s' %
                   backend.lower())
    depends_on('kokkos+cuda_lambda', when='~trilinos+cuda')

    # Trilinos/Kokkos
    # Notes:
    # - there is no Trilinos release with Kokkos 3.1 yet
    # - current version of Trilinos package does not allow disabling Serial
    # - current version of Trilinos package does not allow enabling CUDA
    depends_on('trilinos+kokkos@develop', when='+trilinos')
    depends_on('trilinos+openmp', when='+trilinos+openmp')
    conflicts('~serial', when='+trilinos')
    conflicts('+cuda', when='+trilinos')

    def cmake_args(self):
        spec = self.spec

        options = [
            '-DKokkos_ROOT=%s' % (spec['kokkos'].prefix if '~trilinos' in spec
                                  else spec['trilinos'].prefix),
            '-DARBORX_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF')
        ]

        if '+cuda' in spec:
            # Only Kokkos allows '+cuda' for now
            options.append(
                '-DCMAKE_CXX_COMPILER=%s' % spec["kokkos"].kokkos_cxx)

        return options
