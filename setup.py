from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='microsat-uitl',
    version='0.1.0',
    description='A sample Python project',
    long_description=long_description,
    url='https://github.com/phl-microsat-dpad/microsat-util',

    author='Benjie Jiao',
    author_email='hi@benjie.me',
    license='MIT',
    packages=['microsat_util'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='gis geoinformatics image-processing remote-sensing rs',
)