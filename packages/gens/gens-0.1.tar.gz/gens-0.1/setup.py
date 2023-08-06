"""
Setup the Python package
"""

import pathlib
import re
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

WORK_DIR = pathlib.Path(__file__).parent


def get_version():
    """ Get version """

    txt = (WORK_DIR / 'gens' / '__init__.py').read_text('utf-8')

    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError as e:
        raise RuntimeError('Unable to determine version') from e


setup(
    name='gens',
    version=get_version(),
    description='Code & token generators',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kosyachniy/gens',
    author='Alexey Poloz',
    author_email='polozhev@mail.ru',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='generate, codes, tokens, ids, passwords, generator',
    packages=find_packages(exclude=('tests',)),
    python_requires='>=3.7, <4',
    project_urls={
        'Source': 'https://github.com/kosyachniy/gens',
    },
    license='MIT',
    include_package_data=False,
)
