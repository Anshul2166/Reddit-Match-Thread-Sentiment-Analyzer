from datetime import datetime, UTC

import praw
import json

from redditCricketSentimentAnalyzer.resources.flair_to_team import flair_to_team
from redditCricketSentimentAnalyzer.utils.utils import extract_teams_from_title, capitalize, tokenize_flair


# Clean the reddit flair and return the flair
def get_flair(flair, flair_to_team_mapping):
    tokens = tokenize_flair(flair)
    for token in tokens:
        token = capitalize(token)
        if token in flair_to_team_mapping:
            return flair_to_team_mapping[token]
    return 'Neutral'

# Convert comment object to required json format
def get_comment_json(comment, team_a, team_b):
    flair = get_flair(comment.author_flair_text, flair_to_team)
    return {
        "author": str(comment.author) if comment.author else "[deleted]",
        "body": comment.body,
        "created_utc": comment.created_utc,
        "timestamp": datetime.fromtimestamp(comment.created_utc, UTC).isoformat(),
        "actual_flair" : comment.author_flair_text,
        "flair" : flair,
        "context_flair" : flair if flair in (team_a, team_b) else "Neutral" # Will only have flair of teams playing. Any other team would be listed "Neutral"
     }

# Get all replies to top comment in single flat list
def flatten_replies(comment, team_a, team_b):
    # Recursively collect all replies in a flat list
    list_of_replies = []
    for reply in comment.replies:
        if isinstance(reply, praw.models.Comment):
            if reply.body not in ('[removed]', '[deleted]'):
                comment_json = get_comment_json(reply, team_a, team_b)
                list_of_replies.append(comment_json)
            list_of_replies.extend(flatten_replies(reply, team_a, team_b))  # recursively get all replies
    return list_of_replies

def get_comments_for_thread(match_thread_link):
    # Load reddit credentials
    with open('../credentials/reddit_credentials.json', 'r') as file:
        data = json.load(file)

    reddit = praw.Reddit(
        client_id=data['REDDIT_CLIENT_ID'],
        client_secret=data['REDDIT_SECRET'],
        user_agent=data['REDDIT_USER_AGENT']
    )

    # Fetch the submission object for given match thread
    submission = reddit.submission(url=match_thread_link)

    # Get the list of two teams playing
    title = submission.title
    team_a, team_b = extract_teams_from_title(title)
    print("Team A:", team_a)
    print("Team B:", team_b)

    # Sort the comment by New
    submission.comment_sort = "new"

    # Get all nested replies
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    print("Got all comments:", len(all_comments))

    # Build list with top-level comment + all replies in single flat list
    thread_comments = []

    # Iterate over all submission comments
    for top_level in submission.comments:
        if top_level.body not in ('[removed]', '[deleted]'):
            # Valid top-level comment
            top_data = get_comment_json(top_level)
            replies_flat = flatten_replies(top_level, team_a, team_b)
            top_data["replies"] = replies_flat
            if top_data:
                thread_comments.append(top_data)
        else:
            # Skip top-level, but promote replies
            replies_list = flatten_replies(top_level, team_a, team_b)
            if replies_list:
                thread_comments.append(replies_list)

    # Flatten the replies to single extended list
    flattened_list_of_comments = []
    for comment in thread_comments:
        # If comment is list, it means the top-level comment was deleted (by author) and only replies remained
        if type(comment) is list:
            flattened_list_of_comments.extend(comment)
        # Top level comment isn't deleted
        else:
            replies_list = comment['replies']
            del comment['replies']
            flattened_list_of_comments.append(comment)
            if replies_list:
                flattened_list_of_comments.extend(replies_list)

    # Save to a file named 'comments.json' (This is for development phase only)
    with open('comments.json', 'w', encoding='utf-8') as f:
        json.dump(flattened_list_of_comments, f, indent=2, ensure_ascii=False)

    print("Finished writing comments.json")

match_thread_link = "https://www.reddit.com/r/Cricket/comments/1lynujm/match_thread_3rd_test_england_vs_india_day_4/"
get_comments_for_thread(match_thread_link)