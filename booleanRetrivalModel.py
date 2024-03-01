import numpy as np

def process_documents(sentences):
        """
    Process the input documents to extract unique words and create an incidence matrix.

    Args:
        sentences (list): List of input documents.

    Returns:
        tuple: A tuple containing a list of unique words and a numpy array representing the incidence matrix.
    """
    # Extract all unique words from the documents and create a sorted list
    all_words = [word.lower().rstrip(',.?!') for doc in sentences for word in doc.split()]
    unique_words = sorted(set(all_words))
    
    # Count the occurrence of each word in each document and store it in a list of dictionaries
    word_counts = []
    for doc in sentences:
        doc_words = doc.split('. ')
        for sentence in doc_words:
            words = [word.lower().rstrip(',.?!') for word in sentence.split()]
            word_counts.append({word: words.count(word) for word in words})
            
    # Create an incidence matrix to represent the presence of words in documents
    sentences_count = len(word_counts)
    incidence_matrix = np.zeros((len(unique_words), sentences_count), dtype=np.int8)

    for i, count in enumerate(word_counts):
        for j, word in enumerate(unique_words):
            if word in count:
                incidence_matrix[j, i] = 1

    return unique_words, incidence_matrix

def evaluate_query(query, sentences, unique_words, incidence_matrix):
        """
    Evaluate a boolean query against the collection of documents.

    Args:
        query (str): The boolean query provided by the user.
        sentences (list): List of documents.
        unique_words (list): List of unique words in the documents.
        incidence_matrix (numpy.ndarray): Incidence matrix representing the presence of words in documents.

    Returns:
        set: A set of document indices that satisfy the query.
    """
    result_docs = set(range(len(sentences)))

    query_terms = query.split()
    boolean_operators=["AND","OR","NOT"]
    bool_operator = "AND"  # Default boolean operator
    for i, term in enumerate(query_terms):
        if term in boolean_operators:
            bool_operator = term
        else:
            try:
                term_index = unique_words.index(term.lower())
                term_vector = incidence_matrix[term_index]
            except ValueError:
                print(f"Term '{term}' not found in documents.")
                continue

            if i == 0:
                result_docs = set(np.where(term_vector == 1)[0])
            else:
                if bool_operator == "AND":
                    result_docs = result_docs.intersection(np.where(term_vector == 1)[0])
                elif bool_operator == "OR":
                    result_docs = result_docs.union(np.where(term_vector == 1)[0])
                elif bool_operator == "NOT":
                    result_docs = result_docs.difference(np.where(term_vector == 1)[0])

    return result_docs
def main():
        """
    Main function to execute the boolean retrieval system.

    This function interacts with the user to input documents and queries,
    and displays the documents that satisfy the queries.
    """
    while True:
        num_docs = int(input("Enter the number of documents: "))
        sentences = []
        for i in range(num_docs):
            sentence = input(f"Enter document {i+1}: ")
            sentences.append(sentence)

        unique_words, incidence_matrix = process_documents(sentences)

        query = input("Enter your query: ")

        result_docs = evaluate_query(query, sentences, unique_words, incidence_matrix)

        print("Documents satisfying the query:")
        for doc_index in result_docs:
            print(f"doc{doc_index}: {sentences[doc_index]}")

        change_doc = input("Do you want to change the documents? (yes/no): ")
        if change_doc.lower() != 'yes':
            break

    while True:
        change_query = input("Do you want to change the query? (yes/no): ")
        if change_query.lower() != 'yes':
            break
        query = input("Enter your new query: ")
        result_docs = evaluate_query(query, sentences, unique_words, incidence_matrix)
        print("Documents satisfying the query:")
        for doc_index in result_docs:
            print(f"doc{doc_index}: {sentences[doc_index]}")

if __name__ == "__main__":
    main()
