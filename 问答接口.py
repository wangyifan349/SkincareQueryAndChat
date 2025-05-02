from flask import Flask, request, jsonify
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
app = Flask(__name__)
# Load the data from the JSON file
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
questions = [entry['question'] for entry in data]
answers = [entry['answer'] for entry in data]
# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
# Encode the questions and create a Faiss index
def initialize_faiss(questions):
    # Encode all the questions
    question_embeddings = model.encode(questions)
    # Determine the dimension of the embeddings
    dimension = question_embeddings.shape[1]
    # Create a Faiss index with L2 distance
    index = faiss.IndexFlatL2(dimension)
    # Add the encoded questions to the Faiss index
    index.add(np.array(question_embeddings))
    return index

# Initialize the Faiss index
index = initialize_faiss(questions)
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    # Encode the query
    query_embedding = model.encode([query])
    # Search in the Faiss index
    distances, indices = index.search(np.array(query_embedding), 1)
    # Get the closest match
    best_match_idx = indices[0][0]
    best_answer = answers[best_match_idx]
    return jsonify({
        'question': questions[best_match_idx],
        'answer': best_answer
    })
if __name__ == '__main__':
    app.run(debug=False)



data.json中存储一下内容

[
    {
        "question": "新能源汽车应该多久保养一次？",
        "answer": "新能源汽车的保养周期通常为每1万公里或一年，以先到者为准。保养项目包括：电池检测，检查电池的健康状态和充电系统；制动系统检查，包括刹车片和制动液的检查；确保车载系统的软件是最新版本，以优化性能和安全性；还有轮胎和悬挂系统的检查，包括胎压和磨损情况。定期保养不仅确保车辆的高效运行，也有助于延长其使用寿命。"
    },
    {
        "question": "电池在行驶中没电了怎么办？",
        "answer": "如果电池在行驶中没电并导致车辆停止，请遵循以下步骤：确认车辆停在安全的位置并打开双闪警示灯。使用车载导航或手机应用快速定位最近的充电站。若无法到达充电站，联系专业的道路救援服务以获取拖车或移动充电服务。日常驾驶中，确保电量不低于20%，并提前规划充电站位置以减少完全没电的风险。"
    },
    {
        "question": "新能源汽车电池的寿命是多久，如何延长？",
        "answer": "新能源汽车电池寿命通常为8-10年或15万至20万公里，具体取决于车型和使用条件。要延长电池寿命，请尽量减少快速充电，采用较慢的家庭或标准充电方式。平常使用时，将电量维持在20%-80%之间，避免深度放电。在阴凉干燥的位置停车，适宜的停车环境可以避免极端温度影响电池性能。"
    },
    {
        "question": "如何正确充电，可延长电池寿命？",
        "answer": "充电时，确保使用来自可靠供应商的正规充电设备，避免使用劣质产品以防损坏电池。充电到80%左右即可，减少满充时间来延缓电池老化。在电池长期不用时，将电量保持在50%左右，并每月进行一次充电。高温和极寒环境下尽量减少充电，保持电池工作在正常的温度范围。"
    },
    {
        "question": "长期存放新能源汽车时，电池如何保养？",
        "answer": "如果计划长期不使用车辆，做好以下几点保养：将电量维持在50%。即使不使用车辆，也要定期启动并充电；确保停车环境良好，选择阴凉干燥的地方停放，避免阳光直射；每3至6个月进行一次电池的全面检测，以保持电池的健康状态。"
    },
    {
        "question": "行驶时车辆发出异常声音是什么原因？",
        "answer": "新能源汽车在行驶中发出异常声响可能源于以下原因：由于电动机和制动系统的操作声音会比内燃机更明显，检查制动系统和悬挂连接是必要的。如有轮胎噪音，需检查轮胎是否正确安装，是否磨损或者气压不当。如果异响持续，建议前往正规维修站进行详细检查，避免潜在问题导致更大故障。"
    }
]






实际需要接入自己的网站，这个只是一个模拟，仅供参考。
后端主要构建问答接口。

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新能源汽车问答</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #faf3e0;
            color: #3e3e3e;
        }
        .chat-container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff5e8;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .chat-box {
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #fffdf6;
            border-radius: 5px;
            border: 1px solid #e7e2d1;
        }
        .question, .answer {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 10px;
        }
        .question {
            background-color: #fff7d6;
            text-align: left;
        }
        .answer {
            background-color: #f1e1b8;
            text-align: right;
        }
        .input-group {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container chat-container">
        <h2 class="text-center mb-4">新能源汽车问答</h2>
        <div id="chat-box" class="chat-box">
            <!-- Chat messages will be appended here -->
        </div>
        <div class="input-group">
            <input type="text" id="user-question" class="form-control" placeholder="请输入你的问题..." aria-label="User question">
            <div class="input-group-append">
                <button id="send-button" class="btn btn-warning">发送</button>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('send-button').addEventListener('click', sendMessage);
        document.getElementById('user-question').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        function sendMessage() {
            const userQuestionEle = document.getElementById('user-question');
            const userQuestion = userQuestionEle.value.trim();
            if (userQuestion) {
                addMessageToChat(userQuestion, 'question');
                fetchAnswer(userQuestion);
                userQuestionEle.value = '';
            }
        }

        function addMessageToChat(message, type) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add(type);
            if (type === 'question') {
                messageDiv.textContent = `你: ${message}`;
            } else {
                messageDiv.textContent = `回答: ${message}`;
            }
            document.getElementById('chat-box').appendChild(messageDiv);
            scrollToBottom();
        }

        function fetchAnswer(question) {
            fetch(`https://example.com/search?query=${encodeURIComponent(question)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.answer) {
                        addMessageToChat(data.answer, 'answer');
                    } else {
                        addMessageToChat('抱歉，我无法找到相关答案。', 'answer');
                    }
                })
                .catch(() => {
                    addMessageToChat('检测到网络问题，请稍后再试。', 'answer');
                });
        }

        function scrollToBottom() {
            const chatBox = document.getElementById('chat-box');
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>


