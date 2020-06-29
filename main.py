import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import ast
authenticator = IAMAuthenticator('Icm8EDkcRK9-TC4cP-O3qdec2oQ3C-he9iIOgLefBgTk')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/dc3bf3f4-b8a0-48bb-bc2a-eb1678b197aa')

  
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        # authenticating
        consumer_key = 'ijp50vWS5KU7UcUjCwz27Ov3E'
        consumer_secret = 'g4IrQnMKPDpqo8K2M5rnRvokPkIvzJ05bpysfZvStrHOBTrJMx'
        access_token = '1110101452695834624-WxoRCZTtKQwXrLtMjGoKGt3v2duAEg'
        access_token_secret = 'wI9kXYbSvIHzG9sKYgG0MptOtsYc5X15uYCrbO59b3NBY'

# attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        text = tweet
        tone_analysis = tone_analyzer.tone(
         {'text': text},
              content_type='application/json'
              ).get_result()

        res=(json.dumps(tone_analysis))
        res= ast.literal_eval(res)
       # res = not bool(test_dict) 
        #if len(res['document_tone']['tones']) > 0:
             #  print(res['document_tone']['tones'][0]['tone_name'])
       # print(res)
        
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets(query = 'covid', count = 10000000) 
    print(len(tweets))
  
  
if __name__ == "__main__": 
    # calling main function 
    main() 