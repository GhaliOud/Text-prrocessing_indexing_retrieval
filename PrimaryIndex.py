import os
import re
import nltk
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer

# nltk.download('punkt')

# Path to the Reuters-21578 dataset
dataset_path = r'C:\Users\21265\Desktop\.School Stuff\Uni\25Fall\Comp 479\p1\Python\reuters21578'

# Function to extract the article and headline texts, and their respective DocIDs
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

def tokenize_text(text):
    return nltk.word_tokenize(text)

# SPIMI-inspired indexer
def spimi_indexer(dataset_path):
    index = defaultdict(list)

    # Iterate over all files in the dataset
    for file_name in os.listdir(dataset_path):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(dataset_path, file_name)
            doc_data = extract_text(file_path)

            # Tokenize the extracted headlines and articles
            for doc_id, headline, article in doc_data:
                tokens = tokenize_text(headline + " " + article)

                # Append tokens to index
                for token in tokens:
                    if doc_id not in index[token]:
                        index[token].append(doc_id)

    return index


# Create the index
index = spimi_indexer(dataset_path)

# Retrieve and print the postings lists
print_tokens = list(index.keys())[0:13]
for token in print_tokens:
    print(f"Postings list for '{token}': {index[token]}")