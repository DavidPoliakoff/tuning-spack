Steps: get spack, as of this moment 0.16.1 seems good

Clone this repo

Spack repo add /path/to/this/repo/root

cd builds/openmp or builds/cuda

spack env activate .

spack concretize -f

spack install
