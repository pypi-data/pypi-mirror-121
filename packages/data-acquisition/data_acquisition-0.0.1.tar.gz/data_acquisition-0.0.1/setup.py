from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Stock Data Acquisition'
LONG_DESCRIPTION = 'A python package in order to acquire raw OHLC data for a \
                    specific ticker as well as calculate technical indicators.'

# Setting up
setup(
        name="data_acquisition", 
        version=VERSION,
        author="Scott Hirsch",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['ta', 'requests', 'pandas'],
        
        keywords=['python', 'stock', 'finance', 'technical analysis'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
