
from setuptools import setup, find_packages
from backpedal import VERSION


f = open('README-pypi.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(name='backpedal',
    version=VERSION,
    description="Backpedal",
    long_description=LONG_DESCRIPTION,
    author='BJ Dierkes',
    author_email='derks@datafolklabs.com',
    url='http://github.com/datafolklabs/backpedal',
    license='BSD-three-clause',
    packages=find_packages(exclude=['ez_setup', 'example', 'tests']),
    include_package_data=True,
    zip_safe=False,
)
