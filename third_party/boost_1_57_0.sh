#!/bin/bash
set -x # echo on

kTmp="$(pwd)/tmp"

# boost 1.57.0
tar -xzf "$kTmp/boost_1_57_0.tar.gz" -C "$kTmp"

# bzip2 1.0.6
tar -xzf "$kTmp/bzip2-1.0.6.tar.gz" -C "$kTmp"
export BZIP2_SOURCE="$kTmp/bzip2-1.0.6"

# icu 54.1
tar -xzf "$kTmp/icu4c-54_1-src.tgz" -C "$kTmp"
#export ICU_PATH="$kTmp/icu"

# python 2.7.9
tar -xzf "$kTmp/Python-2.7.9.tgz" -C "$kTmp"
export PYTHON_ROOT="$kTmp/Python-2.7.9"
export PYTHON_VERSION=2.7

# zlib 1.2.8
tar -xzf "$kTmp/zlib-1.2.8.tar.gz" -C "$kTmp"
export ZLIB_SOURCE="$kTmp/zlib-1.2.8"


# icu
pushd "tmp/icu/source"

# see "https://github.com/aosm/ICU/blob/master/icuSources/runConfigureICU"
if [ "$(uname)" == "Darwin" ]; then
# Do something under Mac OS X platform        
kPlatform="MacOSX"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
# Do something under Linux platform
kPlatform="Linux"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
# Do something under Windows NT platform
kPlatform="MinGW"
fi

#chmod +x "configure" "install-sh" "runConfigureICU"
#./runConfigureICU "$kPlatform" --prefix="$kTmp" --enable-static
#make
#make install
popd

# compile
pushd "$kTmp/boost_1_57_0"
chmod +x bootstrap.sh
./bootstrap.sh
./b2 --prefix="$kTmp/../boost_1_57_0" --without-mpi toolset=clang cxxflags="-std=c++11 -stdlib=libc++" linkflags="-stdlib=libc++" variant=debug,release threading=multi link=static runtime-link=static address-model=64 --layout=tagged install
popd
