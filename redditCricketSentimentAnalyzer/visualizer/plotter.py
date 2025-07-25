from datetime import timedelta

import matplotlib.pyplot as plt

def plot(df, time_scale, sentiment_scale, team_column):

    # Find the earliest time_bucket
    start_time = df[time_scale].min()

    # Set end time to 15 hours later
    end_time = start_time + timedelta(hours=10)

   # Filter the dataframe to only contain data between start and end time
    filtered = df[(df[time_scale] >= start_time) & (df[time_scale] <= end_time)].copy()

    # Convert to YYYY-MM-DD HH:MM format for better readability
    filtered["formatted_time"] = filtered[time_scale].dt.strftime("%Y-%m-%d %H:%M")

    # Create a line for each team
    teams = filtered[team_column].unique()

    # For each group, smooth the sentiment over a 3-point rolling window
    filtered["smoothed_sentiment"] = filtered.groupby(team_column)[sentiment_scale].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean())

    # Prepare the plot with given size
    plt.figure(figsize=(20, 15))

    # For each team, plot the sentiment
    for team in teams:
        team_df = filtered[filtered[team_column] == team]
        plt.plot(team_df["formatted_time"], team_df["smoothed_sentiment"], label=team)

    # Labels and title
    plt.xlabel("Time")
    plt.ylabel("Average Sentiment")
    plt.title("Sentiment Timeline by Team")
    plt.legend(title="Team")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()