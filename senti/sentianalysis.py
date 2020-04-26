import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


# Analysing Sentiment as Positve or Negative or Neutral
def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)

    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        return 'Negative Sentiment'
    elif pos > neg:
        return 'Positive Sentiment'
    else:
        return 'Neutral Vibes'


def main_function(text):

    # Converting complete text into lower case
    lower_case = text.lower()

    # Removing Punctuations
    cleaned_text = lower_case.translate(
        str.maketrans('', '', string.punctuation))

    # Calling sentiment analyse function
    temp = sentiment_analyse(cleaned_text)

    return temp
