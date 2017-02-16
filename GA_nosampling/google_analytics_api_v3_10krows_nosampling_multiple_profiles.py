#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple intro to using the Google Analytics API v3.

This application demonstrates how to use the python client library to access
Google Analytics data. The sample traverses the Management API to obtain the
authorized user's first profile ID. Then the sample uses this ID to
contstruct a Core Reporting API query to return the top 25 organic search
terms.

Before you begin, you must sigup for a new project in the Google APIs console:
https://code.google.com/apis/console

Then register the project to use OAuth2.0 for installed applications.

Finally you will need to add the client id, client secret, and redirect URL
into the client_secrets.json file that is in the same directory as this sample.

Sample Usage:

  $ python hello_analytics_api_v3.py

Also you can also get help on all the command-line flags the program
understands by running:

  $ python hello_analytics_api_v3.py --help
"""

__author__ = 'api.nickm@gmail.com (Nick Mihailovski)'


import argparse
import sys
import csv
import string

from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError

class SampledDataError(Exception): pass


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.
  try:
    profile_id = profile_ids[profile]
    if not profile_id:
      print 'Could not find a valid profile for this user.'
    else:
      for start_date, end_date in date_ranges:
        limit = ga_query(service, profile_id, 0,
                                 start_date, end_date).get('totalResults')
        for pag_index in xrange(0, limit, 10000):
          results = ga_query(service, profile_id, pag_index,
                                     start_date, end_date)
          if results.get('containsSampledData'):
            
            raise SampledDataError
          print_results(results, pag_index, start_date, end_date)

  except TypeError, error:    
    # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')
  
  except SampledDataError:
    # force an error if ever a query returns data that is sampled!
    print ('Error: Query contains sampled data!')


def ga_query(service, profile_id, pag_index, start_date, end_date):

  return service.data().ga().get(
    ids='ga:' + profile_id,
    start_date=start_date,
    end_date=end_date,
    metrics='ga:sessions,ga:goalCompletionsAll,ga:pageviews,ga:uniquePageviews,ga:bounceRate,ga:goalConversionRateAll,ga:entrances,ga:avgTimeOnPage,ga:exitRate',
    dimensions='ga:pagePath,ga:dimension2,ga:date',
    sort='-ga:sessions',
    filters='ga:dimension2==https://launch.solidworks.co.jp/',
    start_index='1',
    max_results='10000').execute()
      

def print_results(results, pag_index, start_date, end_date):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  # New write header
  if pag_index == 0:
    if (start_date, end_date) == date_ranges[0]:
      print 'Profile Name: %s' % results.get('profileInfo').get('profileName')
      columnHeaders = results.get('columnHeaders')
      cleanHeaders = [str(h['name']) for h in columnHeaders]
      writer.writerow(cleanHeaders)
    print 'Now pulling data from %s to %s.' %(start_date, end_date)



  # Print data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      for i in range(len(row)):
        old, new = row[i], str()
        for s in old:
          new += s if s in string.printable else ''
        row[i] = new
      writer.writerow(row)

  else:
    print 'No Rows Found'

  limit = results.get('totalResults')
  print pag_index, 'of about', int(round(limit, -4)), 'rows.'
  return None


##profile_ids = profile_ids = {#'My Profile 1':   '1234567',
               #'My Profile 2':  '1234567'}
			   #'My Profile 3': '1234567',
               #'My Profile 4': '1234567'}

# Uncomment this line & replace with 'profile name': 'id' to query a single profile
# Delete or comment out this line to loop over multiple profiles.

profile_ids = {'Solidworks Prod':  '119857637'}


date_ranges = [('2017-01-01',
               '2017-01-02'),
               ('2017-01-03',
               '2017-01-04'),
               ('2017-01-05',
               '2017-01-06'),
               ('2017-01-07',
               '2017-01-08'),
               ('2017-01-09',
               '2017-01-10'),
               ('2017-01-11',
               '2017-01-12'),
               ('2017-01-13',
               '2017-01-14'),
               ('2017-01-15',
               '2017-01-16'),
               ('2017-01-17',
               '2017-01-18'),
               ('2017-01-19',
               '2017-01-20'),
               ('2017-01-21',
               '2017-01-22'),
               ('2017-01-23',
               '2017-01-24'),
               ('2017-01-25',
               '2017-01-26'),
               ('2017-01-27',
               '2017-01-28'),
               ('2017-01-29',
               '2017-01-30'),
               ('2017-01-31',
               '2017-02-01'),
               ('2017-02-02',
               '2017-02-03'),
               ('2017-02-04',
               '2017-02-05'),
               ('2017-02-06',
               '2017-02-07'),
               ('2017-02-08',
               '2017-02-09'),
               ('2017-02-10',
               '2017-02-11'),
               ('2017-02-12',
               '2017-02-13'),
               ('2017-02-14',
               '2017-02-15'),
               ('2017-02-16',
               '2017-02-17')]



for profile in sorted(profile_ids):
  path = 'C:\\Users\\k6o\\' #replace with path to your folder where csv file with data will be written
  filename = 'google_analytics_data_%s_1.csv' #replace with your filename. Note %s is a placeholder variable and the profile name you specified on row 162 will be written here
  with open(path + filename %profile.lower(), 'wt') as f:
    writer = csv.writer(f, lineterminator='\n')
    if __name__ == '__main__': main(sys.argv)
  print "Profile done. Next profile..."

print "All profiles done."

