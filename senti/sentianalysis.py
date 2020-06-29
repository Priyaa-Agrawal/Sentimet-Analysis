import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import datetime
import os
from datauri import DataURI

#generating image url
def imageUrl(src):
    png_uri = DataURI.from_file(src)
    mt = png_uri.mimetype
    return png_uri


# Analysing Sentiment as Positve or Negative or Neutral


def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        return 'Negative Vibes'
    elif pos > neg:
        return 'Positive Vibes'
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

    # Graph Ploting Process

    # Converting text into token list
    tokenized_words = word_tokenize(cleaned_text, "english")

    # Removing Stopwords from the tokenized words
    final_words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)

    # Calculating Emotion of the final words
    emotion_list = []
    with open('senti/emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(
                ",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')
            if word in final_words:
                emotion_list.append(emotion)

    # Counting words of same emotions
    w = Counter(emotion_list)
    url = []
    fname = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    # Bar Graph
    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()
    srcG = f'media/input/g-{fname}.png'
    srcC = f'media/input/c-{fname}.png'
    plt.savefig(srcG)
    plt.close()
    url.append(imageUrl(srcG))

    # WordCloud graph
    stop_words = set(STOPWORDS)
    wordcloud = WordCloud(width=800, height=800, background_color='white',
                          stopwords=stop_words, min_font_size=10).generate(text)

    wordcloud.to_file(srcC)
    url.append(imageUrl(srcC))

    os.remove(srcG)
    os.remove(srcC)

    return [temp, url]
