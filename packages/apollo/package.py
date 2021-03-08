# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Apollo(CMakePackage):
    homepage = "http://software.llnl.gov/Apollo/"
    git      = "https://github.com/DavidPoliakoff/Apollo.git"

    maintainers = ['davidbeckingsale']

    version('develop', branch='feature/integrated-kokkos-connector')
    version('main', branch='main')

    depends_on('opencv+ml~zlib~vtk~videostab~videoio~ts~tiff~superres~stitching~png~openmp~openclamdfft~openclamdblas~opencl_svm~opencl~lapack~jpeg~java~jasper~ipp_iw~ipp~imgproc~highgui~gtk~flann~features2d~eigen~dnn~calib3d')
    variant('mpi', default='Off')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):

        spec = self.spec
        options = []

        options.append('-DOpenCV_DIR={0}'.format(spec['opencv'].prefix))
        options.append('-DENABLE_MPI={0}'.format('ON' if '+mpi' in spec else 'OFF'))

        return options
