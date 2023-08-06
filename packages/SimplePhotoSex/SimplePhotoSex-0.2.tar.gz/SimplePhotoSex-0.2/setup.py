import sys
import os
#from distutils.core import setup
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="SimplePhotoSex",
    version="0.2",
    packages=["download_panstar", "PhotoSex"],
    package_dir={"download_panstar": "download_panstar","PhotoSex":"PhotoSex"},
    #package_data={"pnicer": ["tests_resources/*.fits"]},
    #install_requires=["numpy>=1.11", "scipy>=0.18", "scikit-learn>=0.18", "matplotlib>=1.5", "astropy>=1.3"],
    url="https://gitee.com/zhang-miaomiao1983/photsex",
    license="MIT",
    author="Miaomiao Zhang",
    author_email="mmzhang83@163.com",
    description="A simple tool to perform aperture or PSF photometry with Sextractor+PSFEX",
    long_description=read('README.md'),
    long_description_content_type='text/plain',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
