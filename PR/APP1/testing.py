from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from textblob.sentiments import PatternAnalyzer
analysis = TextBlob("He is a greatest liar but he is not that bad",  analyzer = NaiveBayesAnalyzer())

#analysis1 = TextBlob("He is a greatest liar but he is not that bad",  analyzer = PatternAnalyzer())

print(analysis.polarity)
print(analysis1.polarity)