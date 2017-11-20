"""
.. module:: test
   :platform: Unix, Windows
   :synopsis: Module to run tests for features

.. moduleauthor:: Tyler Santos <1tsantos at gmail.com>

"""
__docformat__ = 'reStructuredText'

# builtin P&Ms
import unittest
from pprint import pprint

# TODO: allow for API key to be passed in or Env Var
api_key = ''


def run_test():

    #w = weather.Extract(api_key,settings={"lang":"FR"})
    w = weather.Extract(api_key)
    # This willa actually run the connx
    #now = w.for_today_now(['MA','Boston'])
    #now = w.today_now('02481')

    # this will use cached version for testing
    #feature_key = weather.Extract.FEATURE_RESPONSE_MAP['now']
    #now = today.Now(data=today.now_response[feature_key])
    # print("TEMP:",now.temp_f)
    # print(type(now.temp_f))
    # print("Nonshort:",now.data.display_location.full)
    # pprint(now.data)

    # feature_key = weather.Extract.FEATURE_RESPONSE_MAP['date']
    # d = date.Date(data=date.date_response[feature_key])
    # print("TEMP:",d.temp_f)

    # # print all observations for the date specified
    # [print(obs.date_pretty,obs.temp_f,obs.heat_index_f) for obs in d.observations]

    # make a composite features request
    query = ['MA','Boston']
    feature_context = (
                        ('now',''),
                        ('today_historical',''),
                        ('date',"20161111"),
                        )
    [now,history,date] = w.features(query,feature_context)
    print(now)
    print(history)
    print(date)

    # this will use cached version for testing
    #feature_key = weather.Extract.FEATURE_RESPONSE_MAP['daycast']
    #feature_key = weather.Extract.FEATURE_RESPONSE_MAP['weekcast']

    # print(feature_key)
    # pprint(forecast.forecast_10_day_response)
    # print('\n\n')
    #response = forecast.daycast_response[feature_key]
    #response = forecast.forecast_10_day_response[feature_key]
    #futurecast = forecast.Forecast(data=response)
    # print("DATE:",futurecast.date)

    # for period in futurecast.periods:
    # print(period.period)
    # pprint(period.data)
    # print(period.date_pretty)
    # print(period.data.date.pretty)
    # print('\n\n')

    # Testing hurricane logic
    #hurricane = w.hurricane()
    # pprint(hurricane.data)


class TestAlerts(unittest.TestCase):

    def setUp(self):

      # feature specific vars
        feature_key = 'alerts'
        response = test_responses.alerts_response

        # setup for feature
        resp_feature_key = Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = Extract.get_feature_class(feature_key)

        # create response
        self.test_alerts = ctor({resp_feature_key: response[resp_feature_key]})

    def test_get_item_count(self):

        self.assertEqual(len(self.test_alerts.data.alerts), 1,
                         'Incorrect number of items')

    def test_get_one_item_data(self):

        self.assertEqual(self.test_alerts.data.alerts[0].description, 'Heat Advisory',
                         'Incorrect data value')


class TestTodayHistorical(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'today_historical'
        response = test_responses.historical_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_today_historical = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(self.test_today_historical.data.temp_high.normal.F, '71',
                         'data based gets are broken')

    def test_shorthand_based_get(self):

        self.assertEqual(self.test_today_historical.high_avg_temp_f, '71',
                         'shorhand gets are broken')


class TestAstronomy(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'astronomy'
        response = test_responses.astronomy_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_astronomy = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(self.test_astronomy.data.sunrise.hour, '7',
                         'data based gets are broken')


class TestTodayNow(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'now'
        response = test_responses.now_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response obj instance
        self.test_today_now = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(self.test_today_now.data.display_location.full, 'Boston, MA',
                         'data based gets are broken')

    def test_shorthand_based_get(self):

        self.assertEqual(self.test_today_now.temp_f, 47.1,
                         'shorhand gets are broken')


class TestHurricane(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'hurricane'
        response = test_responses.hurricane_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_hurricane = ctor(
            {resp_feature_key: response[resp_feature_key]})

    def test_data_based_get(self):

        self.assertEqual(self.test_hurricane.data.currenthurricane[0].stormInfo.stormName_Nice, "Hurricane Daniel",
                         'data based gets are broken')


class TestDaycast(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'daycast'
        response = test_responses.daycast_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_daycast = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(len(self.test_daycast.data.txt_forecast.forecastday), 8,
                         'data based gets are broken')

    def test_shorthand_based_get(self):
        self.assertEqual(len(self.test_daycast.periods), 8,
                         'shorhand gets are broken')

    def test_shorthand_child_based_get(self):

        period = self.test_daycast.periods[1]
        self.assertEqual(period.high_temp_f, "68",
                         'shorhand child gets are broken')


class TestWeekcast(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'weekcast'
        response = test_responses.weekcast_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_weekcast = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(len(self.test_weekcast.data.txt_forecast.forecastday), 20,
                         'data based gets are broken')

    def test_shorthand_based_get(self):
        self.assertEqual(len(self.test_weekcast.periods), 20,
                         'shorhand gets are broken')

    def test_shorthand_child_based_get(self):

        period = self.test_weekcast.periods[1]
        self.assertEqual(period.high_temp_f, "75",
                         'shorhand child gets are broken')


class TestGeolookup(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'geolookup'
        response = test_responses.geolookup_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_geolookup = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(len(self.test_geolookup.data.nearby_weather_stations), 2,
                         'data based gets are broken')


class TestDate(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'date'
        response = test_responses.date_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_date = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(len(self.test_date.data.observations), 25,
                         'data based gets are broken')

    def test_shorthand_based_get(self):
        self.assertEqual(len(self.test_date.observations), 25,
                         'shorhand gets are broken')

    def test_shorthand_child_based_get(self):

        observation = self.test_date.observations[1]
        self.assertEqual(observation.temp_f, "39.9",
                         'shorhand child gets are broken')


class TestHourlyDaycast(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'hourly_daycast'
        response = test_responses.hourly_daycast_response

        # setup for feature
        resp_feature_key = Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = Extract.get_feature_class(feature_key)

        # create response
        self.test_hourly_daycast = ctor(
            {resp_feature_key: response[resp_feature_key]})

    def test_get_item_count(self):

        self.assertEqual(len(self.test_hourly_daycast.data.hourly_forecast), 36,
                         'Incorrect number of items')

    def test_get_one_item_data(self):

        self.assertEqual(self.test_hourly_daycast.data.hourly_forecast[0].temp.english, '66',
                         'Incorrect data value')


class TestRange(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'date_range'
        response = test_responses.date_range_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_date_range = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(self.test_date_range.data.temp_high.avg.F, '71',
                         'data based gets are broken')

    def test_shorthand_based_get(self):
        self.assertEqual(self.test_date_range.high_avg_temp_f, '71',
                         'shorhand gets are broken')


class TestRawtide(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'rawtide'
        response = test_responses.rawtide_response

        # setup for feature
        resp_feature_key = Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = Extract.get_feature_class(feature_key)

        # create response
        self.test_rawtide = ctor(response[resp_feature_key])

    def test_get_item_count(self):

        self.assertEqual(len(self.test_rawtide.data.tideInfo), 1,
                         'Incorrect number of items')

    def test_get_one_item_data(self):

        self.assertEqual(self.test_rawtide.data.tideInfo[0].tideSite,
                         "Newport Beach, Newport Bay Entrance, Corona del Mar, California",
                         'Incorrect data value')


class TestTide(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'tide'
        response = test_responses.tide_response

        # setup for feature
        resp_feature_key = Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = Extract.get_feature_class(feature_key)

        # create response
        self.test_tide = ctor(response[resp_feature_key])

    def test_get_item_count(self):

        self.assertEqual(len(self.test_tide.data.tideInfo), 1,
                         'Incorrect number of items')

    def test_get_one_item_data(self):

        self.assertEqual(self.test_tide.data.tideSummary[0].data.type,
                         "Full Moon",
                         'Incorrect data value')


class TestYesterday(unittest.TestCase):

    def setUp(self):

        # feature specific vars
        feature_key = 'yesterday'
        response = test_responses.yesterday_response

        # setup for feature
        resp_feature_key = weather.Extract.FEATURE_RESPONSE_MAP[feature_key]
        ctor = weather.Extract.get_feature_class(feature_key)

        # create response
        self.test_yesterday = ctor(response[resp_feature_key])

    def test_data_based_get(self):

        self.assertEqual(len(self.test_yesterday.data.observations), 26,
                         'data based gets are broken')

    def test_shorthand_based_get(self):
        self.assertEqual(len(self.test_yesterday.observations), 26,
                         'shorhand gets are broken')

    def test_shorthand_child_based_get(self):

        observation = self.test_yesterday.observations[1]
        self.assertEqual(observation.temp_f, "59.0",
                         'shorhand child gets are broken')

def run_snippet():
    pass

def main():
    run_test()
    #run_snippet()


if __name__ == '__main__':
    # main()
    import os
    import sys
    sys.path.insert(0, os.path.abspath('../'))

    #local Ms
    import test_responses
    import weather
    from weather import *
    
    #unittest.main()
    main()
