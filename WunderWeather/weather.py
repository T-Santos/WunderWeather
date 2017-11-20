"""
.. module:: weather
   :platform: Unix, Windows
   :synopsis: The classes and modules provided have several functions to aid in abstracting the nuances with the
                wunderground responses. The purpose is to expose the results in a uniform format while providing
                shortcuts, normalizing access, and making more pythonic references to wunderground's data.
.. moduleauthor:: Tyler Santos <1tsantos at gmail.com>

"""
__docformat__ = 'reStructuredText'

# 3rd party P&Ms
import requests

# local Ms
import WunderWeather
from WunderWeather import today, date, forecast, weather_base


class Extract():
    """Encapsulate logic for extracting weather data

    This is the main point of entry to extract data from the weather underground service
    utilizing their public API.
    
    Notes:
        `Wunderground Doc <https://www.wunderground.com/weather/api/d/docs>`_
        
        URL Request Format:
            `http://api.wunderground.com/api/<API_KEY>/features/settings/q/query.format`
    
    Attributes:
        BASE_URL (str): Base string used for URL generation
        FEATURE_URL (str): string template to generate URL for a feature request
        HURRICANE_URL (str): string template to generate URL for a hurricane feature request
        FEATURE_URL_MAP (dict): Mapping of module's feature key to wunderground's key in the URL
        FEATURE_RESPONSE_MAP (dict): Mapping of module's feature key to wunderground's key in the response
        FEATURE_CLASS_MAP (dict): Mapping of module's feature key to the object definition to generate an instance
    """
    BASE_URL = 'http://api.wunderground.com/api'
    FEATURE_URL = BASE_URL + '/{key}/{features}/{settings}/q/{query}.{format}'
    HURRICANE_URL = BASE_URL + '/{key}/{feature}/{settings}/view.{format}'

    FEATURE_URL_MAP = {
                        'alerts': 'alerts',
                        'astronomy': 'astronomy',
                        'cams': 'webcams',
                        'date': 'history_',
                        'date_range': 'planner_',
                        'daycast': 'forecast',
                        'geolookup': 'geolookup',
                        'hourly_daycast': 'hourly',
                        'hourly_weekcast': 'hourly10day',
                        'hurricane': 'currenthurricane',
                        'now': 'conditions',
                        'rawtide': 'rawtide',
                        'satelite': 'satelite',
                        'tide': 'tide',
                        'today_historical': 'almanac',
                        'weekcast': 'forecast10day',
                        'yesterday': 'yesterday',
                        }

    FEATURE_RESPONSE_MAP = {
                            'alerts': 'alerts',
                            'astronomy': 'moon_phase',
                            'cams': 'webcams',
                            'date': 'history',
                            'date_range': 'trip',
                            'daycast': 'forecast',
                            'geolookup': 'location',
                            'hourly_daycast': 'hourly_forecast',
                            'hourly_weekcast': 'hourly_forecast',
                            'hurricane': 'currenthurricane',
                            'now': 'current_observation',
                            'rawtide': 'rawtide',
                            'satelite': 'satelite',
                            'tide': 'tide',
                            'today_historical': 'almanac',
                            'weekcast': 'forecast',
                            'yesterday': 'history',
                            }

    FEATURE_CLASS_MAP = {
                            'alerts': 'weather_base.WeatherBase',
                            'astronomy': 'weather_base.WeatherBase',
                            'cams': 'weather_base.WeatherBase',
                            'date': 'date.Date',
                            'date_range': 'date.Range',
                            'daycast': 'forecast.Forecast',
                            'geolookup': 'weather_base.WeatherBase',
                            'hourly_daycast': 'weather_base.WeatherBase',
                            'hourly_weekcast': 'weather_base.WeatherBase',
                            'hurricane': 'weather_base.WeatherBase',
                            'now': 'today.Now',
                            'rawtide': 'weather_base.WeatherBase',
                            'satelite': 'weather_base.WeatherBase',
                            'tide': 'weather_base.WeatherBase',
                            'today_historical': 'today.Historical',
                            'weekcast': 'forecast.Forecast',
                            'yesterday': 'date.Date',
                            }

    @classmethod
    def get_feature_class(cls, feature_key):
        """Get the class definition for a particular feature

        Args:
            feature_key (str): internal key for feature

        Returns:
            Class definition for feature

        """
        pkg = 'WunderWeather'
        klass = cls.FEATURE_CLASS_MAP[feature_key]
        [mod,kls] = klass.split('.')
        mod = __import__(pkg+'.'+mod, fromlist=[kls])
        return getattr(mod, kls)

    def __init__(self, api_key, settings=None):
        """constructor to set up extract defaults for wunderground connection

        Args:
            api_key (str): Wunderground supplied API Key.
            settings (dict, optional): Settings for URL as defined.
                https://www.wunderground.com/weather/api/d/docs?d=data/index
                Defaults to lang:EN

        Attributes:
            api_key (str): Wunderground supplied API Key.
            format (str): Response format. currently only JSON is supported
            settings (dict): Settings for URL as defined.
                https://www.wunderground.com/weather/api/d/docs?d=data/index
                Defaults to {lang:EN}

        """
        self.api_key = api_key
        self.settings = settings if settings else {'lang': 'EN'}

        self.format = 'json'

    def hurricane(self):
        """Interface with the current hurricane data feature

        Attributes:
            feature_key (str): Module feature key
            context (dict): Used to populate feature URL template
            response (dict): JSON representation of the response
            response_feature_key (str): Module feature key's key for response parsing
            ctor (`weather.WeatherBase`): Reference to class to potentially generate an instance

        Returns:
            weather.weather_base instance or None

        """
        feature_key = 'hurricane'
        context = {
                    'key': self.api_key,
                    'feature': type(self).FEATURE_URL_MAP[feature_key],
                    'format': self.format,
                    'settings': '/'.join(['{0}:{1}'.format(skey, svalue) for skey, svalue in self.settings.items()]),
                    }
        response = self._make_feature_request(type(self).HURRICANE_URL, context)

        response_feature_key = type(self).FEATURE_RESPONSE_MAP[feature_key]

        if response_feature_key in response:
            ctor = type(self).get_feature_class(feature_key)
            return ctor({response_feature_key: response[response_feature_key]})

    def today_now(self, query):
        """Shorthand to interface with the conditions data feature

        Args:
            query (str or list): string or list of strings for query portion of URL generation

        Attributes:
            feature_context (tuple): tuple of tuples to give feature of interest
                and necessary data for that feature

        Returns:
            today.Now instance or None

        """
        feature_context = (('now', ''),)
        return self.features(query, feature_context)[0]

    def today_historical(self, query):
        """Shorthand to interface with the almanac data feature

        Args:
            query (str or list): string or list of strings for query portion of URL generation

        Attributes:
            feature_context (tuple): tuple of tuples to give feature of interest
                and necessary data for that feature

        Returns:
            today.Now instance or None

        """
        feature_context = (('today_historical', ''),)
        return self.features(query, feature_context)[0]

    def daycast(self, query):
        """Shorthand to interface with the forcast data feature

        Args:
            query (str or list): string or list of strings for query portion of URL generation

        Attributes:
            feature_context (tuple): tuple of tuples to give feature of interest
                and necessary data for that feature

        Returns:
            today.Now instance or None

        """
        feature_context = (('daycast', ''),)
        return self.features(query, feature_context)[0]

    def weekcast(self, query):
        """Shorthand to interface with the forcast10day data feature

        Args:
            query (str or list): string or list of strings for query portion of URL generation

        Attributes:
            feature_context (tuple): tuple of tuples to give feature of interest
                and necessary data for that feature

        Returns:
            today.Now instance or None

        """
        feature_context = (('weekcast', ''),)
        return self.features(query, feature_context)[0]

    def date(self, query, date):
        """Shorthand to interface with the history data feature

        Args:
            query (str or list): string or list of strings for query portion of URL generation
            date (str): Date in the form YYYYMMDD.

        Attributes:
            feature_context (tuple): tuple of tuples to give feature of interest
                and necessary data for that feature

        Returns:
            today.Now instance or None

        """
        feature_context = (('date', date),)
        return self.for_features(query, feature_context)[0]

    def date_range(self, query, date_range):
        """Shorthand to interface with the planner data feature

        Args:
            query (str or list): string or list of strings for query portion of URL generation
            date_range (str): Date range (30 day max) in the form MMDDMMDD.

        Attributes:
            feature_context (tuple): tuple of tuples to give feature of interest
            and necessary data for that feature

        Returns:
            today.Now instance or None

        """
        feature_context = (('date_range', date_range),)
        return self.features(query, feature_context)[0]

    def features(self, query, feature_context):
        """Central logic for making data feature requests

        Args:
            query (str or list): string or list of strings for query portion of URL generation
            feature_context (tuple): tuple of tuples to supply feature of interest
                and necessary data for that feature

        Attributes:
            query (list): Strings for URL generation
            feature_codes (str):  Final format for URL feature keys (with data appended)
            context (dict): final formatted data for URL template
            response (dict): JSON response
            ctor (obj): Object Class Reference to generate an instance.
                Could be one of

                * :mod:`weather_base.WeatherBase`
                * :mod:`today.Now`
                * :mod:`today.Historical`
                * :mod:`forcast.Daycast`
                * :mod:`forcast.Weekcast`
                * :mod:`date.Date`
                * :mod:`date.Range`

            weather_features (list): Instances to be retuned. Offset could be None
                if there was no response for the supplied data feature.
            feature_key (str): Module's feature key
            response_feature_key (str): Module's feature key for URL response

        Returns:
            List of weather_features. Offsets returned in the order they are supplied
            in the feature_context arg. Offset could be none if no response

        """
        if not type(query) == list:
            query = [query]

        feature_codes = [type(self).FEATURE_URL_MAP[f_key] + f_val for f_key,f_val in feature_context]

        context = {
                    'key': self.api_key,
                    'features': '/'.join(feature_codes),
                    'query': '/'.join(query),
                    'format': self.format,
                    'settings': '/'.join(['{0}:{1}'.format(s_key,s_val) for s_key,s_val in self.settings.items()]),
                    }
        response = self._make_feature_request(type(self).FEATURE_URL,context)

        weather_features = []
        for feature_key, _ in feature_context:
            
            ctor = type(self).get_feature_class(feature_key)

            response_feature_key = type(self).FEATURE_RESPONSE_MAP[feature_key]

            if response_feature_key in response:

                # if we get a list back as the high level item
                # keep the feature key in there as a single key dict
                if response[response_feature_key] is list:
                    weather_features.append(
                        ctor({response_feature_key: response[response_feature_key]}))
                else:
                    weather_features.append(
                        ctor(response[response_feature_key]))
            else:
                weather_features.append(None)

        return weather_features


    def _make_feature_request(self,url_template,data):
        """Private member to make a request 

        Args:
            url_template (str): Template used for URL generation
            data (dict): Data used to populate URL template

        Returns:
            JSONified response in dictionary format

        """
        return requests.get(url_template.format(**data)).json()
