import tweepy
import textblob
import numpy as np
import matplotlib.pyplot as plt
import jsonpickle
import time

consumer_api_key = ''
consumer_api_key_secret = ''
access_token = ''
access_token_secret = ''

searchQuery = input("Enter the word you would like to search for.")
# Ask user for keywords they would like to look for

auth = tweepy.OAuthHandler(consumer_api_key, consumer_api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# Gain access to twitter API

maxTweets = 10000000
tweets_per_query = 100
# Set Maximum number of tweets we require and the tweets to pull up per query

output_file = 'Output.txt'
since_id = None
max_id = -1
Counts = 0
# Name the output file we would like to create or edit
# Since_id to recognize how far back in the past we want to find tweets.
# It is the lower limit
# Max id is the upper limit. Starting from max id, query will look
#  for older tweets
# Counts simply keeps track on the number of tweets we have pulled

tweet_sentiment = []
# tweet sentiment to keep track of the sentiment of the tweets we have pulled

print("Downloading max {0} tweets".format(Counts))

with open(output_file, 'w') as f:
    while Counts < maxTweets:
        try:
            if (max_id <= 0):
                if (not since_id):
                    new_tweets = api.search(q=searchQuery, count=tweets_per_query)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweets_per_query,
                                            since_id=since_id)
                    # search for tweets without a max_id for context
                    # if since id is given, use as a lower limit

            else:
                if (not since_id):
                    new_tweets = api.search(q=searchQuery, count=tweets_per_query,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweets_per_query,
                                            max_id=str(max_id - 1),
                                            since_id=since_id)
                    # else if a max id is provided, look for tweets older than it
                    # if since id is also provided, find tweets inbetween em

            if not new_tweets:
                print("No more tweets found")
                break
                # break look if we have found all relevant tweets

            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
                tweet_sentiment.append(textblob.TextBlob(tweet.text).\
                                       sentiment.polarity)
                # Write tweets to our output file as JSON
                # Use textblob (word lexicon) to judge the sentiment of
                # those tweets
                # and append to out list for later use when graphing

            Counts += len(new_tweets)
            print("Downloaded {0} tweets".format(Counts))
            max_id = new_tweets[-1].id
            # increment counts to keep track of the number of tweets we
            #  have downloaded
            # change max_id to keep track of the tweets we have already pulled

        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            time.sleep(60*15)
            # Errors are usually due to rate limit. Print out error and let
            # program sleep until rate limit is refreshed


# Tweet crawling methodology taken from BHASKAR KARAMBELKAR'S BLOG
# An amazing resource

hist = np.histogram(tweet_sentiment)
plt.hist(tweet_sentiment)
plt.show()

# plot a histogram to show sentiment surrounding keyword


