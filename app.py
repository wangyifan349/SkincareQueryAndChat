from flask import Flask, render_template, request, jsonify
from data import products, questions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import numpy as np

app = Flask(__name__)
# -----------------------------------
# 长公共子序列算法（LCS）
# -----------------------------------
def longest_common_subsequence(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L[m][n]
# -----------------------------------
# TF-IDF + 余弦相似度
# -----------------------------------
def calculate_tfidf_cosine_similarity(query, texts, use_jieba=False):
    if use_jieba:
        # 使用jieba分词
        texts_cut = []
        for text in texts:
            texts_cut.append(" ".join(jieba.cut(text)))
        query = " ".join(jieba.cut(query))
    else:
        texts_cut = texts
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts_cut)
    query_vec = tfidf_vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    return similarity
# -----------------------------------
# 查找最接近的产品
# -----------------------------------
def find_closest_products(query, num_results=3, method='lcs'):
    query = query.lower().strip()
    matches = []
    if method == 'lcs':
        for product in products:
            lcs = longest_common_subsequence(query, product["name"].lower())
            if lcs > 0:
                matches.append((lcs, product))
        matches.sort(key=lambda match: match[0], reverse=True)
    elif method == 'tfidf':
        names = []
        for product in products:
            names.append(product['name'])
        similarities = calculate_tfidf_cosine_similarity(query, names, use_jieba=True)
        for idx in range(len(similarities)):
            matches.append((similarities[idx], products[idx]))
        matches.sort(key=lambda match: match[0], reverse=True)
    else:
        raise ValueError("Invalid method: choose 'lcs' or 'tfidf'")
    results = []
    for match in matches[:num_results]:
        results.append(match[1])
    return results
# -----------------------------------
# 查找最接近的答案
# -----------------------------------
def find_closest_answer(question, method='lcs'):
    question = question.lower().strip()
    matches = []
    if method == 'lcs':
        for q in questions:
            lcs = longest_common_subsequence(question, q.lower())
            if lcs > 0:
                matches.append((lcs, q))
        matches.sort(key=lambda match: match[0], reverse=True)
        best_question = matches[0][1] if matches else None
    elif method == 'tfidf':
        q_list = list(questions.keys())
        similarities = calculate_tfidf_cosine_similarity(question, q_list, use_jieba=True)
        max_similarity = -1
        best_index = -1
        for idx, sim in enumerate(similarities):
            if sim > max_similarity:
                max_similarity = sim
                best_index = idx
        best_question = q_list[best_index]
    else:
        raise ValueError("Invalid method: choose 'lcs' or 'tfidf'")
    if best_question is not None:
        return questions.get(best_question, "Sorry, I don't know the answer to that question.")
    return "Sorry, I don't know the answer to that question."
# -----------------------------------
# 路由
# -----------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = []
    method = 'lcs'  # Default method
    if request.method == 'POST':
        query = request.form.get('query')
        method = request.form.get('method', 'lcs')  # Get method from form
        if query:
            search_results = find_closest_products(query, method=method)

    return render_template('index.html', search_results=search_results, chosen_method=method)

@app.route('/product/<product_name>')
def product_detail(product_name):
    product = None
    for p in products:
        if p['name'] == product_name:
            product = p
            break
    return render_template('product_detail.html', product=product)

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    method = request.form.get('method', 'lcs')  # Get method from form
    answer = find_closest_answer(question, method=method)
    return jsonify({'answer': answer})
# -----------------------------------
# 启动应用
# -----------------------------------
if __name__ == '__main__':
    app.run(debug=False)
