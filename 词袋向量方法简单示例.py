import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Custom tokenizer using jieba for Chinese word segmentation
def jieba_tokenizer(text):
    return list(jieba.cut(text))
# Sample question-answer dictionary
qa_pairs = {
    "什么是高血压？": "High blood pressure is a condition where the pressure in the arteries is elevated.",
    "如何预防感冒？": "Maintain good personal hygiene, wash your hands regularly, and avoid contact with infected people.",
    "糖尿病的症状有哪些？": "Common symptoms include increased urination, thirst, weight loss, and fatigue.",
    "什么是偏头痛？": "Migraine is a common type of headache, often accompanied by nausea, vomiting, and sensitivity to light or sound.",
    "如何治疗失眠？": "Treatment methods include improving sleep environment, maintaining a regular sleep schedule, and relaxation training."
}
# Convert all questions to lowercase for consistent matching
qa_pairs_lower = {}
for question, answer in qa_pairs.items():
    qa_pairs_lower[question.lower()] = answer
# Create a list of all questions in lowercase
questions = list(qa_pairs_lower.keys())
# Initialize the TF-IDF Vectorizer with the custom jieba tokenizer
tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenizer, lowercase=True)
# Build the TF-IDF matrix for the questions
tfidf_matrix = tfidf_vectorizer.fit_transform(questions)
# Define a function to find the best matching answers using cosine similarity
def find_best_answers(user_question, threshold=0.1):
    if not user_question.strip():
        return []
    user_question_lower = user_question.lower()
    # Transform the user's question into a TF-IDF vector
    user_vector = tfidf_vectorizer.transform([user_question_lower])
    # Compute cosine similarities between the user question and all stored questions
    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    # Get indices sorted by similarity in descending order
    sorted_indices = cosine_similarities.argsort()[::-1]
    results = []
    for i in sorted_indices:
        sim = cosine_similarities[i]
        # If similarity is below threshold, append a message and break out of the loop
        if sim < threshold:
            message = f"Similarity below threshold ({threshold}). Suitable answer may not be found."
            results.append(("No Match", message, sim))
            break
        question = questions[i]
        answer = qa_pairs_lower[question]
        results.append((question, answer, sim))
    return results
print("Welcome to the Q&A Bot! Type 'exit' to quit.")
while True:
    user_input = input("Enter your question: ")
    if user_input.strip().lower() == "exit":
        print("Thank you for using the Q&A Bot. Goodbye!")
        break
    answer_list = find_best_answers(user_input)
    print("Matched Answers (sorted by similarity):")
    for question, answer, similarity in answer_list:
        print("Question: {} (Similarity: {:.4f})".format(question, similarity))
        print("Answer: {}\n".format(answer))
