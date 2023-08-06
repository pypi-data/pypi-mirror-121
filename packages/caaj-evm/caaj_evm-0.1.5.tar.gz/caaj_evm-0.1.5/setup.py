"""erc20transfer"""

from setuptools import setup, find_packages
from glob import glob

setup(
    name='caaj_evm',
    version='0.1.5',
    license='mit',
    description='tools for generateing caaj',

    author='bitblt',
    author_email='ywakimoto1s@gmail.com',
    url='https://github.com/ca3-caaip/caaj_evm',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')] 
)

