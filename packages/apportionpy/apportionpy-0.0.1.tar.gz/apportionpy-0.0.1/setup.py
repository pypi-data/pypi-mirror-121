from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A Python package for apportionment."
LONG_DESCRIPTION = "A package that allows users to apportion seats to states based on population figures. Initial " \
                   "fair shares, final fair shares, initial quotas, final quotas, initial divisors, and modified " \
                   "divisors are calculated."

# Setting up
setup(
    name="apportionpy",
    version=VERSION,
    author="Brandon Rorie",
    author_email="ticer1999@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "apportionment", "apportion", "hamilton", "webster", "adam", "jefferson", "method"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)
