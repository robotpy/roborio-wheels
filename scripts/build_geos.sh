#!/bin/bash -e

/build/venv/bin/build-pip install cmake ninja

[ -f geos-3.13.0.tar.bz2 ] || wget https://download.osgeo.org/geos/geos-3.13.0.tar.bz2
[ -d geos-3.13.0 ] || tar -xf geos-3.13.0.tar.bz2

cd geos-3.13.0/

mkdir build
cd build
/build/venv/build/bin/cmake \
    -DCMAKE_TOOLCHAIN_FILE=../../roborio-toolchain.cmake \
    -DCMAKE_MAKE_PROGRAM=/build/venv/build/bin/ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local/arm-nilrt-linux-gnueabi/sysroot/usr \
    -DBUILD_DOCUMENTATION=OFF \
    -DBUILD_TESTING=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -G Ninja \
    ..

/build/venv/build/bin/cmake --build .
/build/venv/build/bin/cmake --install .
