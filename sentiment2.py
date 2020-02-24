#NewSentiment
#Stephen Schneider
#Capstone Python Text Analytics Project

from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt

#create a function to calculate the percentage. Takes 2 arguments, part and whole.
def percentage(part, whole):
	return 100 * float(part)/float(whole)

#Twitter app info	
consumerKey = "nT8KP0LQX0p7sxqgUawojrpxd"
consumerSecret = "lZFejHEMD5mA7Lwjxc47DuHe6gUekG4wddo270UIRbzigUj6fq"
accessToken = "1046519830461984768-JiGfq4e0VNGgewONGM8A5ixBcFWUT3"
accessTokenSecret = "ITvIwjGNdJY28gmJRlJM9ZdKmiVbRMILgmLAGgKnLBSYS"

#establish connection to Twitter API
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#Get input from user, what to search and how many tweets to analyze
searchTerm = input("Enter keyword to search: ")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))

#make tweets based on search criteria
tweets = tweepy.Cursor(api.search, q=searchTerm).items(noOfSearchTerms)

#TextBlob rates a sentence from -1 to 1. -1 being extremely negative. 1 being extremely positive.
#Test: a = TextBlob("I am the worst programmer ever."
#a.sentiment.polarity
# -1
#b = TextBlob("I am the best programmer ever.")
#b.sentiment.polarity
# 1
#c = TextBlob("I am a programmer.")
#c.sentiment.polarity
# 0

#create 3 variables to store the polarity
positive = 0
negative = 0
neutral = 0
polarity = 0

#get total polarity for all the tweets
for tweet in tweets:
	#print(tweet.text)
	analysis = TextBlob(tweet.text)
	polarity += analysis.sentiment.polarity
	
	if(analysis.sentiment.polarity == 0):
		neutral += 1

	elif(analysis.sentiment.polarity < 0.00):
		negative += 1
	
	elif(analysis.sentiment.polarity > 0.00):
		positive += 1

#calculate percentage of positive, negative, and neutral		
positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)

#reformat to 2 decimal places
positive = format(positive, '.2f')
negative = format(negative, '.2f')
neutral = format(neutral, '.2f')

print("How people are reacting to " +searchTerm + " by analyzing " +str(noOfSearchTerms) + " Tweets.")

#print consensus
if (polarity == 0):
	print("Neutral")
elif (polarity < 0):
	print("Negative")
elif (polarity > 0):
	print("Positive")
	
#create pie chart
labels = ['Positive ['+str(positive)+ '%]', 'Neutral ['+str(neutral)+ '%]', 'Negative ['+str(negative)+ '%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches,labels, loc="best")
plt.title("How people are reacting to " +searchTerm + " by analyzing " +str(noOfSearchTerms) + " Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()
