#based on this tutorial https://medium.com/dataseries/how-to-scrape-millions-of-tweets-using-snscrape-195ee3594721

# importing libraries and packages

import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import string
from bs4 import BeautifulSoup
import spacy
import en_core_web_sm
import nltk
nltk.download('stopwords')
import datetime as dt

def get_tweets_by_searchquery(search_query, number_of_tweets):
    # Creating list to append tweet data 
    tweets_list = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    until = dt.date.today()
    since = until - dt.timedelta(days=10)
    print(until)
    print(since)
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_query} since:{since} until:{until}').get_items()):
        if i>number_of_tweets: #number of tweets you want to scrape
            break
        if i % 100 == 0:
            print(i)
        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.user.followersCount, tweet.user.location, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.lang, tweet.hashtags]) #declare the attributes to be returned
    
    # Creating a dataframe from the tweets list above 
    #print(tweets_list)
    tweets_df = pd.DataFrame(tweets_list, columns=['datetime', 'tweet_Id', 'text', 'username', 'user_followersCount', 'user_location', 'tweet_replyCount', 'tweet_retweetCount', 'tweet_likeCount', 'tweet_quoteCount', 'tweet_lang', 'tweet_hashtags'])
    #print(tweets_df)
    search_query = re.sub(r" ", "_", search_query)
    path_to_safe = f'./Data/twitter/{search_query}_last_{number_of_tweets}.pkl'
    tweets_df.to_pickle(path_to_safe)
    return path_to_safe

def get_tweets_from_user(username, number_of_tweets):
    # Creating list to append tweet data 
    tweets_list = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username}').get_items()): #declare a username 
        if i>number_of_tweets: #number of tweets you want to scrape
            break
        if i % 100 == 0:
            print(i)
        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.user.followersCount, tweet.user.location, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.lang, tweet.hashtags]) #declare the attributes to be returned
    
    # Creating a dataframe from the tweets list above 
    #print(tweets_list)
    tweets_df = pd.DataFrame(tweets_list, columns=['datetime', 'tweet_Id', 'text', 'username', 'user_followersCount', 'user_location', 'tweet_replyCount', 'tweet_retweetCount', 'tweet_likeCount', 'tweet_quoteCount', 'tweet_lang', 'tweet_hashtags'])
    #print(tweets_df)
    path_to_safe = f'./data/{username}_last_{number_of_tweets}.pkl'
    tweets_df.to_pickle(path_to_safe)
    return path_to_safe

def clean_tweets(data_path, language):
    tweets = pd.read_pickle(data_path)
    #tweets = tweets.head(5)
    
    #use and configure spacy and nltk for text cleaning
    #nlp = spacy.load('en_core_web_sm')
    stop_words = nltk.corpus.stopwords.words("english")
    
    # remove all tweets where language doesnt match
    tweets = tweets.loc[tweets['tweet_lang'] == language]
    tweets.reset_index(drop=True, inplace=True)
    tweets['clean_txt'] = ''
    #print(tweets)
    
    for r in range(len(tweets)):
        raw_text = tweets['text'].iloc[r]
        print(r, raw_text)
        
        # make text lowercase
        text = raw_text.lower()
        
        # Remove line breaks
        text = re.sub(r'\n', '', text)
        
        # Remove puncuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        
        # Remove stop words
        text = text.split()
        
        text = [word for word in text if not word in stop_words]
        
        # Remove numbers
        text = [re.sub(r'\w*\d\w*', '', w) for w in text]
        
        tweets.at[r, 'clean_txt'] = text
        print(r, text)
        tweets.to_pickle(data_path)
        return tweets
        
        

def get_tweets_for_list_of_shares(sharelist, tweets_per_stock=100):
    for share in sharelist:
        clean_tweets(get_tweets_by_searchquery(f'{share} stock', tweets_per_stock), 'en')
