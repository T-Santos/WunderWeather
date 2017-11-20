"""
.. module:: date
   :platform: Unix, Windows
   :synopsis: Module to abstract the date based data features for wunderground

.. moduleauthor:: Tyler Santos <1tsantos at gmail.com>

"""
__docformat__ = 'reStructuredText'

# local Ms
#from weather_base import WeatherBase
from WunderWeather.weather_base import WeatherBase


class Date(WeatherBase):
    """
    Wrapper for one (date) history type data feature response.
    """

    def __init__(self, data, *args, **kwargs):
        super(Date, self).__init__(data, *args, **kwargs)
        """constructor to interface with feature response

        Args:
            data (dict): JSON response

        """
        pass

    @property
    def temp_f(self):
        return self.extract_value(['dailysummary', 0, 'meantempi'])

    @property
    def temp_c(self):
        return self.extract_value(['dailysummary', 0, 'meantempm'])

    @property
    def observations(self):
        """Abstract the observations for given date

        Notes:
            In a date based response (History,Yesterday) there is a list of observations.

        Attributes:
            observations (list): List of dictionaries for each observation for the date

        Returns:
            list of Observation instances

        """
        observations = self.extract_value(['observations'])
        if observations:
            return [Observation(data=obs) for obs in observations]


class Observation(WeatherBase):
    """
    Wrapper for one date based data feature's observations
    """

    def __init__(self, data, *args, **kwargs):
        super(Observation, self).__init__(data, *args, **kwargs)
        """constructor to interface with feature response for one observation

        Args:
            data (dict): JSON response

        """
        pass

    @property
    def temp_f(self):
        return self.extract_value(['tempi'])

    @property
    def temp_c(self):
        return self.extract_value(['tempm'])

    @property
    def date_pretty(self):
        return self.extract_value(['date', 'pretty'])


class Range(WeatherBase):
    """
    Wrapper for one (date) history type data feature response.
    """

    def __init__(self, data, *args, **kwargs):
        super(Range, self).__init__(data, *args, **kwargs)
        """constructor to interface with feature response

        Args:
            data (dict): JSON response

        """
        pass

    @property
    def high_avg_temp_f(self):
        return self.extract_value(['temp_high', 'avg', 'F'])

    @property
    def high_avg_temp_c(self):
        return self.extract_value(['temp_high', 'avg', 'C'])

    @property
    def low_avg_temp_f(self):
        return self.extract_value(['temp_low', 'avg', 'F'])

    @property
    def low_avg_temp_c(self):
        return self.extract_value(['temp_low', 'avg', 'C'])
