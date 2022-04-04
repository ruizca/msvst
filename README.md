MSVST
=======
The Multi-Scale Variance Stabilization Transform (MSVST, [Starck et al. 2009](https://arxiv.org/abs/0904.3299)) is a denoising algorithm based on wavelets suited for astronomical images. Here we provide a C++ implementation of the 2D and 2D+1D versions of the algorithm along with a python wrapper for ease of use.

The original C++ code was developed by CEA Saclay and distributed within the [Sparse2D](https://github.com/CosmoStat/Sparse2D) library.


Installation
-------------
This can be installed as a python package. However, for the compilation of the C++ code the following software and libraries should be available in your system: 
- C/C++ compiler
- [CMake](http://www.cmake.org)
- [CFITSIO](https://heasarc.gsfc.nasa.gov/fitsio/) (>V3.31)
- [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/)

In Ubuntu (and other Debian based linux distributions) these dependencies can be installed via apt:
```
sudo apt install gcc cmake libcfitsio* pkg-config
```
If available, the library will use OpenMPI for parallelization in multi-core systems.

Once the prerequisites are installed:
```
git clone git@github.com:ruizca/msvst.git
cd msvst
python setup.py install
```