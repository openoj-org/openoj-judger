#!/bin/bash

# Make sure you have docker installed and running
cd src/judger
make clean
make
cd ../..

# Install judger and its dependencies
pip3 install .