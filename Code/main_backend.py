import pandas as pd
from twitter_scrapper import get_tweets_by_searchquery, clean_tweets
from text_ml import generate_sentiment_information_for_all_tweets, get_mean_sentiment

def get_recommendation(path_to_stocks, sample=10):
#    stocks = pd.read_pickle(path_to_stocks)
    stocks=path_to_stocks
    #print(stocks)
    stocks.dropna(inplace=True)
    
    stock_sample = stocks[:9]
    print('stock selection stage_1')
    print(stock_sample)
    stock_sample.reset_index(drop=True, inplace=True)
    stock_sample['sentiment'] = 0.0
    for i in range(len(stock_sample)):
        stock_name = stock_sample['long_name'].iloc[i]
        print(stock_name)
        sentiment = get_mean_sentiment(generate_sentiment_information_for_all_tweets(clean_tweets(get_tweets_by_searchquery(f'{stock_name}', 300), 'en')))
        stock_sample.at[i, 'sentiment'] = sentiment
    stock_sample.to_pickle('Data/Stock/stock_recommendation.pkl')
    print(stock_sample)
    return stock_sample
        
        
#path = 'Data/df_esg_final'
#get_recommendation(path)
