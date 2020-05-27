import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from datauri import DataURI
import datetime
import os


def imageUrl(src):
    png_uri = DataURI.from_file(src)
    mt = png_uri.mimetype
    return png_uri


def tweetanalysis(searchTerm,NoOfTerms):
    # authenticating
    consumerKey = '****'
    consumerSecret = '*********'
    accessToken = '**********'
    accessTokenSecret = '*******'
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

        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
            positive += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= 0):
            negative += 1


    # Write to csv and close csv file

    csvWriter.writerow(tweetText)
    csvFile.close()

    # finding average of how people are reacting
    positive = percentage(positive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

    # finding average reaction
    polarity = polarity / NoOfTerms

    # printing out data
    print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
    print()
    print("General Report: ")

    if (polarity == 0):
        sentiment = "Neutral"
    elif (polarity > 0 and polarity <= 1):
        sentiment = "Positive"
    elif (polarity > -1 and polarity <= 0):
        sentiment = "Negative"

    print()
    print("Detailed Report: ")
    print(str(positive) + "% people thought it was positive")
    print(str(negative) + "% people thought it was negative")
    print(str(neutral) + "% people thought it was neutral")

    graph = plotPieChart(positive, negative, neutral, searchTerm, NoOfTerms)
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
    colors = ['blue', 'gold', 'red']
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



