"""
    compute the sentiment of the terms that do not appear in the file 
    AFINN-111.txt.
"""


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
    clean_tweet():
    format raw twitterdata, extract twitter text information
    (file) -> ([str, list])
"""
def clean_tweet(file):
    tweets=[]
    for line in file:
        try:
            tweet=json.loads(line)
            if tweet.has_key('text'):
                tweet_text = tweet['text'].encode('utf-8')
                tweet_words =tweet_text.split()
        
                for i in range(len(tweet_words)):
                    tweet_words[i]=tweet_words[i].strip(",.:!")
                tweets.append(tweet_words)    
        except:
            continue
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

    # clean the twitters
    tweets=clean_tweet(tweet_file)
    num=len(tweets)

    # initiate sentiment score list
    sentiments=[0]*num

    # calculate sentiment score of each tweet
    for i in range(num):
        sentiments[i]=calculate_score(tweets[i],dictionary)

    new_dictionary=dict()
    # assign sentiment score to unknown term
    for i in range(num):
        for word in tweets[i]:
            if word not in dictionary:
                if word not in new_dictionary and sentiments[i]<0:
                    new_dictionary[word]=[0,-sentiments[i]]
                elif word not in new_dictionary and sentiments[i]>0:
                    new_dictionary[word]=[sentiments[i],0]
                elif word in new_dictionary and sentiments[i]<0:
                    new_dictionary[word][0]-=sentiments[i]
                elif word in new_dictionary and sentiments[i]>0:
                    new_dictionary[word][1]+=sentiments[i]

                
    for word in new_dictionary:
        if new_dictionary[word][0]==0:
            new_score=float(new_dictionary[word][1])
        elif new_dictionary[word][1]==0:
            new_score=-float(new_dictionary[word][0])
        else:
            new_score=float(new_dictionary[word][1])/new_dictionary[word][0]
                           
        print ("%s %f" % (word,new_score))
   

if __name__ == '__main__':
    main()
