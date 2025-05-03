import os
from dotenv import load_dotenv
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- Load environment variables ---
load_dotenv(dotenv_path=".env")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# --- Debug: check if token loaded ---
if not BEARER_TOKEN:
    raise Exception("❌ Bearer Token not found. Check your .env file!")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

query = "Tesla stock -is:retweet lang:en"

# --- Fetch Tweets ---
try:
    response = client.search_recent_tweets(query=query, max_results=50)
    tweets_data = response.data
    if not tweets_data:
        print("⚠️ No tweets found for the given query.")
        exit()
except tweepy.errors.Unauthorized as e:
    print("❌ Unauthorized: Invalid or expired Bearer Token.")
    exit()
except Exception as e:
    print(f"❌ Error fetching tweets: {e}")
    exit()

# --- Extract text and analyze sentiment ---
tweets = [tweet.text for tweet in tweets_data]
polarities = [TextBlob(text).sentiment.polarity for text in tweets]

# --- Display tweets with sentiment scores ---
for i, (text, score) in enumerate(zip(tweets, polarities)):
    print(f"\nTweet {i+1}: {text}\nSentiment Score: {score:.3f}")

# --- Plot the sentiment scores ---
plt.plot(polarities, marker='o')
plt.title("📈 Sentiment Polarity of Recent Tweets about Tesla")
plt.xlabel("Tweet Index")
plt.ylabel("Polarity (-1 to 1)")
plt.grid(True)
plt.tight_layout()
plt.show()
