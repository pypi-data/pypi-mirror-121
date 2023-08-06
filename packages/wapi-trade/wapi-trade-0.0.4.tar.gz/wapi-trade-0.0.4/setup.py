from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'wapi is an open source library that acts as a Wealthsimple Trade API wrapper for python.'

# Setting up
setup(
    name="wapi-trade",
    version=VERSION,
    author="Andre Ceschia",
    author_email="andre.ceschia04@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['cloudscraper', 'bs4'],
    keywords=['python', 'finance', 'wealthsimple', 'wealthsimple trade', 'broker api'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)