"""
    computes the ten most frequently occurring hash tags 
    from the gathered data
"""


import sys
import json

def get_hashtags(tweet_file):
    hashtag_dict=dict()
    for line in tweet_file:
        try:
            tweet=json.loads(line)
            if tweet['entities']['hashtags']!=[]:
                for i in range(len(tweet['entities']['hashtags'])):
                    hashtags=tweet['entities']['hashtags']
                    if hashtag_dict.has_key((hashtags[i])['text']):
                        hashtag_dict[(hashtags[i])['text']]+=1                        
                    else:
                        hashtag_dict[(hashtags[i])['text']]=1
        except:
            continue
    return hashtag_dict


def main():
    tweet_file = open(sys.argv[1])
    
    # get hashtag dictionary and sort the converted list
    hashtags=get_hashtags(tweet_file)
    hashtags_list=[]

    for item in hashtags:
        hashtags_list.append([hashtags[item],item])

    hashtags_list=sorted(hashtags_list)
    
    # print top_ten
    for i in range(1,11):
        print("%s %f" %(hashtags_list[-i][1],hashtags_list[-i][0]))
    
    

if __name__ == '__main__':
    main()
