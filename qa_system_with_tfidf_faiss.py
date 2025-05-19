假设你的问答对存储在一个名为qa_data.json的JSON文件中，
文件格式如下
{
    "What are the symptoms of diabetes?": "Common symptoms of diabetes include increased thirst, frequent urination, and unexplained weight loss. Other symptoms may include extreme hunger, presence of ketones in the urine, fatigue, irritability, blurred vision, slow-healing sores, frequent infections, and in some cases, areas of darkened skin. It's important to consult a healthcare provider for a confirmed diagnosis and appropriate management plan if these symptoms are present.",    
    "Explain the process of mitosis.": "Mitosis is a fundamental process for life as it involves the division of a parent cell into two identical daughter cells. This process consists of several stages: prophase, where chromatin condenses into visible chromosomes and the mitotic spindle forms; metaphase, where the chromosomes align at the cell's equatorial plate; anaphase, where the sister chromatids are pulled apart to opposite poles of the cell; and telophase, where the chromosomes begin to de-condense and are surrounded by a re-forming nuclear envelope. Cytokinesis usually follows, dividing the cell's cytoplasm to form two distinct cells. Mitosis ensures genetic consistency in cell reproduction, facilitating growth and repair in multicellular organisms.",    
    "What is the treatment for hypertension?": "The treatment for hypertension typically involves a combination of lifestyle changes and medication. Lifestyle modifications may include dietary changes such as reducing sodium intake, eating a balanced diet rich in fruits and vegetables, and maintaining a healthy weight through regular exercise. Quitting smoking and limiting alcohol consumption can also be beneficial. Medications such as diuretics, ACE inhibitors, calcium channel blockers, and beta-blockers may be prescribed to help manage high blood pressure. It's important for individuals to work closely with healthcare providers to monitor blood pressure levels and adjust treatment plans as needed.",
    "Describe the structure of DNA.": "DNA, or deoxyribonucleic acid, is the hereditary material in humans and almost all other organisms. Its structure is a double helix, which resembles a twisted ladder. The sides of the ladder are composed of alternating sugar (deoxyribose) and phosphate groups, while the rungs consist of nitrogenous base pairs. There are four types of nitrogenous bases in DNA: adenine (A), thymine (T), cytosine (C), and guanine (G). The bases pair specifically, with adenine pairing with thymine and cytosine pairing with guanine, forming base pairs held together by hydrogen bonds. This structure is crucial for DNA replication and the accurate transmission of genetic information during cell division."
}

"""
pip install scikit-learn faiss-cpu numpy jieba
"""

import json
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import numpy as np
# 从JSON文件加载问答字典
def load_qa_from_json(file_path):
    with open(file_path, "r", encoding='utf-8') as file:  # 注意添加encoding设置
        qa_dict = json.load(file)
    return qa_dict
# 对中文文本进行分词
def chinese_tokenizer(text):
    return jieba.lcut(text)
# 示例：从外部JSON文件加载
qa_dict = load_qa_from_json('qa_data.json')
# 获取所有问题和答案
questions = list(qa_dict.keys())
answers = list(qa_dict.values())
# 使用TF-IDF向量化问题，同时指定自定义的分词器
vectorizer = TfidfVectorizer(tokenizer=chinese_tokenizer)
tfidf_matrix = vectorizer.fit_transform(questions).toarray()
# 使用Faiss进行最近邻搜索
dimension = tfidf_matrix.shape[1]
index = faiss.IndexFlatL2(dimension)  # 使用L2距离
index.add(tfidf_matrix)
# 开始持续对话
print("欢迎使用医学和生物问答系统。输入 'exit' 结束对话。\n")
while True:
    query = input("你: ")
    if query.lower() == "exit":
        print("再见！")
        break
    query_vec = vectorizer.transform([query]).toarray()
    # 使用Faiss进行搜索
    k = 1  # 找到最接近的一个问题
    D, I = index.search(query_vec.astype('float32'), k)
    # 找到最匹配的问答对
    best_match_index = I[0][0]
    best_question = questions[best_match_index]
    best_answer = answers[best_match_index]
    # 输出结果
    print("AI:", best_answer)
    print(f"(匹配问题: {best_question} | 相似度得分: {1 - D[0][0]:.4f})\n")
