# This aggregates the comments/sentiments across fixed time intervals
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from redditCricketSentimentAnalyzer.visualizer.plotter import plot

# For a text, generate a sentiment score
def get_sentiment(text, analyzer):
    return analyzer.polarity_scores(text)["compound"]

def aggregate_comments(comments, time_window_in_minutes = 15):
    # Sort the comment thread as per creating timestamp
    comments.sort(key = lambda c: c['created_utc'])

    # Create a pandas dataframe
    df = pd.DataFrame(comments)

    # Convert UNIX to datetime
    df['timestamp'] = pd.to_datetime(df['created_utc'], unit='s', utc=True)

    # Round down to the nearest minute
    df['time_bucket'] = df['timestamp'].dt.floor(str(time_window_in_minutes)+'min')

    analyzer = SentimentIntensityAnalyzer()

    # Generate the sentiment from comment body
    df["sentiment"] = df["body"].apply(lambda text: get_sentiment(text, analyzer))

    # Get team from context_flair (team A, team B or neutral)
    df["team"] = df["context_flair"]

    # Group the dataframe as per time_bucket and team to find mean sentiment
    grouped_team = df.groupby(["time_bucket", "team"])["sentiment"].mean().reset_index()

    # Plot the graph
    plot(grouped_team, "time_bucket", "sentiment", "team")

with open("../testing_folder/comments.json","r", encoding="utf-8") as f:
    comments_json = json.load(f)

aggregate_comments(comments_json)