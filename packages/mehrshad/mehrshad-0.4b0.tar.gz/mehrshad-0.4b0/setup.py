from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mehrshad',
    packages=['mehrshad'],
    version='0.4-beta',
    description=
    'A Python 3 module that contains all of my collections to let you code easier!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mehrshad Dadashzadeh',
    author_email='mehrdadashzadeh1379@gmail.com',
    url='https://github.com/mehrshaad/mehrshad-pypi',
    license='MIT',
    download_url=
    'https://github.com/mehrshaad/mehrshad-pypi/archive/refs/tags/v0.4-beta.tar.gz',
    keywords=['mehrshad', 'json', 'excel', 'text'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.4',
)

# import io
# import os

# from setuptools import find_packages, setup

# NAME = 'py-notifier'
# DESCRIPTION = 'Cross-platform desktop push-notifications.'
# URL = 'https://github.com/YuriyLisovskiy/pynotifier'
# EMAIL = 'yuralisovskiy98@gmail.com'
# AUTHOR = 'Yuriy Lisovskiy'
# REQUIRES_PYTHON = '>=3.6.0'
# VERSION = (0, 3, 0)

# REQUIRED = [
#     "win10toast==0.9; platform_system=='Windows'",
#     "pync==2.0.3; platform_system=='Darwin'",
# ]

# here = os.path.abspath(os.path.dirname(__file__))

# try:
#     with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#         long_description = '\n' + f.read()
# except FileNotFoundError:
#     long_description = DESCRIPTION

# setup(
#     name=NAME,
#     version='.'.join(map(str, VERSION)),
#     description=DESCRIPTION,
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     author=AUTHOR,
#     author_email=EMAIL,
#     python_requires=REQUIRES_PYTHON,
#     url=URL,
#     packages=find_packages(exclude=('tests', )),
#     install_requires=REQUIRED,
#     include_package_data=True,
#     license='MIT',
#     classifiers=[
#         # Full list: https://pypi.org/classifiers
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Environment :: MacOS X',
#         'Operating System :: MacOS',
#         'Operating System :: POSIX :: Linux',
#         'Operating System :: Microsoft :: Windows :: Windows 10'
#     ])
