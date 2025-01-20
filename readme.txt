--README--

1. **Set Up Your Environment**
   - Ensure Python is installed on your machine (Python 3.7 or higher).
   - Install required Python packages using the following commands:

     ```bash
     pip install nltk
     pip install regex
     ```

   - Download the NLTK resources by running:
     ```python
     import nltk
     nltk.download('punkt')
     nltk.download('stopwords')
     ```

2. **Prepare the Dataset**
   - Download the **Reuters-21578** dataset (you can find it at [this link](https://kdd.ics.uci.edu/databases/reuters21578/reuters21578.html)).
   - Extract the dataset and locate the `.sgm` files.
   - **Important**: Update the `dataset_path` variable in the script to point to the directory where the Reuters dataset `.sgm` files are located. 
   
     Example: 
     ```python
     dataset_path = r'C:\path\to\reuters21578\folder'
     ```
     Make sure to use the correct absolute path to the folder containing the `.sgm` files (you can copy the path from your file explorer and paste it in the script).

3. **Run the Scripts**
   - Open the project in a Python IDE such as VSCode or PyCharm.
   - Execute the script to create and evaluate the SPIMI-inspired positional and preprocessed indexes.

4. **Available Features and Outputs**
   - **Positional Indexing:**
     - Extracts tokens and positions from the headlines and body text, building a positional index.
     - Supports NEAR queries that find documents where two tokens appear within a given number of positions.
     - Example NEAR query:
       ```python
       token1 = "Reagan"
       token2 = "War"
       k = 5
       result = near_query(positional_index, token1, token2, k)
       print(f"Documents where '{token1}' is within {k} tokens of '{token2}': {sorted(result)}")
       ```

   - **Boolean Retrieval (AND, OR):**
     - Retrieves documents matching a query based on single-term or multi-term boolean logic (AND/OR).
     - Example query:
       ```python
       query = "Reagan and War"
       result = retrieval(index, query)
       print_tokens(query, result)
       ```

   - **Preprocessing Techniques:**
     - Generates indexes for different preprocessing steps (case folding, removing numbers, stop words, and stemming).
     - Outputs a statistical summary comparing:
       - Distinct Terms
       - Non-positional Postings
       - Total Tokens

     Example of preprocessing results:
     ```
     Preprocessing Step     Distinct Terms     Nonpositional Postings     Tokens
     Unfiltered             125678            450345                     1256789
     Case Folding           120567            430123                     1205678
     ```

5. **Files**
   - **Dataset Files:** Ensure `.sgm` files are in the directory specified by `dataset_path`.
   - **Script Output:** Displays a statistical table of preprocessing techniques in the terminal, as well as the results of the queries.

6. **Python Packages**
   - **NLTK:**
     - Installation: `pip install nltk`
     - Version: Latest
     - Ensure `punkt` and `stopwords` are downloaded via `nltk.download()`

   - **Regex:**
     - Installation: Built into Python (no installation needed)

7. **Customization**
   - To modify preprocessing, adjust the flags in `preprocessed_indexer()`:
     - `case_fold=True`: Converts text to lowercase.
     - `remove_numbers=True`: Removes numeric tokens.
     - `remove_stopwords=True`: Filters out common stop words.
     - `apply_stemming=True`: Applies stemming using the Porter Stemmer.
