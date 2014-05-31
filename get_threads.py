from skills import retrieve_json
import datetime
import re

pages = 3
url = 'https://hn.algolia.com/api/v1/search?query=%22freelancer?%20seeking%20freelancer%22&tags=story'

ids = []

for i in xrange(0, pages):
  search_results = retrieve_json(url + '&page={}'.format(i))
  for hit in search_results['hits']:
    print hit['title'], hit['objectID']
  
  for hit in search_results['hits']:
    if re.search('hiring', hit['title'].lower()):
      continue
    try:
      date_match = re.search('\w+ \d+', hit['title'])
      month_year = date_match.group()
      month_year = datetime.datetime.strptime(month_year, "%B %Y")
      ids.append((month_year, hit['objectID']))
    except AttributeError:
      print('Failed to parse:')
      print(hit['title'])
      print(hit['objectID'])

print('----------------\n')
ids.sort()
for date, id in ids:
  print('{} {}'.format(date.strftime('%Y %B'), id))
