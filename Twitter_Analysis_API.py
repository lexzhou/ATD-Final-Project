### Import the libraries and adequate setting
### The output

from deep_translator import GoogleTranslator
import tweepy as tw               # API of tweeter
import re                         # Regular expression
import itertools
import collections
import nltk                       # Natural Language Toolkit library (stopwords and bigrams)
from nltk.corpus import stopwords # Import the set of stopwords

consumer_key= 'wwIXVkskBYuCtiHXsPiy7OGNR'
consumer_secret= 'eNHxydGwAUPbvjkku1hYyQNflZAn80CAbBnixtt68j4Rvug6LJ'
access_token= '1347667572595040256-kxlChS2G6uE0arYcm2ujHmD5vbgmq0'
access_token_secret= '0FKZyO4dy9lBr1P8fU23uiTE0Bm4L2TFfl803JtUW9NG7'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
### Import the libraries and adequate setting
### Function to remove the URLs of the tweets that we will use later
def remove_url(txt):
    """
    We use regular expressions by using re library to eliminate URLs (links) that the tweets contained and replace 
    those URLs with " " by using method sub() of re package.
    """
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())  

def treding_topic(search_topic,idiom, N=100, M=30):
    """
    search_topic --> The treding topic that users are interested in
    N --> Number of tweets (the default is 100)
    M --> The number of words that have higher frequency (the default is 30).
    """
    try:
        ### Obtain N tweets related to "search_topic" in a list
        search_term = f"#{search_topic} -filter:retweets" # And exclude the retweets (转发)
        tweets = tw.Cursor(api.search,
                           q=search_term,
                           lang=idiom).items(N)            # The language can be selected as english or spanish
        all_tweets = [tweet.text for tweet in tweets]     # Obtain the tweets in text format
        
    except:     
        raise ValueError('Topic introduced not found')
    
    if len(all_tweets)==0:
        raise ValueError('Not Acceptable, no tweet related to selected topic is published')
        
    ### Eliminate the URLs by utilizing the function remove_url()
    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls] # Create a list of lists and tranform into lower case
    
    ### obtain the stopwords (english&spanish) with nltk library
    stop_words = set(stopwords.words('english')).union(set(stopwords.words('spanish')))  # the stop words are lower case, thus we have to make sure the words are lowercase

    ### Eliminate stop words from each tweet list of words
    tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                  for tweet_words in words_in_tweet]

    ###################################
    ###         WORD COUNT          ###
    ###################################
    # flatten all the lists that are contained insede the list tweets_nsw into one single list
    all_words_nsw = list(itertools.chain(*tweets_nsw))

    # Use a Counter to return the number of ocurrence of each word and select the M most common words among N tweets.
    counts_nsw = collections.Counter(all_words_nsw)
    words_most_common = counts_nsw.most_common(M)     # This will be one of the output of the flask!!!
    resul1 = dict(words_most_common)                  # Convert the data into dictionary structure as a JSON output.        
        
    ###################################
    ###            BIGRAM           ###
    ###################################
    # Create list of lists that contain bigrams in tweets
    terms_bigram = [list(nltk.bigrams(tweet)) for tweet in tweets_nsw]
    # Flatten list of bigrams in clean tweets
    bigrams = list(itertools.chain(*terms_bigram))

    # Create counter of words in clean bigrams
    bigram_counts = collections.Counter(bigrams)
    bigram_counts = bigram_counts.most_common(M)

    # Transform into a json-like object
    resul2 = {}
    for word_tuple, count in bigram_counts:
        text = word_tuple[0] + ' ' + word_tuple[1]
        resul2[text] = count
        
    return resul1, resul2

def user_tweets(userID,idiom, N=100, M=30):
    try:
        if N <= 200:     # Because 200 is the maximum amount for the following method
            tweets = api.user_timeline(screen_name=userID, 
                                   count=N,
                                   include_rts = False,    # Exclude retweets
                                   tweet_mode = 'extended' # To keep full_text 
                                   )
            
        else:            # We use the following method to run iteratively until N tweets of a user (maximum is 3200)
            tweets = []
            for status in tw.Cursor(api.user_timeline, screen_name=userID, tweet_mode="extended",lang=idiom).items():
                tweets.append(status)
                if len(tweets) >= N:
                    break
    except:
        raise ValueError('Incorrect userID introduced, authorization refused')

    if len(tweets)>0:
        all_tweets = [tweet.full_text for tweet in tweets]     # Obtain the tweets in text format (.full_text)

        ### Eliminate the URLs by utilizing the function remove_url()
        all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
        words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls] # Create a list of lists and tranform into lower case

        ### obtain the stopwords (english&spanish) with nltk library
        stop_words = set(stopwords.words('english')).union(set(stopwords.words('spanish')))  # the stop words are lower case, thus we have to make sure the words are lowercase

        ### Remove stop words from each tweet list of words
        tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                          for tweet_words in words_in_tweet]
        
        ###################################
        ###         WORD COUNT          ###
        ###################################
        # flatten all the lists that are contained insede the list tweets_nsw into one single list
        all_words_nsw = list(itertools.chain(*tweets_nsw))

        # Use a Counter to return the number of ocurrence of each word and select the M most common words among N tweets.
        counts_nsw = collections.Counter(all_words_nsw)
        words_most_common = counts_nsw.most_common(M)     # This will be one of the output of the flask!!!
        resul1 = dict(words_most_common)       # Convert the data into dictionary structure as a JSON output.        
        
        ###################################
        ###            BIGRAM           ###
        ###################################
        # Create list of lists containing bigrams in tweets
        terms_bigram = [list(nltk.bigrams(tweet)) for tweet in tweets_nsw]
        # Flatten list of bigrams in clean tweets
        bigrams = list(itertools.chain(*terms_bigram))

        # Create counter of words in clean bigrams
        bigram_counts = collections.Counter(bigrams)
        bigram_counts = bigram_counts.most_common(M)

        # Transform the bigram
        resul2 = {}
        for word_tuple, count in bigram_counts:
            text = word_tuple[0] + ' ' + word_tuple[1]
            resul2[text] = count
        return resul1, resul2
    
    else:
        raise ValueError('Not Acceptable, the userID does not have any tweets published')
        

class Spanish_Dict:
    """
    Obtain the a diccionary about the Spanish definitions of a word or a list of words.
    """
    def buscar(self, elem, num_def):
        if isinstance(elem, str):               
            return self._buscar(elem, num_def)
        elif isinstance(elem, list): 
            # Our API always executes this condition
            return {i[0]:self._buscar(i[1], num_def) for i in elem} 
        else:
            return None

    def _buscar(self, elem, num_def):   
        # Find the definitino of each word in RAE by using webscraping technique (re and bs4 package)
        import requests as rq
        from bs4 import BeautifulSoup as bs
        busqueda = rq.get("https://dle.rae.es/"+elem)
        soup=bs(busqueda.content,"lxml")
        return [elem.text for elem in soup.find_all("p", class_='j')][:num_def]

class English_Dict:
    """
    Obtain the a diccionary about the English definitions of a word or a list of words.
    """
    def search(self, elem, num_def):
        if isinstance(elem, str):
            return self._search(elem,num_def)
        elif isinstance(elem, list):
            # Our API always executes this condition
            return {i[0]:self._search(i[1],num_def) for i in elem}
        else:
            return None
    
    def _search(self, elem, num_def):
        from PyDictionary import PyDictionary   # Extract the word's English definitions from PyDictionary package
        i, res = 0, []
        try:            
            for key, values in PyDictionary().meaning(elem, disable_errors=True).items():
                for value in values:
                    res.append(str(i+1)+'. '+key+'. '+value)
                    i+=1
                    if i==num_def:
                        return res
        except:
            return res
    
def juntar_info(dicc_rep,dicc_def):
    # Merge the word's frequency dictionary and bigram's frequency dictionary
    dicc={}
    for palabra in dicc_rep:
        dicc[palabra]={'recurrence':dicc_rep[palabra], 'definitions':dicc_def[palabra]}
    return dicc


#####################
### Build out API ###
#####################
from flask import Flask, jsonify, request, abort   # The necessary methods
from dicttoxml import dicttoxml                    # To trasform JSON object into XML object

app = Flask(__name__)

### Our Twitter Analysis API currently have two accessible resource (one to get informations of a treding topic, another gets informatino of a particular user)
@app.route("/api/topic/<topic>", methods=['GET'])  ### The first resource is /api/topic/<topic> where topic is a treding topic specified by user
def getTopic(topic):
    '''
    Obtain the M most frequent words along with their definitions (Spanish or English) 
    among N tweets related to a specific topic
    '''
    idiom=None
    N = 100     # Number of tweets to analyze by default, 100 
    D = 3       # Number of denifitions for each word by default, 3
    M = 10      # Number of most frequent words and bigrams to return by default, 10
    for l in re.split(' |,',request.headers['Accept-Language']): # Extract the first valid language specified by the user in order to work with the proper language if it is possible 
        if l=='es' or l=='en':   # See if the language required by user is English or Spanish (If it is not the previous two, the program returns Spanish by default)
            idiom=l
            break
    ### Read the parameters given by the user
    for key, value in request.args.items():
        if key == 'N':
            try:
                N = int(value)  # Number of tweets to analyze
            except:
                pass
        elif key =='M':
            try:
                M = int(value)  # Number of most frequent words and bigrams to extract
            except:
                pass
        elif key == 'D':        # Number of definitions for each word (as maximum)
            try:
                D = int(value)  # Number of definitions for each word (as maximum)
            except:
                pass
            
    ### Parse information in Spanish    
    if idiom is None or idiom=='es':
        dicc = Spanish_Dict()
        try:
            dicc_topic, dicc_b = treding_topic(topic,'es', N, M)  # Parse the M most frequent words among N tweets.
        except:
            abort(404,'Topic Not Found')  # If the topic does not exist, raise an error and include 404 to the response HTTP message for user
        dicc_w = dicc.buscar([(i,GoogleTranslator(source='auto', target='es').translate(i+' ')) for i in dicc_topic.keys()],D)  # Obtain D Spanish definitions for each word
        
    ### Parse information in English
    else:
        dicc = English_Dict()
        try:
            dicc_topic, dicc_b = treding_topic(topic,'en', N, M) 
        except:
            abort(404,'Topic Not Found') 
        dicc_w = dicc.search([(i,GoogleTranslator(source='auto', target='en').translate(i+' ')) for i in dicc_topic.keys()],D)  # Obtain D English definitions for each word

        
    info = juntar_info(dicc_topic,dicc_w)    # Merge the dictioniaries of most frequent words and bigrams as output (JSON object)
    res = {'words':info, 'bigrams':dicc_b}
    if 'Content-Type' in request.headers: 
        if request.headers['Content-Type']=='text/xml': 
            # Transmute the output into XML object if it is required by user
            return dicttoxml(res)
    return jsonify(res) # If no XML was required, send as JSON object


@app.route("/api/user/<user>", methods=['GET'])  ### The second resource in our API is /api/user/<user> where user is the userID of a specific twitter user specified by user
def getUser(user):
    '''
    Obtain the M most frequent words along with their definitions (Spanish or English) 
    among N tweets published by a particular user
    '''
    idiom=None
    N = 100     # Number of tweets to analyze by default, 100 
    D = 3       # Number of denifitions for each word by default, 3
    M = 10      # Number of most frequent words and bigrams to return by default, 10
    for l in re.split(' |,|-',request.headers['Accept-Language']):   # Extract the first valid language specified by the user in order to work with the proper language if it is possible 
        if l=='es' or l=='en':   # See if the language required by user is English or Spanish (If it is not the previous two, the program returns Spanish by default)
            idiom=l
            break
    for key, value in request.args.items():
        if key == 'N':
            try:
                N = int(value)  # Number of tweets to analyze
            except:
                pass
        elif key =='M':
            try:
                M = int(value)  # Number of most frequent words and bigrams to extract
            except:
                pass
        elif key == 'D':        
            try:
                D = int(value)  # Number of definitions for each word (as maximum)
            except:
                pass
    ### Parse information in Spanish 
    if idiom is None or idiom=='es': 
        dicc = Spanish_Dict()
        try:
            dicc_user, dicc_b = user_tweets(user,'es',N,M) # Parse the M most frequent words among N tweets.
        except:
            abort(404, 'User not found')                   # If the user does not exist, abort an error and include 404 to the response HTTP message for user
        dicc_w = dicc.buscar([(i,GoogleTranslator(source='auto', target='es').translate(i+' ')) for i in dicc_user.keys()],D)# Obtain D Spanish definitions for each word
    else:
        dicc = English_Dict() 
        try:
            dicc_user, dicc_b = user_tweets(user,'en',N,M) # Parse the M most frequent words among N tweets.
        except:
            abort(404, 'User not found') 
        dicc_w = dicc.search([(i,GoogleTranslator(source='auto', target='en').translate(i+' ')) for i in dicc_user.keys()], D) # Obtain D English definitions for each word
    info = juntar_info(dicc_user,dicc_w)    # Merge the dictioniaries of most frequent words and bigrams as output (JSON object)
    res = {'words':info, 'bigrams':dicc_b}
    if 'Content-Type' in request.headers: 
        if request.json['Content-Type']=='text/xml':
             # Transmute the output into XML object if it is required by user
            return dicttoxml(res)
    return jsonify(res) # If no XML was required, send as JSON object

app.run(port=8080) # Run the API in port 8080