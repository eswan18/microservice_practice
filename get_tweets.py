from flask import Flask, request
import tweepy
import json, pickle

from creds import creds

app = Flask(__name__)

# Create the API
auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
auth.set_access_token(creds['access_token'], creds['access_secret'])
api = tweepy.API(auth)

@app.route('/get_tweets', methods=['POST'])
def get_tweets():
    data = json.loads(request.data)
    user, count = data['user'], int(data['count'])
    # Initialize a list to hold all the tweepy Tweets.
    all_tweets = []
    # Make initial request for most recent tweets.
    # (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=user, count=200)
    # While you keep getting tweets back, but still need more.
    while len(new_tweets) > 0 and len(all_tweets) + len(new_tweets) < count:
        # Save the most recent tweets.
        all_tweets += new_tweets
        # Save the id of the oldest tweet less one.
        oldest = all_tweets[-1].id - 1
        # Try to pull more
        new_tweets = api.user_timeline(screen_name=user, count=200, max_id=oldest)
    all_tweets += new_tweets

    # Keep only the first `count` tweets
    all_tweets = all_tweets[:count]
    print(len(all_tweets))
    return json.dumps([tweet._json for tweet in all_tweets])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
