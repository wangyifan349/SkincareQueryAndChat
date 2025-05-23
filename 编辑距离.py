import os
import argparse

# 嵌入式物理学知识
PHYSICS_KNOWLEDGE = [
    {
        "name": "牛顿第一定律",
        "description": "任何物体都要保持匀速直线运动或静止状态，直到外力迫使它改变运动状态为止。",
        "formula": "无",
        "keywords": ["惯性", "力", "运动"]
    },
    {
        "name": "牛顿第二定律",
        "description": "物体加速度的大小跟作用力成正比，跟物体的质量成反比，加速度的方向跟作用力的方向相同。",
        "formula": "F = ma",
        "keywords": ["力", "质量", "加速度"]
    },
    {
       "name": "重力势能",
       "description": "物体由于被举高而具有的能",
       "formula": "E = mgh",
       "keywords": ["质量", "重力加速度", "高度"]
    },
    {
        "name": "动能定理",
        "description": "合外力所做的功等于物体动能的变化",
        "formula": "W = ΔEk",
        "keywords": ["功", "动能", "能量"]
    }

]

def edit_distance(s1, s2):
    """计算两个字符串之间的编辑距离(Levenshtein距离)."""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def jaccard_similarity(set1, set2):
    """计算两个集合之间的 Jaccard 相似度."""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0  # 避免除以零
    return intersection / union

def search_knowledge(query):
    """
    搜索嵌入的物理学知识. 仅搜索知识库，不再搜索文件。

    Args:
        query: 要搜索的字符串。
    """
    results = []

    # 搜索嵌入的物理学知识
    query_keywords = set(query.lower().split())  # 将查询关键词转换为集合

    for item in PHYSICS_KNOWLEDGE:
        knowledge_keywords = []
        for keyword in item['keywords']:
            knowledge_keywords.append(keyword.lower())
        knowledge_keywords_set = set(knowledge_keywords)

        similarity = jaccard_similarity(query_keywords, knowledge_keywords_set)

        if similarity > 0.5:  # 设置 Jaccard 相似度阈值
            results.append(item)

        # 编辑距离匹配
        distance = edit_distance(query.lower(), item['name'].lower())
        if distance <= 2:  # 设置一个阈值
            results.append(item)

    return results

def main():
    while True:
        query = input("请输入你的问题 (输入 '退出' 结束): ")
        if query.lower() == "退出":
            break

        results = search_knowledge(query)

        if results:
            print("找到以下相关知识：")
            for item in results:
                print(f"  名称: {item['name']}")
                print(f"  描述: {item['description']}")
                print(f"  公式: {item['formula']}")
                print("---")
        else:
            print("未找到匹配的知识。")

if __name__ == "__main__":
    main()
