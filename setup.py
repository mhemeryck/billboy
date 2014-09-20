from setuptools import setup


def readme(filename='README.md'):
    """return README contents"""

    with open(filename, 'r') as fh:
        return fh.read()


def requirements(filename='requirements.txt'):
    """return install requirements"""

    with open(filename, 'r') as fh:
        return fh.read().splitlines()


setup(
    name='billboy',
    version='1.1',
    author='Martijn Hemeryck',
    author_email='martijn.hemeryck@soundtalks.com',
    url='https://github.com/mhemeryck/billboy/',
    packages=['app'],
    description='billboy',
    long_description=readme(),
    install_requires=requirements()
)
