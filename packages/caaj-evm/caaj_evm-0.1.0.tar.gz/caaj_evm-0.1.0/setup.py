"""erc20transfer"""

from setuptools import setup, find_packages

setup(
    name='caaj_evm',
    version='0.1.0',
    license='mit',
    description='tools for generateing caaj',

    author='bitblt',
    author_email='ywakimoto1s@gmail.com',
    url='https://github.com/ca3-caaip/caaj_evm',

    packages=find_packages(where='erc20transfer'),
    package_dir={'': 'erc20transfer'},
)

