import requests

app_id = '<APP_ID>'
report_type = '<REPORT_TYPE>'

params = {
  'api_token': '<API_TOKEN>',
  'from': 'FROM_DATE',
  'to': 'TO_DATE'
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

