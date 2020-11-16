from setuptools import setup, find_packages
from greaseweazle import version

setup(
    name="Greaseweazle",
    description='Tools and USB interface for accessing a floppy drive at the raw flux level',
    url='https://github.com/keirf/Greaseweazle',
    version=f'{version.major}.{version.minor}',
    author="Keir Fraser",
    author_email="keir.xen@gmail.com",
    packages=find_packages(),
    install_requires=[
        'crcmod',
        'pyserial',
        'bitarray',
    ],
)
