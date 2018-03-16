import textblob
import numpy as np
import matplotlib.pyplot as plt
import json

sentiment_list = []
input_txt_file = input("Which file would you like to import?")
input_file = open(input_txt_file, "r")
# Open the file with out tweets

for item in input_file:
    sentiment_list.append(textblob.TextBlob(json.loads(item)["text"]).sentiment.polarity)
    # For every tweet in our file: Find the text, Record and append the sentiment

hist = np.histogram(sentiment_list)
plt.hist(sentiment_list)
plt.xlabel("Sentiment")
plt.ylabel("Frequency")
plt.show()
# Plot the sentiment in a histogram
