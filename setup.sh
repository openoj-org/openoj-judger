#!/bin/bash

# Make sure you have docker installed and running
docker build -t oj .

# Install judger and its dependencies
pip3 install .