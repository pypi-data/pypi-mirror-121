from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Ai Vision package'
LONG_DESCRIPTION = 'Has timetable of Wisdom High Internation Grade 9'

# Setting up
setup(
    name="aivision.pvt",
    version=VERSION,
    author="Ai Vision",
    author_email="aivision.pvt@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['tejas', 'neel', 'aivision', 'timetable', 'whis','wisdom high'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
