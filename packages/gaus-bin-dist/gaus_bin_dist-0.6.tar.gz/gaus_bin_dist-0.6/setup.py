from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='gaus_bin_dist',
      version='0.6',
      description='Gaussian and Binomial Distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['gaus_bin_dist'],
      author='Eric Kwok',
      author_email='ekwok25@gmail.com',
      zip_safe=False)
