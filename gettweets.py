import tweepy
import json
import pandas as pd
from pandas import DataFrame
auth = tweepy.OAuthHandler('nT8KP0LQX0p7sxqgUawojrpxd','lZFejHEMD5mA7Lwjxc47DuHe6gUekG4wddo270UIRbzigUj6fq')
auth.set_access_token('1046519830461984768-JiGfq4e0VNGgewONGM8A5ixBcFWUT3', 'ITvIwjGNdJY28gmJRlJM9ZdKmiVbRMILgmLAGgKnLBSYS')
api = tweepy.API(auth)



#---------------------- get tweet objects in json format ------------------------------------
json_list = []
user_list = []
entities_list = []
hashtag_list = []
mention_list = []
# ------------------------------------- SEARCH STRING GOES HERE ---------------------------------------
querylist = ['"@JoeBiden"AND -filter:retweets','"@BernieSanders" AND -filter:retweets','"@CoreyBooker" AND -filter:retweets','"@PeteButtigieg" AND -filter:retweets','"@JulianCastro"AND -filter:retweets','"@KamalaHarris"AND -filter:retweets','"@AmyKlobuchar"AND -filter:retweets','"@BetoORourke"AND -filter:retweets','"@TomSteyer"AND -filter:retweets','"@ElizabethWarren"AND -filter:retweets','"@AndrewYang"AND -filter:retweets' ]
#query = '"@JoeBiden" OR "@BernieSanders" OR "@CoreyBooker" OR "@PeteButtigieg" OR "@JulianCastro" OR "@KamalaHarris" OR "@AmyKlobuchar" OR "@BetoORourke" OR "@TomSteyer" OR "@ElizabethWarren" OR "@AndrewYang"  AND -filter:retweets'
for query in querylist :
    status_list = api.search(q=query, count=100)
    for status in status_list:

        #status = status_list[0]
        json_str = json.dumps(status._json)
        json_data = json.loads(json_str)
        user = json_data['user']
        del user['entities']
        user_list.append(user)
        entities = json_data['entities']

        hashtag_text = []
        hashtags = entities['hashtags']
        for hashtag in hashtags:
            hashtag_text.append(hashtag['text'])
        hashtag_list.append(hashtag_text)

        screen_names = []
        user_mentions = entities['user_mentions']
        for mention in user_mentions:
            screen_names.append(mention['screen_name'])
        mention_list.append(screen_names)

        entities_list.append(entities)

        del json_data['user']
        del json_data['entities']
        json_list.append(json_data)

        json_df = pd.DataFrame(json_list)

        # Note: status list might be empty because we use the Standard Search API which limits our search history to within the past 7 days
        # ---------------------- create a data frame of the list of tweets -----------------------------

        # ---------------------- extract required fields ----------------------------------------------
        json_df = json_df[['id_str','text','retweet_count','favorite_count','created_at','coordinates', 'in_reply_to_screen_name']]

        user_df = pd.DataFrame(user_list)
        hashtag_series = pd.Series(hashtag_list)
        mention_series = pd.Series(mention_list)
        user_df =  user_df[['id_str', 'location', 'screen_name']]
        # entities_df = pd.DataFrame(entities_list)

        json_df['user_id_str'] = user_df['id_str']
        json_df['user_location'] = user_df['location']
        json_df['user_screen_name'] = user_df['screen_name']
        json_df['hashtags'] = hashtag_series
        json_df['mentions'] = mention_series
    #since some tweets mention more than one candidate there will be duplicates
    json_2 = json_df.drop_duplicates(keep = False, subset = "id_str") 
  

    # ---------------------- save as a csv file grouped by candidate while appending new tweets each run  ----------------------------------------------
#print(json_df)
check = json_2['id_str'] == 1180839899731120000
#print(json_2[check])
json_2.to_csv('fulloutput.csv',header = True,mode = 'a')
KamalaHarris = json_2.mentions.str.contains('KamalaHarris',regex = False)
print(KamalaHarris.head())
KamalaHarrisDF= json_2[KamalaHarris]
KamalaHarrisDF.to_csv('Harris.csv',header = True, mode = 'a')
JoeBiden = json_2.mentions.str.contains('JoeBiden',regex = False)
JoeBidenDF = json_2[JoeBiden]
JoeBidenDF.to_csv('Biden.csv',header = True, mode = 'a')
BernieSanders = json_2.mentions.str.contains('BernieSanders',regex = False)
BernieSandersDF = json_2[BernieSanders]
BernieSandersDF.to_csv('Sanders.csv',header = True, mode = 'a')
CoreyBooker = json_2.mentions.str.contains('CoreyBooker',regex = False)
CoreyBookerDF = json_2[CoreyBooker]
CoreyBookerDF.to_csv('Booker.csv',header = True, mode = 'a')
PeteButtigieg = json_2.mentions.str.contains('PeteButtigieg',regex = False)
PeteButtigiegDF = json_2[PeteButtigieg]
PeteButtigiegDF.to_csv('Buttigieg.csv',header = True,mode = 'a')
JulianCastro = json_2.mentions.str.contains('JulianCastro',regex = False)
JulianCastroDF= json_2[JulianCastro]
JulianCastroDF.to_csv('Castro.csv',header = True, mode = 'a')
AmyKlobuchar = json_2.mentions.str.contains('AmyKlobuchar',regex = False)
AmyKlobucharDF = json_2[AmyKlobuchar]
AmyKlobucharDF.to_csv('Klobuchar.csv',header = True, mode = 'a')
BetoORourke = json_2.mentions.str.contains('BetoORourke',regex = False)
BetoORourkeDF = json_2[BetoORourke]
BetoORourkeDF.to_csv('Rourke.csv',header = True, mode = 'a')
TomSteyer = json_2.mentions.str.contains('TomSteyer',regex = False)
TomSteyerDF = json_2[TomSteyer]
TomSteyerDF.to_csv('Steyer.csv',header = True, mode = 'a')
ElizabethWarren = json_2.mentions.str.contains('ElizabethWarren',regex = False)
ElizabethWarrenDF = json_2[ElizabethWarren]
ElizabethWarrenDF.to_csv('Warren.csv',header = True, mode = 'a')
AndrewYang = json_2.mentions.str.contains('AndrewYang',regex = False)
AndrewYangDF = json_2[AndrewYang]
AndrewYangDF.to_csv('Yang.csv',header = True, mode = 'a')

print('done')
