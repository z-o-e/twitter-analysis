import sys
import json


""" 
    calculate_score():
    calculate score of a given list of text
    (list, dict) -> float    
"""
def calculate_score(text, dictionary):
    score=0
    for item in text:
        if item in dictionary:
            score=score+dictionary[item]
    return score



"""
    get_tweet_and_place():
    format raw twitterdata, extract twitter text and location(state) information
    (file) -> ([str, list, str])
"""
def get_tweet_and_place(tweet_file):
    tweets_words=[]
    tweets_location=[]
    for line in tweet_file:
        try:
            tweet=json.loads(line)
            if tweet.has_key('place') and tweet.has_key('text'):
                if tweet['place']['country_code']=='US':
                    state = tweet['place']['full_name'][-2:].encode('utf-8')
                    tweet_text = tweet['text'].encode('utf-8')
                    tweet_words = tweet_text.split()
                    for i in range(len(tweet_words)):
                        tweet_words[i]=tweet_words[i].lower().strip(",.:'!")
                    tweets_words.append(tweet_words)
                    tweets_location.append(state)
        except:
            continue
    tweets=[tweets_words,tweets_location]
    return tweets
    


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    
    # store sentiment evaluation file into string
    f=sent_file.readlines()
    
    
    # initiate a dictionary
    dictionary=dict()


    # formulate dictionary, keys are sentiment word, values are scores
    for line in f:
        line=(line.strip('\n')).split('\t')
        word=line[0]
        score=line[1]
        dictionary[word]=int(score)


    # clean the tweets and get location information
    tweets=get_tweet_and_place(tweet_file)
    num=len(tweets[0])
    
    
    # sentiment score list for each tweet
    sentiments=[0]*num
    for i in range(num):
        sentiments[i]=calculate_score(tweets[0][i],dictionary)
    
    
    # cummulative sentiment score and occurrences for each state
    state_sentiment=dict()
    for i in range(num):
        state=tweets[1][i]
        if state_sentiment.has_key(state):
            state_sentiment[state]=[ state_sentiment[state][0]+sentiments[i] ,
                             state_sentiment[state][1]+1 ]   
        else:
            state_sentiment[state]=[sentiments[i],1]
                             
    # calculate regularized sentiment score for each state
    for item in state_sentiment:
        state_sentiment[item]=state_sentiment[item][0]/state_sentiment[item][1]
    
    # find the highest sentiment score and corresponding state    
    highest_score=0    
    for item in state_sentiment:
        if state_sentiment[item]>highest_score:
            happiest_state=item
            highest_score=state_sentiment[item]
                
    print happiest_state
        

if __name__ == '__main__':
    main()
            
