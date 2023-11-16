from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="judger",
    version="0.0.1",
    description="A simple judger",
    author="Tian Sibo",
    author_email="tsb20@mails.tsinghua.edu.cn",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
