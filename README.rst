.. This package and all of its contents are supplied "as-is" and follow
	the GNU General Public License
	https://www.gnu.org/licenses/gpl.txt

Welcome to WunderWeather!
=========================================

Whether you're already a user and want a refresher on the documentation or you're evaluating the package for the first time, you've come to the right place. So what do you want to learn more about?


.. contents::
	:local:

Introduction
************

WunderWeather attempts to expose data supplied by `Weather Underground <https://www.wunderground.com/?apiref=0627061efb72054c>`_ in a way that is easy to use and easy to get weather data into your application quickly without having to deal with all of the details. 

About the Wunderground API
##########################

The Wunderground API supplies different endpoints called `data features <https://www.wunderground.com/weather/api/d/docs?d=data/index?apiref=0627061efb72054c>`_ which, when supplied the proper arguments, return numerous data points describing the feature being queried. 

`Documentation <https://www.wunderground.com/weather/api/d/docs?apiref=0627061efb72054c>`_

About the WunderWeather API
###########################

WunderWeather was built to expose the data supplied by Wunderground in a uniform fashion. For certain data features where it applied, wrapper classes were created to normalize the data returned and supply ease of access to that data. 

When developing WunderWeather there were a few key concepts kept in mind which are listed below. If you intend on contributing, please keep these ideas in mind.
	#. Out of the hundreds of data points that Wunderground so graciously supplies, expose shortcuts to the more frequently used/popular data points such as temperature and date through the data feature specific wrappers.
		#. For the history data feature, Wunderground exposes the average temperature data point using 3 keys rather than the one abstracted in WunderWeather
		
		**Wunderground:** 

		>>> response["history"]["daily_summary"]["meantempi"]
		
		**WunderWeather:**

		>>> response.temp_f

	#. Normalize the data point names being exposed.
		#. The Wunderground API does a great job at supplying endless amounts of weather data but unfortunately similar data points across different features have different names. A case where this crops up frequently is for imperial (i) and metric (m) and their respective Fahrenheit (f) and Celsius (c) identifiers for temperature. 
		
		**Example Data Points:**
		 
		* temp_i vs temp_f
		* temp_m vs temp_c 

Code Examples
#############

The following code snippets are examples of extracting data from data feature responses. Some examples build off of previous examples (as to avoid repetition) but should be properly documented as ``continuation from NNN example``.

.. warning::
	The WunderWeather only Python 3 compatible. 

.. note::
	Because the `requests package <http://docs.python-requests.org/en/master/>`_ is awesome, we're going to be using that to make our requests in the following examples. We use it to make requests in our package and so should you!

**Not using Requests**

*Example listed in Wunderground documentation*

.. code:: python

	import urllib2
	import json
	f = urllib2.urlopen('http://api.wunderground.com/api/<YOUR_API_KEY>/geolookup/conditions/q/IA/Cedar_Rapids.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
	print "Current temperature in %s is: %s" % (location, temp_f)
	f.close()

`example <https://www.wunderground.com/weather/api/d/docs?d=resources/code-samples#python&apiref=0627061efb72054c>`_

**Using Requests**

*Example listed in Wunderground doc converted to use requests*

.. code:: python

	import requests # learn more: https://python.org/pypi/requests
	response = requests.get('http://api.wunderground.com/api/<YOUR_API_KEY>/geolookup/conditions/q/MA/Boston.json').json()
	location = response['location']['city']
	temp_f = response['current_observation']['temp_f']
	print("Current Temperature in %s is: %s" %(location,temp_f))

**Using WunderWeather**

*Example listed in Wunderground doc converted to use WunderWeather*

.. code:: python

	from wunder import weather
	extractor = weather.Extract(api_key)
	[location,current] = extractor.features("MA/Boston",(('geolookup',''),('now','')))
	print("Current Temperature in %s is: %s" %(location.data.city,current.temp_f))

*In the example above, notice how data points can be extracted from a feature using dotted notation whether there is a feature specific wrapper class or not to provide a uniform look in the calling application. When referencing shortcuts from wrapper classes or directly accessing the data, the look is the same. As of writing this documentation Geolookup does not have a wrapper so all data extracted from that feature must use the* ``WeatherBase.data`` *member to use the dotted notation.*

Contributors
************

Thanks for checking out this section and showing interest in making this package better. The following are points of interest that could use polishing or expanding. As always, if you see data points across data features that could use a level of abstraction just add a wrapper class if not already defined and add a property member to that class to provide a shortcut or normalized external name across features. 

TODOs
#######

#. Several Data Features only exist using the generic WeatherBase, base class and thus their data is accessed using the data member. There are likely reasons to create wrappers for these features. current hurricane seemed to need a wrapper the most. But some others that might benefit from abstraction are listed below.
	#. currenthurricane
	#. rawtide and tide
	#. hourly\* based features
#. And of course, help with documentation, documentation, and more documentation.


Mentions
********

I just want give mention and thanks to the following:

#. `Weather Underground <https://www.wunderground.com/?apiref=0627061efb72054c>`_ for supplying the data.
#. `requests <http://docs.python-requests.org/en/master/>`_ for making http for me.
	
	* `requests github <https://github.com/requests/requests>`_

#. `EasyDict <https://pypi.python.org/pypi/easydict/>`_ for supplying the dotted dictionary notation functionality.

	* `EasyDict github <https://github.com/makinacorpus/easydict>`_