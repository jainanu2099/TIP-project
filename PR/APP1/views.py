import csv
import re
import tweepy

import matplotlib.pyplot as plt
from django.shortcuts import render
from textblob import TextBlob


def get_info(request):
    searchTerm = None
    NoOfTerms = None
    tweetText = []
    fetched_tweets = []
    
    if request.method == "POST":
        searchTerm = request.POST['keyword']
        NoOfTerms = request.POST['num']
    else:
        if searchTerm is None or NoOfTerms is None:
            return render(request, 'firsthtml.html')
  
    print(searchTerm, NoOfTerms)
    
    consumerKey = 'BGKDzIhDmtUol8qDW9R8lJwQ7'
    consumerSecret = 'Hy9tNkHHLA9Ccp6Vz2hQ3nQQKAM3q8fHYbu2X8cJefz8BVVHMf'
    accessToken = '1163863698349293569-DSJyprSNfi5if0l8HnrOgLsJ8fYl7H'
    accessTokenSecret = 'x1KzbrkaxJiNDGuN8dvnd7JdgU042zENX7yRy6brGvSdB'
    
    try:
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        print("Auth successful")
    
    except():
        print("Error: Authentication Failed")

    def cleanTweet(tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+|([^0-9A-Za-z \t])|(\w+:\/\/\S+))", " ", str(tweet)).split())

    def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(positive, wpositive, spositive, negative, wnegative,
                     snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive ['+str(spositive) + '%]','Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) +
                  ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    # searching for tweets
    fetched_tweets = tweepy.Cursor(api.search, q=searchTerm,
            lang="en").items(int(NoOfTerms) if NoOfTerms else 1)

    # Open/create a file to append data to
    csvFile = open('result7.csv', 'w')

    # Use csv writer
    csvWriter = csv.writer(csvFile)
    # print('run successful\n')

    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    
    for tweet in fetched_tweets:
        # Append to temp so that we can store in csv later.
        # print(tweet.text)
        tweetText.append(cleanTweet(tweet.text).encode('utf-8'))

        analysis = TextBlob(tweet.text)
        # print(analysis.sentiment.polarity)  # print tweet's polarity
        polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
        
        if analysis.sentiment.polarity == 0:  # adding reaction of
            neutral = neutral + 1             # how people are reacting to find average later
        elif 0 < analysis.sentiment.polarity <= 0.3:
            wpositive = wpositive + 1
        elif 0.3 < analysis.sentiment.polarity <= 0.6:
            positive = positive + 1
        elif 0.6 < analysis.sentiment.polarity <= 1:
            spositive = spositive + 1
        elif -0.3 < analysis.sentiment.polarity <= 0:
            wnegative = wnegative + 1
        elif -0.6 < analysis.sentiment.polarity <= -0.3:
            negative = negative + 1
        elif -1 < analysis.sentiment.polarity <= -0.6:
            snegative = snegative + 1

    # Write to csv and close csv file
    csvWriter.writerow(tweetText)
    csvFile.close()
    
    positive = percentage(positive, NoOfTerms)
    wpositive = percentage(wpositive, NoOfTerms)
    spositive = percentage(spositive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    wnegative = percentage(wnegative, NoOfTerms)
    snegative = percentage(snegative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

    polarity = float(polarity) / float(NoOfTerms)

    # printing out data
    print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
    print()
    print("General Report: ")

    if polarity == 0:
        print("Neutral")
    elif 0 < polarity <= 0.3:
        print("Weakly Positive")
    elif 0.3 < polarity <= 0.6:
        print("Positive")
    elif 0.6 < polarity <= 1:
        print("Strongly Positive")
    elif -0.3 < polarity <= 0:
        print("Weakly Negative")
    elif -0.6 < polarity <= -0.3:
        print("Negative")
    elif -1 < polarity <= -0.6:
        print("Strongly Negative")

    print()
    print("Detailed Report: ")
    print(str(positive) + "% people thought it was positive")
    print(str(wpositive) + "% people thought it was weakly positive")
    print(str(spositive) + "% people thought it was strongly positive")
    print(str(negative) + "% people thought it was negative")
    print(str(wnegative) + "% people thought it was weakly negative")
    print(str(snegative) + "% people thought it was strongly negative")
    print(str(neutral) + "% people thought it was neutral")

    plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)

    return render(request, 'firsthtml.html')







def display(request):
    return render(request, 'result.html')
