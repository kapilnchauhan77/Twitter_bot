import tweepy
import time
import numpy as np
import random
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

print('This is my twitter bot', flush=True)
auth = tweepy.OAuthHandler('yiUbLJuxRRTHpZImLhdg9jWYe',
                           'duHLQOLtmhCX4gPTBxrDeF29j3pVokWC9230vDQrSRrnDFIY7c')
auth.set_access_token('858510109332447232-3hYibbQNq1m44VijTmswiPe1lE9Ud79',
                      'IJF7FdlmlGkNShjrExlR71m9cl3ZWxLZavTB4WgHvHJrk')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
FILE_NAME = 'last_seen_id.txt'

data = fetch_movielens(min_rating=4.0)

model = LightFM(loss='warp')

model.fit(data['train'], epochs=30, num_threads=3)


def sample_recommendation(model, data, user_ids, n_users, n_items, known_positives, mention):

    for user_id in user_ids:

        scores = model.predict(user_id, np.arange(n_items))

        top_item = data['item_labels'][np.argsort(-scores)]

        movies_to_recommend = []

        for movie_to_recommend in top_item[:3]:
            if movie_to_recommend not in movies_to_recommend:
                movies_to_recommend.append(movie_to_recommend)
            else:
                pass

        api.update_status('@' + mention.user.screen_name +
                          ' Recommended movies:\n' + '; '.join(movies_to_recommend), mention.id)


def find_user_id(model, data, favourite_movie):
    answered_user_ids = []

    n_users, n_items = data['train'].shape

    for user_id_I_want in range(n_users):
        known_positive_movies = data['item_labels'][data['train'].tocsr()[
            user_id_I_want].indices]
        for known_positive_movie in known_positive_movies[:900]:
            if favourite_movie.lower() in known_positive_movie.lower():
                answered_user_ids.append(user_id_I_want)
                if len(answered_user_ids) > 5:
                    return answered_user_ids, n_users, n_items, known_positive_movies
                    break
                else:
                    continue
            else:
                continue
    if answered_user_ids == []:

        for N_iteration in range(3):
            answered_user_ids.append(random.randrange(3))

        return answered_user_ids, n_users, n_items, known_positive_movies

    else:

        return answered_user_ids, n_users, n_items, known_positive_movies


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
                mention.full_text = mention.full_text.replace(
                    '@KapilCh23582972', '').strip()
                final_user_ids, n_users, n_items, known_positives = find_user_id(
                    model, data, mention.full_text)
                sample_recommendation(model, data, final_user_ids,
                                      n_users, n_items, known_positives, mention)


while True:
    reply_to_tweets()
    time.sleep(12)
