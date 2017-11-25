import io
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
  name = 'WunderWeather',
  packages = ['WunderWeather'],
  # To include everything defined in MANIFEST.in file
  include_package_data=True,
  # to include addl files
  package_data={
    '':['*.rst','*.txt'],
    },
  install_requires = ['easydict','requests'],
  version = '0.2.8',
  description = 'Wrapper for Weather Underground API',
  long_description = long_description,
  author = 'Tyler Santos',
  author_email = '1tsantos7+wunderweather@gmail.com',
  url = 'http://wunderweather.readthedocs.io/en/latest/',
  download_url = 'https://github.com/T-Santos/WunderWeather',
  keywords = ['weather', 'wunderground'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.5'],
    )