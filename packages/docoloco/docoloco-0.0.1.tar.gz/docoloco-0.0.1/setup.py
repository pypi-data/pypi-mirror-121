from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Makes Templates'
LONG_DESCRIPTION = 'Makes templates and stores data collected'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="docoloco", 
        version=VERSION,
        author="Armorlol",
        author_email="cluckluckboi@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)