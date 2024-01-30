import tweepy
import openai
from datetime import datetime
import numpy as np 
#from sklearn.metrics.pairwise import cosine_similarity

# Twitter API v2 credentials
BEARER_TOKEN = 'YOUR_BEARER_TOKEN'

# Initialize OpenAI Client
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
openai.api_key = OPENAI_API_KEY

# Initialize Tweepy Client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Function to read keywords from a file
def read_keywords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Define keywords for blocking
red_words = read_keywords('red_words.txt')#['keyword1', 'keyword2', 'keyword3']
yellow_phrases = read_keywords('yellow_phrases.txt')#['phrase one', 'phrase two', 'phrase three']

# Cache for storing checked phrases to avoid redundant API calls
checked_phrases_cache = {}

# Example phrases for semantic comparison, we will need to tune the threshold for sensitivity
# yellow_phrases = ['i hate the detroit lions', 'astronomy isn\'t cool', 'andrew tate']

# Example tweet texts
# example_tweets = [
#     "Really dislike those Detroit players",  # Semantically similar to 'i hate the detroit lions'
#     "Studying stars is so boring",           # Semantically similar to 'astronomy isn\'t cool'
#     "That guy West is really controversial"  # Semantically similar to 'kanye west', might need to make positive/negative semantic association buckets
# ]

def is_semantically_similar(tweet_text, phrases):
    for phrase in phrases:
        # Check cache first
        if (tweet_text, phrase) in checked_phrases_cache:
            return checked_phrases_cache[(tweet_text, phrase)]

        response = openai.Completion.create(
            model="text-embedding-ada-002",
            prompt=f"Tweet: '{tweet_text}'\nPhrase: '{phrase}'\nIs the tweet semantically similar to the phrase? (Yes or No)",
            temperature=0,
            max_tokens=1
        ) 
        similarity_answer = response.choices[0].text.strip().lower()
        checked_phrases_cache[(tweet_text, phrase)] = (similarity_answer == 'yes')
        if similarity_answer == 'yes':
            return True
    return False

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return np.array(response['data'][0]['embedding'])

def semantic_cosine_similarity(tweet_text, phrases, threshold=0.5):
    tweet_embedding = get_embedding(tweet_text)
    
    for phrase in phrases:
        # Check cache first
        if (tweet_text, phrase) in checked_phrases_cache:
            similarity_score = checked_phrases_cache[(tweet_text, phrase)]
        else:
            phrase_embedding = get_embedding(phrase)
            #similarity_score = cosine_similarity([tweet_embedding], [phrase_embedding])[0][0]
            #checked_phrases_cache[(tweet_text, phrase)] = similarity_score

        if similarity_score > threshold:
            return True
    return False

def handle_tweet(tweet):
    tweet_text = tweet.text.lower()

    # Check for red keywords and yellow phrases directly
    if any(keyword in tweet_text for keyword in red_words) or \
       any(phrase in tweet_text for phrase in yellow_phrases):
        block_user(tweet)
    else:
        # Perform semantic similarity check only if direct checks do not match
        if is_semantically_similar(tweet_text, yellow_phrases):
            block_user(tweet)

def block_user(tweet):
    try:
        # Block the user
        client.block(tweet.author_id)
        print(f'Blocked user: {tweet.author_id}')

        # Log the blocked user's ID, timestamp, and tweet text to a file
        with open('blocked_users_log.txt', 'a') as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f'Timestamp: {timestamp}, User ID: {tweet.author_id}, Tweet: {tweet.text}\n')
    except tweepy.TweepError as e:
        print(f'Error occurred: {e}')


class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        # Check if tweet is a reply or quote tweet to @player1
        if tweet.referenced_tweets is not None and any(rt.type in ["replied_to", "quoted"] for rt in tweet.referenced_tweets):
            handle_tweet(tweet)

# Create StreamListener instance
listener = MyStreamListener(bearer_token=BEARER_TOKEN)

# Adding rules to filter the stream
rule = tweepy.StreamRule(value="@player1")
listener.add_rules(rule, dry_run=False)

# Start streaming
listener.filter()
