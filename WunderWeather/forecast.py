"""
.. module:: forecast
   :platform: Unix, Windows
   :synopsis: Module to abstract the forecast data features for wunderground

.. moduleauthor:: Tyler Santos <1tsantos at gmail.com>

"""
__docformat__ = 'reStructuredText'

# builtin P&Ms
from collections import defaultdict

# local Ms
#from weather_base import WeatherBase
from WunderWeather.weather_base import WeatherBase


class Forecast(WeatherBase):
  """Wrapper for one Forecast-y type data feature response.
  """

  def __init__(self, data, *args, **kwargs):
    super(Forecast, self).__init__(data, *args, **kwargs)
    """constructor to interface with feature response

    Args:
        data (dict): JSON response

    """
    pass

  @property
  def date(self):
    return self.extract_value(['txt_forecast', 'date'])

  @property
  def periods(self):
    """Abstract the periods for given forecast

    Notes:
      In a forecast response there are two list of dictionaries. One list is
      of text representations for each period and the other list is detailed
      data of each period. This member joins the two lists together, merging
      dictionaries of matching period keys. Each list is not always sorted in
      period increasing order and some periods may be missing from each list.

    Attributes:
      periods (`defaultdict`): of period data
      txt_periods (dict): list of dicts representing text period data
      simple_periods (dict): list of dict representing detailed period data
      list_of_periods (str): single list of period dicts for processing
      period_dict (dict): One period in a period list being processed

    Returns:
      list of Period instances

    """
    periods = defaultdict(dict)

    txt_periods = self.extract_value(['txt_forecast', 'forecastday'])
    simple_periods = self.extract_value(['simpleforecast', 'forecastday'])

    for list_of_periods in (txt_periods, simple_periods):
      if list_of_periods:
        for period_dict in list_of_periods:
          periods[period_dict['period']] = {
              **periods[period_dict['period']], **period_dict}

    if periods:
      return [Period(data=val) for prd, val in periods.items()]


class Period(WeatherBase):
    """Wrapper for one Period in a forecast
    """
    def __init__(self,data,*args,**kwargs):
      super(Period,self).__init__(data,*args,**kwargs)
      pass

    @property
    def period(self):
      return self.extract_value(['period'])

    @property
    def date_pretty(self):
      return self.extract_value(['date','pretty'])

    @property
    def text(self):
      return self.extract_value(['fcttext'])

    @property
    def text_metric(self):
      return self.extract_value(['fcttext_metric'])

    @property
    def high_temp_f(self):
      return self.extract_value(['high','fahrenheit'])
