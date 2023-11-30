#!/bin/bash

cd src/judger
make clean
make
cd ../..

# Install judger and its dependencies
pip3 install .