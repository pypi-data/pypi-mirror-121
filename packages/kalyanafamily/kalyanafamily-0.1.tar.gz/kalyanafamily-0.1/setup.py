from setuptools import setup
VERSION = '0.1'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a  add function'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="kalyanafamily", 
        version=VERSION,
        author="kalyanachakravrathy M P",
        author_email="kalyanapayani@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['kalyanafamily'],
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)