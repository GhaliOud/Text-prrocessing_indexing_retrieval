import nltk
import os
import re

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

# Function to tokenize text
def tokenize_text(text):
    return nltk.word_tokenize(text)


# Iterate over all files in the dataset
for file_name in os.listdir(dataset_path):
    if file_name.endswith('.sgm'):
        file_path = os.path.join(dataset_path, file_name)
        print(f"Processing file: {file_path}")
        doc_data = extract_text(file_path)

        # Tokenize the extracted headlines and articles
        for doc_id, headline, article in doc_data:
            headline_tokens = tokenize_text(headline)
            article_tokens = tokenize_text(article)

            # Print document ID with their respective tokens
            print(f"DocID {doc_id}: Headline Tokens: {headline_tokens}")
            print(f"DocID {doc_id}: Article Tokens: {article_tokens}\n")
