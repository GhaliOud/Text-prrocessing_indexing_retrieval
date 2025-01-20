import os
import re
import nltk
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer

# nltk.download('punkt')

# Path to the Reuters-21578 dataset
dataset_path = r'C:\Users\21265\Desktop\.School Stuff\Uni\25Fall\Comp 479\p1\Python\reuters21578'

# Function to extract articles, headlines, and DocIDs
def extract_text(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()

        # Extract each document making sure to find the document ID inside the <Reuters> tags
        documents = re.findall(r'<REUTERS[^>]*?NEWID="(\d+)"[^>]*?>(.*?)</REUTERS>', content, re.DOTALL)

        doc_data = []

        for doc_id, document in documents:
            # Extract headline and body for each document
            headline_match = re.search(r'<TITLE>(.*?)</TITLE>', document, re.DOTALL)
            article_match = re.search(r'<BODY>(.*?)</BODY>', document, re.DOTALL)

            if headline_match and article_match:
                headline = headline_match.group(1)
                article = article_match.group(1)
                doc_data.append((doc_id, headline, article))

        return doc_data

# A nltk tokenizer to exclude punctuation
tokenizer = RegexpTokenizer(r'\w+')

def tokenize_text(text):
    # Convert text to lowercase and tokenize using the RegexpTokenizer, removing all punctuation in text
    return tokenizer.tokenize(text.lower())

# SPIMI-inspired positional indexer
def positional_indexer(dataset_path):
    index = defaultdict(lambda: defaultdict(list))

    # Iterate over all files in the dataset directory
    for file_name in os.listdir(dataset_path):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(dataset_path, file_name)
            doc_data = extract_text(file_path)

            # Tokenize the extracted headlines and articles
            for doc_id, headline, article in doc_data:
                tokens = tokenize_text(headline + " " + article)

                # Append tokens to index
                for position, token in enumerate(tokens):
                    index[token][doc_id].append(position)

    return index

# Function for NEAR queries
def near_query(positional_index, token1, token2, k):
    result_docs = set()

    # Convert terms to lowercase
    token1 = token1.lower()
    token2 = token2.lower()

    if token1 in positional_index and token2 in positional_index:
        for doc_id in positional_index[token1]:
            if doc_id in positional_index[token2]:
                positions1 = positional_index[token1][doc_id]
                positions2 = positional_index[token2][doc_id]

                # Check if any positions are within k tokens
                for pos1 in positions1:
                    for pos2 in positions2:
                        if abs(pos1 - pos2) <= k:
                            result_docs.add(doc_id)
                            break

    return result_docs

# Create the positional index
positional_index = positional_indexer(dataset_path)

# Example NEAR query
token1 = "Reagan"
token2 = "War"
k = 5
result = near_query(positional_index, token1, token2, k)
print(f"Documents where '{token1}' is within {k} tokens of '{token2}': {sorted(result)}")