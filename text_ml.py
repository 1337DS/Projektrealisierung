import pandas as pd
from textblob import TextBlob
import re
import numpy as np

def cleanUpTweet(txt):
    # Remove mentions
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
    # Remove hashtags
    txt = re.sub(r'#', '', txt)
    # Remove retweets:
    txt = re.sub(r'RT : ', '', txt)
    # Remove urls
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
    #remove <>
    txt = re.sub(r'<', '', txt)
    txt = re.sub(r'>', '', txt)
    #remove all non word characters
    txt = re.sub(r'[^\w\s\d]|_', '', txt)
    return txt

#subjectivity
def getTextSubjectivity(txt):
    return TextBlob(txt).sentiment.subjectivity

#polarity
def getTextPolarity(txt):
    return TextBlob(txt).sentiment.polarity

# negative, nautral, positive analysis
def getTextAnalysis(pol):
    pol = float(pol)
    if pol < 0:
        return "Negative"
    elif pol == 0:
        return "Neutral"
    else:
        return "Positive"

def generate_sentiment_information_for_all_tweets(df):
    if df is not None:
        df['text_cleaned'] = ''
        df['subjectivity'] = 0.0
        df['polarity'] = 0.0
        df['sentiment'] = 0.0
        #print(df.info())
        for r in range(len(df)):
            
            # get the cleaned text
            txt = df['text'].iloc[r]
            clean_txt = cleanUpTweet(txt)
            df.at[r, 'text_cleaned'] = clean_txt
            
            #get polarity
            polarity = getTextPolarity(clean_txt)
            df.at[r, 'polarity'] = polarity

            #get subjectivity
            subjectivity = getTextSubjectivity(clean_txt)
            df.at[r, 'subjectivity'] = subjectivity
            
            #print(df.iloc[r])
            
            #get sentiment
            sentiment = getTextAnalysis(polarity)
            df.at[r, 'sentiment'] = sentiment
            
            
        print(df[['text_cleaned', 'polarity', 'subjectivity', 'sentiment']])
        return df

def get_mean_sentiment(df):
    if df is not None:
        df = df.loc[df['subjectivity'] >= 0.5]
        if df.empty:
            mean_sentiment = np.nan
            print(mean_sentiment)
        else:
            df.reset_index(drop=True, inplace=True)
            print(df[['text_cleaned', 'polarity', 'subjectivity', 'sentiment']])
            sentiments = df['polarity'].tolist()
            mean_sentiment = np.mean(sentiments)
            print(mean_sentiment)
        return mean_sentiment
        
        

#df = pd.read_pickle('Data/twitter/General_Dynamics_Corporation_stock_last_300.pkl')
#print(df)
#get_mean_sentiment(generate_sentiment_information_for_all_tweets(df))
    
    
        