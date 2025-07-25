# Performs the main transformations, extracts sentiments and provides sentiment scores

relevant_words_to_check = ["runs","run","wicket","wickets","catch","catches","scores","score","boundary","boundaries","six","sixes","fours","four","plays","played","play","field","pitch","bounce","pace","thriller","scoring","rate","captaincy","coach","seam","swing","spin","DRS","innings","chase","target","batting","bowling","overcast","conditions","sunny"]

relevant_tags = {
    "match_situation":["thriller", "scoring", "low-scoring", "high-scoring", "overcast", "tough", "changing"]
}

# Check if comment body contains relevant words
def check_if_comment_relevant(comment_body):
    res = any(elem in comment_body for elem in relevant_words_to_check)
    return res


def clean_comments(thread_comments):
    thread_comments = []
    clean_thread_comments = []
    for comment in thread_comments:
        comment_body = comment['body']
        is_relevant = check_if_comment_relevant(comment_body)
        if is_relevant(comment_body):
            clean_thread_comments.append(comment)
        replies_list = comment['replies']
        for reply in replies_list:
            reply_comment_body = reply['body']
            if is_relevant(reply_comment_body):
                clean_thread_comments.append(reply_comment_body)
