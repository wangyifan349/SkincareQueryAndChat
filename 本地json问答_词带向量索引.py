import json
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
# ----------------------------------------
# 1. 读取本地 JSON 格式的 QA 数据
def load_qa_data(path='qa_data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
# ----------------------------------------
# 2. 用 TF-IDF 向量化问题列表
def build_vectorizer(questions):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(questions)
    return vectorizer, vectors
# ----------------------------------------
# 3. 稀疏矩阵转成 dense float32 矩阵，便于 Faiss 使用
def to_dense_float32(sparse_matrix):
    dense = sparse_matrix.astype(np.float32).toarray()
    return dense
# ----------------------------------------
# 4. 用 faiss 建立 L2 距离的向量索引
def build_faiss_index(vectors_dense):
    dimension = vectors_dense.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors_dense)
    return index
# ----------------------------------------
# 5. 使用 Faiss 查询 top_k 近邻（L2距离）
def faiss_search(index, query_vec_dense, top_k=10):
    distances, indices = index.search(query_vec_dense, top_k)
    return distances, indices
# ----------------------------------------
# 6. 计算 query_vector 与候选向量的余弦相似度
def cosine_similarity(query_vec_dense, candidate_vecs_dense):
    normalized_query = normalize(query_vec_dense)
    normalized_candidates = normalize(candidate_vecs_dense)
    sim = normalized_query.dot(normalized_candidates.T)
    if hasattr(sim, "toarray"):
        sim = sim.toarray()
    return sim.flatten()
# ----------------------------------------
# 主流程，平铺无嵌套，照步骤执行
# 1. 装载数据
qa_data = load_qa_data()
# 2. 提取所有问题列表
questions_list = []
for item in qa_data:
    questions_list.append(item['question'])
# 3. 建向量器及生成问题向量矩阵
vectorizer, question_vectors_sparse = build_vectorizer(questions_list)
# 4. 转换为dense矩阵供Faiss使用
question_vectors_dense = to_dense_float32(question_vectors_sparse)
# 5. 建立faiss索引
faiss_index = build_faiss_index(question_vectors_dense)
# 下面进入交互循环，查询阶段
while True:
    user_query = input("请输入你的问题（输入 exit 退出）：")
    if user_query.lower() == 'exit':
        break
    # 6. 向量化用户问题
    user_query_sparse = vectorizer.transform([user_query])
    # 7. 转换成dense float32格式
    user_query_dense = to_dense_float32(user_query_sparse)
    # 8. 用Faiss找top_k个候选（L2距离）
    top_k = 10
    dists, idxs = faiss_search(faiss_index, user_query_dense, top_k)
    # 9. 提取候选向量
    candidates_dense = question_vectors_dense[idxs[0]]
    # 10. 计算余弦相似度
    similarities = cosine_similarity(user_query_dense, candidates_dense)
    # 11. 匹配索引与相似度配对
    pairs = []
    for i in range(len(idxs[0])):
        pairs.append((idxs[0][i], similarities[i]))
    # 12. 选出相似度最高的top3，按相似度降序
    # 先排序
    pairs.sort(key=lambda x: x[1], reverse=True)
    # 13. 打印结果
    print("\n------- Top 3 最相关问答 -------")
    for i in range(min(3, len(pairs))):
        idx = pairs[i][0]
        sim = pairs[i][1]
        print("-------------------------------")
        print("问题：", qa_data[idx]['question'])
        print("答案：", qa_data[idx]['answer'])
        print(f"相似度（余弦）：{sim:.3f}")
    print("-------------------------------\n")
