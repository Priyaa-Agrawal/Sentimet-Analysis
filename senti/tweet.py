import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from datauri import DataURI
import datetime
import os
from . import secret as sc


def imageUrl(src):
    png_uri = DataURI.from_file(src)
    mt = png_uri.mimetype
    return png_uri


def tweetanalysis(searchTerm,NoOfTerms):
    # authenticating
    consumerKey = sc.consumerKey
    consumerSecret = sc.consumerSecret
    accessToken = sc.accessToken
    accessTokenSecret = sc.accessTokenSecret
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)


    # searching for tweets
    tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)


    # Open/create a file to append data to
    fname = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    filename = f'media/input/{fname}.csv'
    csvFile = open(filename, 'a')

    # Use csv writer
    csvWriter = csv.writer(csvFile)


    # creating some variables to store info
    polarity = 0
    positive = 0
    negative = 0
    neutral = 0

    tweetText = []

    # iterating through tweets fetched
    for tweet in tweets:
        #Append to temp so that we can store in csv later. I use encode UTF-8
        tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        # print (tweet.text.translate(non_bmp_map))    #print tweet's text
        analysis = TextBlob(tweet.text)
        # print(analysis.sentiment)  # print tweet's polarity
        polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
        # print('polarity-->',polarity)
        # print('analysis.sentiment.polarity-->',analysis.sentiment.polarity)
        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
            # print('netural-->',neutral)
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
            positive += 1
            # print('positive-->',positive)
        elif (analysis.sentiment.polarity >= -1 and analysis.sentiment.polarity < 0):
            negative += 1
            # print('negative-->',negative)


    # Write to csv and close csv file

    csvWriter.writerow(tweetText)
    csvFile.close()

    # finding average of how people are reacting
    positive_percentage = percentage(positive, NoOfTerms)
    negative_percentage = percentage(negative, NoOfTerms)
    neutral_percentage = percentage(neutral, NoOfTerms)
    # print('neutral_percentage -->',neutral_percentage)
    # print('positive_percentage-->',positive_percentage)
    # print('negative_percentage-->',negative_percentage)
    
    # finding average reaction
    polarity_percentage = polarity / NoOfTerms
    print('polarity_percentage-->',polarity_percentage)

    # printing out data
    print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
    print()
    print("General Report: ")

    s = max(positive_percentage,negative_percentage,neutral_percentage)
    if (s == neutral_percentage):
        sentiment = "Neutral"
    elif (s == positive_percentage):
        sentiment = "Positive"
    elif (s == negative_percentage):
        sentiment = "Negative"

    print()
    print("Detailed Report: ")
    print(str(positive_percentage) + "% people thought it was positive")
    print(str(negative_percentage) + "% people thought it was negative")
    print(str(neutral_percentage) + "% people thought it was neutral")

    graph = plotPieChart(positive_percentage, negative_percentage, neutral_percentage, searchTerm, NoOfTerms)
    os.remove(filename)
    
    return [sentiment,graph]


def cleanTweet(tweet):
    # Remove Links, Special Characters etc from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

# function to calculate percentage
def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

def plotPieChart(positive, negative, neutral, searchTerm, noOfSearchTerms):
    
    fname = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                'Negative [' + str(negative) + '%]']
    sizes = [positive,  neutral, negative]
    colors = ['green', 'gold', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on \n ' + searchTerm + '\n by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    srcG = f'media/input/g-{fname}.png'
    plt.savefig(srcG)
    # plt.show()
    plt.close()
    graph = imageUrl(srcG)
    os.remove(srcG)
    
   

    return graph



