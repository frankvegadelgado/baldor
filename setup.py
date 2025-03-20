from pathlib import Path

import setuptools

VERSION = "0.1.1"

NAME = "baldor"

INSTALL_REQUIRES = [
    "numpy>=2.2.1",
    "scipy>=1.15.0",
    "networkx[default]>=3.4.2",
    "ortools>=9.12.4544"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Solve the Minimum Dominating Set for undirected graph encoded in DIMACS format.",
    url="https://github.com/frankvegadelgado/baldor",
    project_urls={
        "Source Code": "https://github.com/frankvegadelgado/baldor",
        "Documentation Research": "https://dev.to/frank_vega_987689489099bf/polynomial-time-algorithm-for-mds-p-np-1ln6",
    },
    author="Frank Vega",
    author_email="vega.frank@gmail.com",
    license="MIT License",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
    python_requires=">=3.10",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["baldor"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'solve = baldor.app:main',
            'test_solve = baldor.test:main',
            'batch_solve = baldor.batch:main'
        ]
    }
)