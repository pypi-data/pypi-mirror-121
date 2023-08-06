from setuptools import setup, find_packages
# import pathlib

# here = pathlib.Path(__file__).parent.resolve()

# long_description = (here / 'README.md').read_text(encoding='utf-8')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# install_reqs = (here / 'requirements.txt').read_text(encoding='utf-8').splitlines()

# reqs = install_reqs

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

# setup(
#
#     name='pyrpa',  # Required
#     version='0.0.1',  # Required
#     zip_safe=False,
#     # This is a one-line description or tagline of what your project does. This
#     # corresponds to the "Summary" metadata field:
#     # https://packaging.python.org/specifications/core-metadata/#summary
#     description='some useful functions in work for SRE',  # Optional
#
#     long_description=long_description,  # Optional
#     long_description_content_type='text/markdown',  # Optional (see note above)
#
#     url='https://github.com/otfsenter/pyrpa',  # Optional
#     author='otfsenter',  # Optional
#     author_email='newellzhou@163.com',  # Optional
#
#     # Classifiers help users find your project by categorizing it.
#     #
#     # For a list of valid classifiers, see https://pypi.org/classifiers/
#     # valid below:
#     # https://test.pypi.org/pypi?%3Aaction=list_classifiers
#     classifiers=[  # Optional
#         # How mature is this project? Common values are
#         #   3 - Alpha
#         #   4 - Beta
#         #   5 - Production/Stable
#         'Development Status :: 1 - Planning',
#
#         # Indicate who your project is intended for
#         'Intended Audience :: Developers',
#         'Topic :: Software Development :: Libraries :: Python Modules',
#
#         # Pick your license as you wish
#         'License :: OSI Approved :: Apache Software License',
#
#         # Specify the Python versions you support here. In particular, ensure
#         # that you indicate you support Python 3. These classifiers are *not*
#         # checked by 'pip install'. See instead 'python_requires' below.
#         'Programming Language :: Python :: 3.8',
#     ],
#
#     keywords='rpa, automation, robot, scripts, operation',  # Optional
#
#     package_dir={'': 'pyrpa'},  # Optional
#
#     packages=find_packages(where='pyrpa'),  # Required
#
#     python_requires='>=3, <4',
#
#     # This field lists other packages that your project depends on to run.
#     # Any package you put here will be installed by pip when your project is
#     # installed, so they must be valid existing projects.
#     #
#     # For an analysis of "install_requires" vs pip's requirements files see:
#     # https://packaging.python.org/en/latest/requirements.html
#     # install_requires=['peppercorn'],  # Optional
#     # install_requires=reqs,  # Optional
#
#     # List additional groups of dependencies here (e.g. development
#     # dependencies). Users will be able to install these using the "extras"
#     # syntax, for example:
#     #
#     #   $ pip install sampleproject[dev]
#     #
#     # Similar to `install_requires` above, these must be valid existing
#     # projects.
#     # extras_require={  # Optional
#     #     'dev': ['check-manifest'],
#     #     'test': ['coverage'],
#     # },
#
#     # If there are data files included in your packages that need to be
#     # installed, specify them here.
#     # package_data={  # Optional
#     #     'sample': ['package_data.dat'],
#     # },
#
#     # Although 'package_data' is the preferred approach, in some case you may
#     # need to place data files outside of your packages. See:
#     # http://docs.python.org/distutils/setupscript.html#installing-additional-files
#     #
#     # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
#     # data_files=[('my_data', ['data/data_file'])],  # Optional
#
#     # # To provide executable scripts, use entry points in preference to the
#     # # "scripts" keyword. Entry points provide cross-platform support and allow
#     # # `pip` to create the appropriate form of executable for the target
#     # # platform.
#     # #
#     # # For example, the following would provide a command called `sample` which
#     # # executes the function `main` from this package when invoked:
#     # entry_points={  # Optional
#     #     'console_scripts': [
#     #         'sample=sample:main',
#     #     ],
#     # },
#
#     project_urls={  # Optional
#         'Bug Reports': 'https://github.com/otfsenter/pyrpa/issues',
#         # 'Funding': 'https://donate.pypi.org',
#         # 'Say Thanks!': 'http://saythanks.io/to/example',
#         'Source': 'https://github.com/otfsenter/pyrpa',
#     },
# )


setup(
    name="pyrpa",
    version="0.0.5",
    author="otfsenter",
    author_email="newellzhou@163.com",
    description="some useful functions in work for SRE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otfsenter/pyrpa",
    project_urls={
        "Bug Tracker": "https://github.com/otfsenter/pyrpa/issues",
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)