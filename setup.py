from kosmorrolib.core import VERSION
from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name='kosmorro',
    version=VERSION,
    author='Jérôme Deuchnord',
    author_email='jerome@deuchnord.fr',
    url='https://kosmorro.astronewbie.space',
    license='AGPL-3.0',
    description='A program that computes the ephemerides.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='kosmorro astronomy ephemerides ephemeris',
    packages=find_packages(),
    scripts=['kosmorro'],
    install_requires=['skyfield>=1.13.0,<2.0.0', 'tabulate', 'numpy>=1.17.0,<2.0.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: Astronomy'
    ]
)
