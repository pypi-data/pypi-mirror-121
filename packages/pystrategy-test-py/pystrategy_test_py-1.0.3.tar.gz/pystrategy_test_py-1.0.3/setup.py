import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pystrategy_test_py',
    version="1.0.3",
    author = 'Francisco A. Prieto Rodriguez, Francisco de Asís Fernández Navarro, David Becerra Alonso',
    description = long_description,
    long_description_content_type= 'text/markdown',
    url = 'https://github.com/faprieto96/pystrategy_test_py',
    packages = setuptools.find_packages(),
    classifiers= [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)
