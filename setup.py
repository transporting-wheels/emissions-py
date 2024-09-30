from setuptools import setup, find_packages

setup(
    name='emissions_py',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    description='CO2e calculator for automotive road transport',
    author='TransportingWheels',
    author_email='dev@transportingwheels.com',
    url='https://github.com/transporting-wheels/emissions-calculator.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
