import os
from codecs import open
from pathlib import Path
from typing import List

from setuptools import setup


def package_files(directory: str, excelude_suffix_list: List=[]) -> List[str]:
    directory_path = Path("kubetwo") / directory
    paths = []
    excelude_suffix_list = ["." + excelude_suffix for excelude_suffix in excelude_suffix_list]
    for path in directory_path.glob("**/*"):
        if path.suffix in excelude_suffix_list:
            continue
        paths.append(str(path.relative_to("kubetwo")))
    return paths


all_package_files = \
    package_files("ansible_template") + \
    package_files("data") + \
    package_files("kubernetes_sample") + \
    package_files("terraform_template")

here = Path(os.path.dirname(__file__))

with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

with open(here / "requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="kubetwo",
    version="0.1.0",
    description="Simple CLI tool to create Kubernetes cluster on AWS EC2.",
    long_description=long_description,
    author="opeco17",
    url="https://github.com/opeco17/kubetwo",
    long_description_content_type="text/markdown",
    packages=["kubetwo"],
    package_data={"kubetwo": all_package_files},
    install_requires=install_requires,
    license="Apache License 2.0",
    python_requires=">= 3.6",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology"
    ],
    keywords="kubetwo kube-two kube2 kube-2",
    entry_points={
        "console_scripts": [
            "kubetwo = kubetwo.cli:main"
        ]
    }
)
