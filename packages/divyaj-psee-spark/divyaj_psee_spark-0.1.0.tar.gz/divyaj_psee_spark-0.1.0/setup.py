import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()  

setuptools.setup(
    name="divyaj_psee_spark",                     # This is the name of the package
    version="0.1.0",                        # The initial release version
    author="Divyaj Balivada",                     # Full name of the author
    author_email = "b.divyajbalivada@gmail.com",
    description="Package for connecting HDFS and JHUB",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3',                # Minimum version requirement of the package
    install_requires=[]                     # Install other dependencies if any
)