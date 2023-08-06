# gaus-bin-dist

This package contains modules for working with Gaussian and Binomial Distributions.

## Files

* `gaus_bin_dist/`: Distributions Package
  * `__init__.py`: Initialization script
  * `Binomialdistribution.py`: Binomial class
  * `Gaussiandistribution.py`: Gaussian class
  * `Generaldistribution.py`: Distribution class
* `license.txt`: MIT license
* `setup.cfg`: Configuration file for code packaging
* `setup.py`: Script for code packaging

## Installation

Download on [PyPi](https://pypi.org/project/gaus-bin-dist/) or use following command:

`pip install gaus-bin-dist`

## Python Interpreter Example

```python
>>> from gaus_bin_dist import Gaussian, Binomial
>>> Gaussian(10, 7)
mean 10, standard deviation 7
>>> Binomial(0.4, 25)
mean 10.0, standard deviation 2.449489742783178, p 0.4, n 25
```
