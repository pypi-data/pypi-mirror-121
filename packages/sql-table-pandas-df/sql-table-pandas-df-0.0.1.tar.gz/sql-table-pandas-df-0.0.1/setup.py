from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = "convert's a sql table to a pandas dataframe"

setup(
    name="sql-table-pandas-df",
    version=VERSION,
    author="Vigneshwar",
    author_email="vigneshwar.pandiyan.s@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pymysql','pandas'],
    keywords=['sql','pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)