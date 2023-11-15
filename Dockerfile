FROM ubuntu:20.04

# C & C++ environment
RUN apt-get update && apt-get install -y gcc g++ make

# Python environment
RUN apt-get install -y python3 python3-pip

# Java environment
# RUN apt-get install -y openjdk-11-jdk

# Set the working directory to /app
WORKDIR /home

# Set Python3 as default Python
RUN ln -sf /usr/bin/python3 /usr/bin/python