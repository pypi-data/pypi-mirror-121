from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pentageoserver",                     # This is the name of the package
    version="1.1.5",                        # The initial release version
    author="ahmed mounir",                     # Full name of the author
    description="Geoserver Automation Helper",
    # Long description read from the the readme file
    long_description=long_description,
    long_description_content_type="text/markdown",
    # List of all python modules to be installed
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["pentageoserver"],             # Name of the python package
    # Directory of the source code of the package
    package_dir={'': '.'},
    # Install other dependencies if any
    install_requires=[""]
)
