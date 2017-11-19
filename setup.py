from distutils.core import setup

setup(
  name = 'wunder',
  packages = ['wunder'],
  install_requires = ['easydict','requests'],
  version = '0.1',
  description = 'Wrapper for Weather Underground API',
  author = 'Tyler Santos',
  author_email = '1tsantos7+wunderweather@gmail.com',
  url = '', # use the URL to the github repo
  keywords = ['weather', 'wunderground'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.5'],
)