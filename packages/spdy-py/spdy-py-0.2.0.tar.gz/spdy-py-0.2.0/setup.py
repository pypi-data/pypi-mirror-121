# Copyright (C) 2021 Mathew Odden
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_desc = fh.read()

setup(
    name="spdy-py",
    version="0.2.0",
    author="Mathew Odden",
    author_email="mrodden@us.ibm.com",
    url="https://github.com/mrodden/spdy-py",
    description="A pure Python implementation of the SDPY/3.x protocol",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="LGPL",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"spdy": ["py.typed", "*.pyi"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: "
        "GNU Library or Lesser General Public License (LGPL)",
    ],
    python_requires=">=3.6",
)
