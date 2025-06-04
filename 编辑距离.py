import Levenshtein


def edit_distance(s1, s2):
    """
    计算字符串 s1 和 s2 的编辑距离（Levenshtein 距离）。
    
    编辑距离指的是将字符串 s1 转换为 s2 所需要的最少编辑操作次数，
    操作包括插入、删除和替换。

    参数:
        s1 (str): 第一个字符串。
        s2 (str): 第二个字符串。

    返回:
        int: s1 和 s2 之间的编辑距离。
    """
    # 创建二维 DP 数组，大小为 (len(s1)+1) x (len(s2)+1)
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化边界值：
    # 当 s1 为空字符串时，将 s1 转换为 s2 需要插入所有字符
    for i in range(m + 1):
        dp[i][0] = i
    # 当 s2 为空字符串时，从 s1 变为 s2 需要删除所有字符
    for j in range(n + 1):
        dp[0][j] = j

    # 填充 DP 表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 如果两个字符相同，则不需要额外操作
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # 删除操作
                dp[i][j - 1] + 1,      # 插入操作
                dp[i - 1][j - 1] + cost  # 替换操作
            )
    return dp[m][n]


def longest_common_subsequence(s1, s2):
    """
    计算字符串 s1 和 s2 的最长公共子序列的长度。

    最长公共子序列指的是两个字符串中均出现的、顺序一致但不要求连续的字符序列。
    例如，对于 s1 = "ABCBDAB"，s2 = "BDCABA"，其最长公共子序列可能为 "BCBA"，长度为 4。

    参数:
        s1 (str): 第一个字符串。
        s2 (str): 第二个字符串。

    返回:
        int: s1 和 s2 的最长公共子序列的长度。
    """
    m, n = len(s1), len(s2)
    # 创建二维 DP 数组，大小为 (m+1) x (n+1)，初始值均为 0
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 填充 DP 表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # 字符相同，则最大长度加 1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # 否则，取上方或左侧较大值
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

"""
# 示例用法
str1 = "intention"
str2 = "execution"
print("编辑距离:", edit_distance(str1, str2))  # 期望输出编辑距离
print("最长公共子序列长度:", longest_common_subsequence("ABCBDAB", "BDCABA"))  # 示例输出
"""





# 嵌入式物理学知识（不包含 formula 和 keywords 字段）
PHYSICS_KNOWLEDGE = [
    {
        "name": "牛顿第一定律",
        "description": (
            "牛顿第一定律，又称为惯性定律，描述了物体保持静止或均匀直线运动状态的性质。"
            "即：物体不愿意改变自身运动状态，除非受到外力的作用。"
            "例如，当一辆汽车突然停车时，车内的乘客会因为惯性而向前倾，这是该定律在日常生活中的直观体现。"
        )
    },
    {
        "name": "牛顿第二定律",
        "description": (
            "牛顿第二定律说明了物体的加速度与作用于物体上的外力成正比，并与物体的质量成反比。"
            "也就是说，对于一个固定质量的物体，外力越大，加速度越大；而对于相同外力，质量越大，加速度则越小。"
            "这一原理是许多工程和物理问题分析的重要基础，例如汽车加速、火箭发射等。"
        )
    },
    {
        "name": "重力势能",
        "description": (
            "重力势能是物体因其所在高度而具有的能量。物体在高处具有更高的重力势能，"
            "这与物体的质量、高度以及当地重力加速度有关。举例来说，一块放在高处的石头相较于在低处的石头蕴含更大的能量，"
            "这种能量在物体下落时会转化为动能。"
        )
    },
    {
        "name": "动能定理",
        "description": (
            "动能定理阐述了外力做功与物体动能变化之间的关系，即外力所作的总功等于物体动能的变化。"
            "这一理论为我们了解能量转化过程提供了重要依据，在碰撞分析、机械运动及安全性能评价中均有重要应用。"
        )
    }
]

def search_knowledge(query):
    """
    搜索嵌入的物理学知识，只返回标题和详细描述。
    参数:
        query: 要搜索的字符串。
    返回:
        一个字典，键为知识的标题，值为详细描述。
    """
    results = {}
    query_lower = query.lower()
    for item in PHYSICS_KNOWLEDGE:
        name_lower = item['name'].lower()
        description_lower = item['description'].lower()
        # 如果 query 是名称或描述的子串，则视为匹配
        if query_lower in name_lower or query_lower in description_lower:
            results[item['name']] = item['description']
        else:
            # 编辑距离匹配：针对名称计算编辑距离，容许的阈值设置为 2
            distance = Levenshtein.distance(query_lower, name_lower)
            if distance <= 2:
                results[item['name']] = item['description']
    return results

def main():
    while True:
        query = input("请输入你的问题 (输入 '退出' 结束): ")
        if query.lower() == "退出":
            break
        results = search_knowledge(query)
        if results:
            print("找到以下相关知识：")
            for title, content in results.items():
                print(f"{title}:")
                print(content)
                print("---")
        else:
            print("未找到匹配的知识。")

if __name__ == "__main__":
    main()
