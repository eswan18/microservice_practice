import requests


r = requests.post('http://127.0.0.1:5000/get_tweets', data=b'{"user": "zachlowe_nba", "count": "3"}')

print(r.json()[0])
