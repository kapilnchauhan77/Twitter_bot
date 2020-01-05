import tweepy
import time
from textblob import TextBlob
print('this is my twitter bot', flush=True)
auth = tweepy.OAuthHandler('yiUbLJuxRRTHpZImLhdg9jWYe', 'duHLQOLtmhCX4gPTBxrDeF29j3pVokWC9230vDQrSRrnDFIY7c')
auth.set_access_token('858510109332447232-3hYibbQNq1m44VijTmswiPe1lE9Ud79', 'IJF7FdlmlGkNShjrExlR71m9cl3ZWxLZavTB4WgHvHJrk')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
FILE_NAME = 'last_seen_id.txt'
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if mention.user.screen_name != 'KapilCh23582972':
            if 'brodad' in mention.full_text.lower():
                print('found kapil!', flush=True)
                print('responding back...', flush=True)
                api.update_status('@' + mention.user.screen_name +
                        ' Hey bro wassup', mention.id)
            else:
                print('found user', flush=True)
                print('responding back...', flush=True)
                a = TextBlob(mention.full_text)
                a.correct
                b = a.sentiment.polarity
                c = a.sentiment.subjectivity
                print(b,c)
                if b < (-0.45) :
                    if c < 0.45 :
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are negative but logical and factual', mention.id)
                    else:
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are negative and entitled to your own personal opinion', mention.id)
                elif b > (-0.45) and b < 0.00 :
                    if c < 0.45 :
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are just a bit negative but logical and factual', mention.id)
                    else:
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are just a bit negative and entitled to your own personal opinion', mention.id)
                elif b == 0.00 :
                    if c < 0.45 :
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are neutral but logical and factual', mention.id)
                    else:
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are neutral and entitled to your own personal opinion', mention.id)
                elif b > 0.00 and b < 0.35:
                    if c < 0.45 :
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are quite positive but logical and factual', mention.id)
                    else:
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are quite positive and entitled to your own personal opinion', mention.id)
                elif b > 0.35:
                    if c < 0.45 :
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are very positive but logical and factual', mention.id)
                    else:
                        api.update_status('@' + mention.user.screen_name +
                                ' Your thoughts are very positive and entitled to your own personal opinion', mention.id)
                else:
                    print('found error!!!!!!!!', flush=True)
                    print('responding back...', flush=True)
                    api.update_status('@' + mention.user.screen_name +
                            ' Please contact me on insta there seems to be some technical error', mention.id)

while True:
    reply_to_tweets()
    time.sleep(2)