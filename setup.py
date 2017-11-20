from distutils.core import setup

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'WunderWeather',
  packages = ['wunder'],
  install_requires = ['easydict','requests'],
  version = '0.2',
  description = 'Wrapper for Weather Underground API',
  long_description = long_description,
  author = 'Tyler Santos',
  author_email = '1tsantos7+wunderweather@gmail.com',
  url = 'https://github.com/T-Santos/WunderWeather',
  keywords = ['weather', 'wunderground'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.5'],
)