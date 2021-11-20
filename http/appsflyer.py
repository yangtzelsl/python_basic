import requests

# id1503443165 |
app_id = ''
report_type = 'installs_report'

params = {
  'api_token': '',
  'from': '2021-10-15',
  'to': '2021-12-15'
}

request_url = 'https://hq.appsflyer.com/export/{}/{}/v5'.format(app_id, report_type)

res = requests.request('GET', request_url, params=params)

if res.status_code != 200:
  if res.status_code == 404:
    print('There is a problem with the request URL. Make sure that it is correct')
  else:
    print('There was a problem retrieving data: ', res.text)
else:
  f = open('{}-{}-{}-to-{}.csv'.format(app_id, report_type, params['from'], params['to']), 'w', newline='', encoding="utf-8")
  f.write(res.text)
  f.close()

