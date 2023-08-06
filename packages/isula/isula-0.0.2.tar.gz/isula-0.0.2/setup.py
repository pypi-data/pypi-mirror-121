from setuptools import setup

setup(
    name='isula',
    version='0.0.2',
    author='openEuler community',
    author_email='dev@openeuler.org',
    description='python sdk for isulad and isula-build',
    url='https://gitee.com/openeuler/pyisula',
    packages=['isula'],
    install_requires=['grpc'],
)
