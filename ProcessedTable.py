import os
import re
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

# nltk.download('punkt')
# nltk.download('stopwords')

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

# Function to tokenize and preprocess text in the 4 different techniques
def preprocess_text(text, case_fold=False, remove_numbers=False, remove_stopwords=False, apply_stemming=False):
    # A nltk tokenizer to exclude punctuation
    tokenizer = RegexpTokenizer(r'\w+')

    # Convert text to lowercase if case_fold is True
    if case_fold:
        text = text.lower()

    tokens = tokenizer.tokenize(text)
    # Remove numbers if remove_numbers is True
    if remove_numbers:
        tokens = [token for token in tokens if not token.isdigit()]

    # Remove stop words if remove_stopwords is True
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

    # Apply stemming if apply_stemming is True
    if apply_stemming:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]

    return tokens

# SPIMI-inspired preprocessed indexer
def preprocessed_indexer(dataset_path, case_fold=False, remove_numbers=False, remove_stopwords=False, apply_stemming=False):
    index = defaultdict(lambda: defaultdict(list))

    # Iterate over all files in the dataset directory
    for file_name in os.listdir(dataset_path):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(dataset_path, file_name)
            doc_data = extract_text(file_path)

            # Tokenize and preprocess the extracted headlines and articles
            for doc_id, headline, article in doc_data:
                tokens = preprocess_text(headline + " " + article, case_fold, remove_numbers, remove_stopwords, apply_stemming)

                # Append tokens to index
                for position, token in enumerate(tokens):
                    index[token][doc_id].append(position)

    return index

# Function to count or sum up the main 3 variables, Distinct Terms, Nonpositional Postings, and total Tokens
def compile_statistics(index):
    distinct_terms = len(index)
    nonpositional_postings = sum(len(docs) for docs in index.values())
    tokens = sum(len(positions) for docs in index.values() for positions in docs.values())
    return distinct_terms, nonpositional_postings, tokens

# Run the indexer depending on the compression technique
unfiltered_index = preprocessed_indexer(dataset_path)
no_numbers_index = preprocessed_indexer(dataset_path, remove_numbers=True)
case_folding_index = preprocessed_indexer(dataset_path, case_fold=True)
stop_words_index = preprocessed_indexer(dataset_path, remove_stopwords=True)
stemming_index = preprocessed_indexer(dataset_path, apply_stemming=True)

# Print the table
print(f"{'Preprocessing Step':<20}{'Distinct Terms':<20}{'Nonpositional Postings':<25}{'Tokens':<20}")
print(f"{'Unfiltered':<20}{compile_statistics(unfiltered_index)[0]:<20}{compile_statistics(unfiltered_index)[1]:<25}{compile_statistics(unfiltered_index)[2]:<20}")
print(f"{'No Numbers':<20}{compile_statistics(no_numbers_index)[0]:<20}{compile_statistics(no_numbers_index)[1]:<25}{compile_statistics(no_numbers_index)[2]:<20}")
print(f"{'Case Folding':<20}{compile_statistics(case_folding_index)[0]:<20}{compile_statistics(case_folding_index)[1]:<25}{compile_statistics(case_folding_index)[2]:<20}")
print(f"{'Stop Words':<20}{compile_statistics(stop_words_index)[0]:<20}{compile_statistics(stop_words_index)[1]:<25}{compile_statistics(stop_words_index)[2]:<20}")
print(f"{'Stemming':<20}{compile_statistics(stemming_index)[0]:<20}{compile_statistics(stemming_index)[1]:<25}{compile_statistics(stemming_index)[2]:<20}")