#!/bin/sh

# Exit script if any line fails
set -e

Z3VER="4.7.1"
DIRN="venv_sasquatch"
virtualenv -p /usr/bin/python2.7 "$DIRN" --no-site-packages
source "$DIRN/bin/activate"

# Install dependencies needed for both
pip install numpy scipy 
# Install dependencies for pysvrt
# pip install torch torchvision cffi h5py
# Install dependencies needed for sasquatch
pip install matplotlib Pillow

cd "$DIRN"

wget "https://github.com/Z3Prover/z3/archive/z3-$Z3VER.tar.gz"

tar xvf "z3-$Z3VER.tar.gz" && rm "z3-$Z3VER.tar.gz"
mv "z3-z3-$Z3VER" z3
#
# Install Z3 into the virtual environment
cd z3
python scripts/mk_make.py
cd build
make
make install
cd ../../
#
# Test the installation of Z3
python -c 'import z3; print(z3.get_version_string())'

