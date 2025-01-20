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

# Create the positional index
positional_index = positional_indexer(dataset_path)


# Function for Concordance
def concordance(index, query, k):
    results = []
    query = query.lower()

    # Check if query exists in the index
    if query in index:
        # Iterate over each document where query appears
        for doc_id, positions in index[query].items():
            # Retrieve all tokens for the documents
            doc_tokens = []
            for token, docs in index.items():
                if doc_id in docs:
                    for pos in docs[doc_id]:
                        doc_tokens.append((pos, token))

            # Sort tokens by position
            doc_tokens.sort()

            # Calculate the start and end positions for the context for each position
            for position in positions:
                start = max(0, position - k)
                end = position + k + 1

                # Extract the tokens that appear before and after the query string
                context = [token for pos, token in doc_tokens if start <= pos < end]
                left_context = context[:k]
                right_context = context[k + 1:]

                # Format the result with the query string aligned vertically
                result = f"{doc_id:<10} {' '.join(left_context):>80} | {query:^30} | {' '.join(right_context)}"
                results.append(result)

    # Print the Concordance
    for result in results:
        print(result)


query_string = "climate"
k = 10
concordance(positional_index, query_string, k)