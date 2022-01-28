#!/usr/bin/env python

"""Setup script."""

from setuptools import setup, find_packages

requirements = ["pyopenms",
                "flask",
                "requests",
                "click",
                "werkzeug",
                "pandas",
                "numpy"
                ]


test_requirements = ['pytest>=3', ]

setup(
    author="Group03",
    author_email='rohitha0112@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Group03 Protein Identification Mass Spectra Package",
    entry_points={
        'console_scripts': [
            'protein_spectra_package=protein_spectra_package.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='protein_spectra_package',
    name='protein_spectra_package',
    packages=find_packages(include=['protein_spectra_package', 'protein_spectra_package.*']),
    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.0',
    zip_safe=False,
)

