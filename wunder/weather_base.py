"""
.. module:: weather_base
   :platform: Unix, Windows
   :synopsis: Module to abstract the data feature responses for wunderground

.. moduleauthor:: Tyler Santos <1tsantos at gmail.com>

"""
__docformat__ = 'reStructuredText'

# builtin P&Ms
from functools import reduce
from operator import getitem

# 3rd party P&Ms
from easydict import EasyDict


class WeatherBase():
    """Wrapper for one all data feature responses.

      Attributes:
          data (`EasyDict`): dictionary that allows for 'dotted' key references
          __data (dict): python dict, JSON representation of portion of response of interest
          NAN (list): list of values that are considered to be no data N/A type values
    """
    NAN = [-999, -9999]

    def __init__(self, data):
        """constructor to set up extract defaults for wunderground connection

        Args:
            data (dict): Interesting portion of wunderground's response

        Attributes:
            data (`EasyDict`): dictionary that allows for 'dotted' key references
            __data (dict): python dict, JSON representation of portion of response of interest

        """
        self.data = EasyDict(data)
        self.__data = data

    def extract_value(self, keys):
        """constructor to interface with feature response

        Args:
            keys (list): list of keys to drill down into nested dictionaries

        Returns:
            value of interest or None

        """

        if self.__data:
            try:
                return reduce(getitem, keys, self.__data)
            except KeyError:
                pass
            else:
                return None
