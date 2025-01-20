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



def spimi_indexer(dataset_path):
    index = defaultdict(list)

    # Iterate over all files in the dataset directory
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

index = spimi_indexer(dataset_path)

# Function to perform the boolean retrieval of single, AND, and OR queries
def retrieval(index, query):
    # Splits the query into terms for the AND and OR queries
    terms = query.lower().split()

    # Single-token query
    if len(terms) == 1:
        return set(index.get(terms[0], []))

    elif 'and' in terms:
        terms = [term for term in terms if term != 'and']
        postings_lists = [set(index.get(term, [])) for term in terms]
        return set.intersection(*postings_lists)

    elif 'or' in terms:
        terms = [term for term in terms if term != 'or']
        postings_lists = [set(index.get(term, [])) for term in terms]
        return set.union(*postings_lists)

    # If nothing is specified, use AND
    else:
        postings_lists = [set(index.get(term, [])) for term in terms]
        return set.intersection(*postings_lists)


def print_tokens(query, result):
    print(f"Documents matching '{query}':")
    # Remove duplicates
    result_list = sorted(set(result))

    # Print the results with a line break after every 20 IDs
    for i in range(0, len(result_list), 20):
        print(' '.join(result_list[i:i + 20]))
    print()


queries = [
    "Bush",
    "Reagan or Bush",
    "Glenn and Kuwait"
]

# Print the postings of each query
for query in queries:
    result = retrieval(index, query)
    print_tokens(query, result)