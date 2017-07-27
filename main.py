from tweetGeneration import *
import random
import tweepy
from source_messages import source_messages

number_of_runthroughs = 3
#number_of_noun_swaps = 3

blacklist = ['x']
tweet = select_base_tweet(source_messages)
print(tweet)

tweet = tweetGeneration(tweet, number_of_runthroughs, source_messages, blacklist)
tweet = check_length(tweet)
output = tweet 

print_final_output(tweet)

auth = tweepy.OAuthHandler(HIDDEN FROM PRYING EYES)
auth.set_access_token(HIDDEN FROM PRYING EYES)

api = tweepy.API(auth)

api.update_status(output)