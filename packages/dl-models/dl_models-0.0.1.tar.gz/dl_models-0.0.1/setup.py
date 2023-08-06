from setuptools import setup, find_packages
import os
from pathlib import Path


project_dir = Path(__file__).parent.parent


with open(os.path.join(project_dir, "requirements.txt")) as f:
    required_packages = f.read().splitlines()

setup(
    name="dl_models",
    version="0.0.1",
    description="Contains different neural networks",
    author="Nitin Kumar Mittal",
    author_email="nitinmittal234@gmail.com",
    packages=find_packages(include=["dl_models", "dl_models.*"]),
    install_requires=required_packages,
)
