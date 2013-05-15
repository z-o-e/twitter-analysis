import sys
import json
import re


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
                try:
                    tweet_text = tweet['text'].encode('utf-8')
                    tweet_words =tweet_text.split()
                    for i in range(len(tweet_words)):
                        tweet_words[i]=tweet_words[i].strip(",.:'!@")
                    tweets.append(tweet_words)
                except:
                    continue
        except:
            continue
    return tweets



def main():
    tweet_file = open(sys.argv[1])

    # clean the twitters
    tweets=clean_tweet(tweet_file)


    # initiate a dictionary and total term count
    counting=dict()
    total=0

    # formulate dictionary, keys are terms, values are number of occurrences
    for tweet in tweets:
        for t in tweet:
            if t not in counting:
                counting[t]=1
                total=total+1
            elif t in counting:
                counting[t]+=1
                total=total+1

                

    # calculate and print out frequency
    for item in counting:
        frequency=float(counting[item])/total
        print ("%s %.4f" %(item,frequency))
        

if __name__ == '__main__':
    main()
