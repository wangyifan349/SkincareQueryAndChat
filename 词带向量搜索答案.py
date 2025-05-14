from flask import Flask, request, jsonify, render_template_string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 初始化Flask应用
app = Flask(__name__)

# 预定义的问答数据
faq_data = [
    {'question': 'What is Flask?', 'answer': 'Flask is a micro web framework for Python.'},
    {'question': 'How to install Flask?', 'answer': 'You can install Flask using pip: pip install Flask.'},
    {'question': 'What is Python?', 'answer': 'Python is a high-level programming language.'},
    {'question': 'How does Flask route work?', 'answer': 'Flask routes are created using app.route decorators.'},
]

# 计算最相似的问题
def find_answer(user_question, faq_data):
    questions = [item['question'] for item in faq_data]
    vectorizer = CountVectorizer().fit_transform(questions + [user_question])
    vectors = vectorizer.toarray()
    
    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1])
    most_similar_index = np.argmax(cosine_similarities)
    return faq_data[most_similar_index] ['answer']

# 主界面路由
@app.route('/')
def home():
    return render_template_string(chat_html)

# AJAX请求处理
@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    user_question = data['question']
    answer = find_answer(user_question, faq_data)
    return jsonify({'answer': answer})

# 定义HTML模板，使用Bootstrap和自定义样式模拟微信风格，支持暗色模式和响应式设计
chat_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>聊天机器人</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 0; }
        .chat-container {
            max-width: 600px;
            margin: 0 auto;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background-color: #f0f0f0;
        }
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            background-color: #e5ddd5;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 7.5px;
            max-width: 75%;
        }
        .message-user {
            background-color: #dcf8c6;
            align-self: flex-end;
        }
        .message-bot {
            background-color: #ffffff;
            align-self: flex-start;
        }
        .input-group {
            padding: 10px;
            background-color: #f0f0f0;
        }
        /* 暗色模式支持 */
        @media (prefers-color-scheme: dark) {
            body { background-color: #121212; color: #ffffff; }
            .chat-box { background-color: #303030; }
            .message-user { background-color: #3b7e72; }
            .message-bot { background-color: #424242; }
            .input-group { background-color: #1e1e1e; }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-box" id="chat-box">
            <!-- 消息将出现在这里 -->
        </div>
        <div class="input-group d-flex">
            <input type="text" id="question-input" class="form-control" placeholder="请输入您的问题">
            <div class="input-group-append">
                <button class="btn btn-success" onclick="submitQuestion()">发送</button>
            </div>
        </div>
    </div>

    <script>
        function submitQuestion() {
            var questionInput = document.getElementById('question-input');
            var userQuestion = questionInput.value;
            if (!userQuestion.trim()) return;

            var chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="message message-user"><strong>您:</strong> ${userQuestion}</div>`;

            fetch('/get_answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: userQuestion })
            }).then(response => response.json())
              .then(data => {
                chatBox.innerHTML += `<div class="message message-bot"><strong>机器人:</strong> ${data.answer}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight; // 滚动到最新消息
              }).catch(error => console.error('Error:', error));

            questionInput.value = '';
        }
    </script>
</body>
</html>
"""

# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=False)
