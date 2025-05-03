import streamlit as st
import os
from dotenv import load_dotenv
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# --- Load environment variables ---
load_dotenv(dotenv_path=".env")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# --- Debug: check if token loaded ---
if not BEARER_TOKEN:
    st.error("❌ Bearer Token not found. Check your .env file!")
    st.stop()

client = tweepy.Client(bearer_token=BEARER_TOKEN)
analyzer = SentimentIntensityAnalyzer()

# StreamLit UI
st.title("📊 Stock Sentiment Analyzer (Live Tweets)")
stock = st.text_input("Enter a stock keyword (e.g., Tesla, Nvidia, Apple)", value="Tesla")

if st.button("Analyze Sentiment"):
    with st.spinner("Fetching and analyzing tweets..."):
        query = f"{stock} stock -is:retweet lang:en"
        try:
            response = client.search_recent_tweets(query=query, max_results=50)
            tweets_data = response.data
            if not tweets_data:
                st.warning("⚠️ No tweets found.")
                st.stop()
        except Exception as e:
            st.error(f"❌ Twitter API error: {e}")
            st.stop()

        tweets = [tweet.text for tweet in tweets_data]
        scores = [analyzer.polarity_scores(text)['compound'] for text in tweets]

        # Plot sentiment trend
        st.subheader("📉 Sentiment Trend")
        st.line_chart(scores)

        # Show top tweets
        sorted_tweets = sorted(zip(tweets, scores), key=lambda x: x[1])
        st.subheader("🔻 Most Negative Tweets")
        for t, s in sorted_tweets[:3]:
            st.markdown(f"**{s:.3f}** — {t}")

        st.subheader("🔺 Most Positive Tweets")
        for t, s in sorted_tweets[-3:]:
            st.markdown(f"**{s:.3f}** — {t}")