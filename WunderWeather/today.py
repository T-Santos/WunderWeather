"""
.. module:: today
   :platform: Unix, Windows
   :synopsis: Module to abstract the today based data features for wunderground

.. moduleauthor:: Tyler Santos <1tsantos at gmail.com>

"""
__docformat__ = 'reStructuredText'

# local Ms
#from weather_base import WeatherBase
from WunderWeather.weather_base import WeatherBase


class Now(WeatherBase):
    """Wrapper for one (today) conditions type data feature response.
    """

    def __init__(self, data, *args, **kwargs):
        super(Now, self).__init__(data, *args, **kwargs)
    """constructor to interface with feature response

    Args:
        data (dict): JSON response

    """
    pass

    @property
    def temp_f(self):
        return self.extract_value(['temp_f'])

    @property
    def temp_c(self):
        return self.extract_value(['temp_c'])

    @property
    def temp_pretty(self):
        return self.extract_value(['temperature_string'])

    @property
    def weather(self):
        return self.extract_value(['weather'])

class Historical(WeatherBase):
    """Wrapper for one (today) almanac type data feature response.
    """

    def __init__(self,data,*args,**kwargs):
        super(Historical,self).__init__(data,*args,**kwargs)
        """constructor to interface with feature response

        Args:
            data (dict): JSON response

        """
        pass

    @property
    def high_avg_temp_f(self):
        return self.extract_value(['temp_high','normal','F'])

    @property
    def high_avg_temp_c(self):
        return self.extract_value(['temp_high','normal','C'])

    @property
    def low_avg_temp_f(self):
        return self.extract_value(['temp_low','normal','F'])

    @property
    def low_avg_temp_c(self):
        return self.extract_value(['temp_low','normal','C'])
