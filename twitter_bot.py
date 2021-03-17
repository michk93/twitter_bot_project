from credentials import *
import tweepy
import time, datetime
import random

################### API AUTHENTICATION ###################
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
##########################################################

# SETS THE FILES TO A VARIABLE
_lastMentionID = 'last_seen.txt'
quote_file = 'quotes_to_tweet.txt'
responses = 'responses_to_mentions.txt'

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
    last_seen_id = retrieve_last_seen_id(_lastMentionID)
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
        store_last_seen_id(last_seen_id, _lastMentionID)
        if mention.full_text.lower():
            print('\na mention has been found!')
            print('picking a response...\n\n')
            print('responding in progres...\n \n')
            api.update_status('@' + mention.user.screen_name + " " + random_line_picker(responses), mention.id)
            time.sleep(30)

# POSTING TWEETS FROM A FILE METHOD
def posting_tweets():
    print("\nfinding today's tweet...\n")
    random_line_picker(quote_file)
    #api.update_status(quote_file)
    time.sleep(900)

# PICKS A RANDOM LINE FROM A FILE
def random_line_picker(file_name):
    print('fetching the line from a file... \n')
    rand_read = open(file_name, 'r')
    rand_line = rand_read.readlines()
    _Listline = []
    for i in range(0, len(rand_line)-1):
        try:
            x = rand_line[i]
            z = len(x)
            a = x[:z-1]
            _Listline.append(a)
            _Listline.append(rand_line[i+1])
            picked_line = random.choice(_Listline)
            print('line picked!\n' + picked_line)
            rand_read.close()
            return picked_line
        except tweepy.TweepError as e:
            f_log = open('log.txt', 'w')
            error_log = f_log.writelines()
            print(e.reason)
            print('\n' + time.date() + '\n')
            f_log.close()
            print('\n Saved to Log.txt')
            time.sleep(2)



while True:
    #posting_tweets()
    reply_to_tweets()
