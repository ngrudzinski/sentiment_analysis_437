#Credit to Marco Bonzanini CC-BY 4.0

import tweepy
from tweepy import OAuthHandler
from tweepy import TweepError

consumer_key = 'KGrJyI9GdujKcowMfrheB78dR'
consumer_secret = 'TEa81xn0OZOwebVyNccqQFkY2Qe0qPJbHixz1GZQZlJZ55jY2V'
access_token = '3021600922-wF6n5jmtjnd6Ip16L3CguHxK4p19OblPXjvJYvF'
access_secret = 'fVpGcfRkzJB0C0lyRUEMr7lGOhz8j1cBQ8PUyQx4FWzaK'

def scrape_tweets(user_id, tweets_scraped):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    # the 10 is an arbitrary value
    # using too much bandwidth puts the Twitter Police on you
    #for status in tweepy.Cursor(api.home_timeline).items(10):
    f = open("scrapings.text", "w+")
    try:
        timeline = api.user_timeline(screen_name = user_id, include_rts = True, count = tweets_scraped)
    except TweepError:
        print("Error scraping tweets.\n")
        f.close()
        return 1

    for tweet in timeline:
        text = u''.join(tweet.text)
        text = text.replace("\n","")

        f.write(text.encode('utf-8') + "\n")
    f.close()
    return 0


if __name__ == "__main__":
    scrape_tweets("potus", 3)