import re

def extract_teams_from_title(title):
    # Basic pattern for "Team A vs Team B"
    match = re.search(r'([A-Za-z ]+?)\s+vs\.?\s+([A-Za-z ]+)', title, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, None

# Capitalise the first letter of the word
def capitalize(str):
    return str[0].upper() + str[1:].lower()

def tokenize_flair(flair):
    if not flair:
        return []
        # Remove emoji shortcodes like :Womens_CWC:
    flair = re.sub(r':[a-zA-Z0-9_]+:', ' ', flair)
    # Replace colons and underscores with space
    flair = re.sub(r'[:_]', ' ', flair)
    # Remove extra whitespace and lowercase
    tokens = flair.lower().split()
    return tokens


def clean_flair_text(flair: str) -> str:
    if not flair:
        return ''
    # Remove emoji-style shortcodes like :India: or :trophy:
    flair = re.sub(r':[a-zA-Z0-9_]+:', '', flair)
    # Remove extra whitespace
    return capitalize(flair.strip())