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

    # Iterate over all files in the dataset
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

# Print the positional postings list
print_tokens = list(positional_index.keys())[:3]
for token in print_tokens:
    # Sum of all amount of times token appears
    total_frequency = sum(len(positions) for positions in positional_index[token].values())
    print(f"Token: '{token}' (Total Frequency: {total_frequency})")
    for doc_id, positions in positional_index[token].items():
        doc_frequency = len(positions)
        print(f"  Document {doc_id}: Frequency {doc_frequency}, Positions {positions}")