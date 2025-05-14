from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import MultifieldParser
import os
import pandas as pd
# -----------------------------------------------
# Define the schema for the index, including title and content fields
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
# -----------------------------------------------
# Create an index directory, create it if it does not exist
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
# Create the index
ix = create_in("indexdir", schema)
# -----------------------------------------------
# Create an index writer object
writer = ix.writer()
# -----------------------------------------------
# Define the documents to be added to the index
documents = [
    {"title": "Vitamin A", "content": "Vitamin A is important for normal vision, the immune system, and reproduction."},
    {"title": "Vitamin C", "content": "Vitamin C, also known as ascorbic acid, is an essential nutrient involved in the repair of tissue."},
    {"title": "Antibiotic: Penicillin", "content": "Penicillin is one of the first discovered and widely used antibiotic agents."},
    {"title": "Antiviral: Acyclovir", "content": "Acyclovir is an antiviral medication primarily used for the treatment of herpes simplex virus infections."},
    {"title": "DNA", "content": "DNA is a molecule that carries the genetic instructions used in growth, development, and functioning of all living organisms."}
]
# -----------------------------------------------
# Add each document to the index
for doc in documents:
    writer.add_document(title=doc["title"], content=doc["content"])
# Commit the write operation to save the index
writer.commit()
# -----------------------------------------------
# Define the search function, accepting a query string and score threshold
def search(query_str, score_threshold=0.0):
    # Use the searcher to execute a query
    with ix.searcher() as searcher:
        # Parse the query string with a multifield parser
        query = MultifieldParser(["title", "content"], ix.schema).parse(query_str)
        # Execute the search
        results = searcher.search(query)
        # Create an empty list to store the results
        data = []
        # Iterate through the search results
        for result in results:
            # Check if the result score is above or equal to the threshold
            if result.score >= score_threshold:
                # Append qualifying results to the data list
                data.append({
                    "Title": result['title'],
                    "Content": result['content'],
                    "Score": result.score
                })
        # Print the results using a pandas DataFrame
        df = pd.DataFrame(data)
        print(df)
# -----------------------------------------------
# Set the score threshold, perform searches and print results
score_threshold = 0.5  # Defined score threshold
print("Searching for 'Vitamin' with score threshold 0.5:")
search("Vitamin", score_threshold)
print("\nSearching for 'Antibiotic' with score threshold 0.5:")
search("Antibiotic", score_threshold)
