from os import environ
url = 'https://notify-api.line.me/api/notify'
token = environ['TOKEN']
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}