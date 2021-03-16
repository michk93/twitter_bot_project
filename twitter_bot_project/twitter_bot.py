from credentials import *
import tweepy
import time, datetime

################### API AUTHENTICATION ###################
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
##########################################################

# SETS THE FILES TO A VARIABLE
FILE_NAME = 'last_seen.txt'
quote_file = 'quotes_to_tweet.txt'
menu_option = 0

# GETS THE ID OF THE LAST PULLED TWEET
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

# STORES THE ID OF THE LAST PULLED TWEET
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
    # FOR TESTING USE THIS ID 1371486654133895169
    # 1371567807071195138
# REPLY TO TWEETS METHOD
def reply_to_tweets():
    print('looking up tweets and replying to them...')
    # POINTS A VARIABLE TO A METHOD TO GET THE LAST PULLED ID
    # AND ATTACHES THE FILE WITH STORED TWEET IDS
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # PULLS MENTIONS IGNORING ANYTHING BEFORE THE LAST SEEN ID
    mentions = api.mentions_timeline(
                    last_seen_id,
                    tweet_mode='extended')
    # LOOP - REPLIES TO EVERY MENTION AND DISPLAYS THEM IN REVERSE ORDER
    # (OLD MENTION TOP, NEW MENTION BOTTOM)
    # STORES THE ID OF EACH POST INTERACTED WITH
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if mention.full_text.lower():
            print('a mention has been found!')
            print('responding in progres...\n \n')
            api.update_status('@' + mention.user.screen_name + ' this is an automated response. Test has been successful', mention.id)
            time.sleep(30)

# POSTING TWEETS FROM A FILE METHOD
def posting_tweets():
    print("posting today's tweet")
    # READS FROM A FILE
    f_quotes = open(quote_file, 'r')
    # READ LINES - ONE BY ONE - ASSIGNED TO A VARIABLE
    file_lines = f_quotes.readlines()
    f_quotes.close()
    # LOOP TO ITERATE OVER LINES FROM A FILE
    for line in file_lines:
        try:

            print('posting...\n' + line)
            api.update_status(line)
            time.sleep(5)
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(2)

def menu():


while True:
    posting_tweets()
    reply_to_tweets()
