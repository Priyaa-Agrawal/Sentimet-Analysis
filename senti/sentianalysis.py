import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


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

    # Bar Graph
    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()
    plt.savefig('media/graph.png')
    plt.close()

    # WordCloud graph
    stop_words = set(STOPWORDS)
    wordcloud = WordCloud(width=800, height=800, background_color='white',
                          stopwords=stop_words, min_font_size=10).generate(text)

    wordcloud.to_file('media/cloud.png')

    return temp
