from flask import Flask, render_template, request, jsonify
from data import products, questions

# 初始化 Flask 应用
app = Flask(__name__)
# -----------------------------------
# 长公共子序列算法（LCS）
# -----------------------------------
def longest_common_subsequence(X, Y):
    # 初始化二维数组
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    # 填充 LCS 表
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
# 查找最接近的产品
# -----------------------------------
def find_closest_products(query, num_results=3):
    query = query.lower().strip()
    matches = []
    for product in products:
        lcs = longest_common_subsequence(query, product["name"].lower())
        if lcs > 0:  # 只考虑 LCS 大于 0 的条目
            matches.append((lcs, product))
    # 排序匹配结果
    def sort_key(match):
        return match[0]
    matches.sort(key=sort_key, reverse=True)
    # 收集最接近的产品结果
    results = []
    limit = min(num_results, len(matches))
    for index in range(limit):
        results.append(matches[index][1])
    return results
# -----------------------------------
# 查找最接近的答案
# -----------------------------------
def find_closest_answer(question):
    question = question.lower().strip()
    best_question = None
    max_lcs = -1
    for q in questions:
        lcs = longest_common_subsequence(question, q.lower())
        if lcs > max_lcs:
            max_lcs = lcs
            best_question = q
    if best_question is not None:
        return questions.get(best_question, "Sorry, I don't know the answer to that question.")
    return "Sorry, I don't know the answer to that question."
# -----------------------------------
# 路由
# -----------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            search_results = find_closest_products(query)
    return render_template('index.html', search_results=search_results)
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
    answer = find_closest_answer(question)
    return jsonify({'answer': answer})
# -----------------------------------
# 启动应用
# -----------------------------------
if __name__ == '__main__':
    app.run(debug=False)
