from distutils.core import setup

# To use a consistent encoding
from codecs import open
from os import path, pardir

# Get the long description from the README file
# with open('README.rst', encoding='utf-8') as f:
#     long_description = f.read()

setup(
  name = 'WunderWeather',
  packages = ['WunderWeather'],
  install_requires = ['easydict','requests'],
  version = '0.2.6',
  description = 'Wrapper for Weather Underground API',
  #long_description = long_description,
  author = 'Tyler Santos',
  author_email = '1tsantos7+wunderweather@gmail.com',
  url = 'https://github.com/T-Santos/WunderWeather',
  keywords = ['weather', 'wunderground'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.5'],
)