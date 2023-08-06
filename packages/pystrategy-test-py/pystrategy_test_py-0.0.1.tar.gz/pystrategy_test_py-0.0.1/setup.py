import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pystrategy_test_py',
    version="0.0.1",
    author = 'Francisco Prieto',
    description = 'Evaluation of strategies portfolios',
    url = 'https://github.com/faprieto96/pystrategy_test_py',
    packages = setuptools.find_packages(),
    classifiers= [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0'
)