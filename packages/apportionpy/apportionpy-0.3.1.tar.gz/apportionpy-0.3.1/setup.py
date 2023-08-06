from setuptools import setup, find_packages

VERSION = "0.3.1"
DESCRIPTION = "A Python package for apportionment."
LONG_DESCRIPTION = "A package that allows users to apportion seats to states based on population figures.\n\n" \
                   "This apportionment package calculates results for the following methods:\n" \
                   " - Hamilton's method\n" \
                   " - Jefferson's method\n" \
                   " - Adam's method\n" \
                   " - Webster's method\n" \
                   " - Huntington Hill's method\n" \
                   " - Method of equal proportions\n\n" \
                   "Hamilton's method calculations:\n" \
                   " - fair shares\n" \
                   " - initial fair shares\n" \
                   " - initial quotas\n" \
                   " - final quotas\n" \
                   " - initial divisor\n" \
                   " - modified divisor\n\n" \
                   "Jefferson's method calculations:\n" \
                   " - fair shares\n" \
                   " - initial fair shares\n" \
                   " - initial quotas\n" \
                   " - final quotas\n" \
                   " - initial divisor\n" \
                   " - modified divisor\n" \
                   " - divisor history\n\n" \
                   "Adam's method calculations:\n" \
                   " - fair shares\n" \
                   " - initial fair shares\n" \
                   " - initial quotas\n" \
                   " - final quotas\n" \
                   " - initial divisor\n" \
                   " - modified divisor\n" \
                   " - divisor history\n\n" \
                   "Webster's method calculations:\n" \
                   " - fair shares\n" \
                   " - initial fair shares\n" \
                   " - initial quotas\n" \
                   " - final quotas\n" \
                   " - initial divisor\n" \
                   " - modified divisor\n" \
                   " - divisor history\n\n" \
                   "Huntington Hill's method calculations:\n" \
                   " - fair shares\n" \
                   " - initial fair shares\n" \
                   " - initial quotas\n" \
                   " - final quotas\n" \
                   " - initial geometric means\n" \
                   " - final geometric means\n" \
                   " - initial divisor\n" \
                   " - modified divisor\n\n" \
                   "Method of equal proportions calculations:\n" \
                   " - fair shares\n\n" \
                   "Experimental features:\n" \
                   " - estimate the lowest possible divisor possible\n" \
                   " - estimate the highest possible divisor possible\n" \

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
    keywords=["python", "apportionment", "apportion", "hamilton", "webster", "adam", "jefferson", "Huntington",
              "method", "equal", "proportions"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)
