from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, "src", "pynata", "__version__.py"), encoding="utf8") as fh:
    exec(fh.read(), about)

with open(path.join(here, "README.md"), "r", "utf-8") as f:
    readme = f.read()

setup(
    name="pynata",
    version=about["__version__"],
    url="https://github.com/unparalleled-js/py-pinata",
    project_urls={
        "Issue Tracker": "https://github.com/unparalleled-js/py-pinata/issues",
        "Documentation": "https://github.com/unparalleled-js/py-pinata",
        "Source Code": "https://github.com/unparalleled-js/py-pinata",
    },
    description="A wrapper around the Pinata REST APIs",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7, <4",
    install_requires=[
        "click>=8.0.3,<9.0",
        "keyring>=21.8.0,<22.0",
        "nft-utils==0.1.0",
        "requests>=2.4.2",
    ],
    extras_require={
        "dev": [
            "flake8==3.9.2",
            "pytest==6.2.4",
            "pytest-cov==2.12.1",
            "pytest-mock==3.6.1",
            "tox==3.24.0",
        ]
    },
    entry_points={"console_scripts": ["pynata=pynata.cli:cli"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
