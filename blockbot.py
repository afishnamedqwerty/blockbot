import tweepy

# Twitter API v2 credentials
BEARER_TOKEN = 'YOUR_BEARER_TOKEN'

# Initialize Tweepy Client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Define keywords for blocking
red_keywords = ['keyword1', 'keyword2', 'keyword3']
yellow_phrases = ['phrase one', 'phrase two', 'phrase three']

class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        # Check if tweet is a reply or quote tweet to @player1
        if tweet.referenced_tweets is not None and any(rt.type in ["replied_to", "quoted"] for rt in tweet.referenced_tweets):
            tweet_text = tweet.text.lower()

            # Check for red keywords and yellow phrases
            if any(keyword in tweet_text for keyword in red_keywords) or \
               any(phrase in tweet_text for phrase in yellow_phrases):
                try:
                    # Block the user
                    client.block(tweet.author_id)
                    print(f'Blocked user: {tweet.author_id}')
                except tweepy.TweepError as e:
                    print(f'Error occurred: {e}')

# Create StreamListener instance
listener = MyStreamListener(bearer_token=BEARER_TOKEN)

# Adding rules to filter the stream
rule = tweepy.StreamRule(value="@player1")
listener.add_rules(rule, dry_run=False)

# Start streaming
listener.filter()
