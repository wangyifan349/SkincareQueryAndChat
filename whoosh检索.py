from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import MultifieldParser
import os
import pandas as pd

# -----------------------------------------------
# 定义索引的schema，包括title和content字段，且都设置为存储（stored=True）
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
index_dir = "indexdir"  # 索引目录名称

# -----------------------------------------------
# 如果索引目录不存在，则创建目录并建立索引
if not os.path.exists(index_dir):
    os.mkdir(index_dir)  # 创建索引目录
    ix = create_in(index_dir, schema)  # 创建索引对象
    writer = ix.writer()  # 创建索引写入器

    # 定义要添加到索引的文档列表，每个文档包含title和content
    documents = [
        {"title": "Vitamin A", "content": "Vitamin A is important for normal vision, the immune system, and reproduction."},
        {"title": "Vitamin C", "content": "Vitamin C, also known as ascorbic acid, is an essential nutrient involved in the repair of tissue."},
        {"title": "Antibiotic: Penicillin", "content": "Penicillin is one of the first discovered and widely used antibiotic agents."},
        {"title": "Antiviral: Acyclovir", "content": "Acyclovir is an antiviral medication primarily used for the treatment of herpes simplex virus infections."},
        {"title": "DNA", "content": "DNA is a molecule that carries the genetic instructions used in growth, development, and functioning of all living organisms."}
    ]

    # 将每个文档添加到索引写入器
    for doc in documents:
        writer.add_document(title=doc["title"], content=doc["content"])

    writer.commit()  # 提交写入操作，保存索引
else:
    # 如果索引目录已存在，直接打开索引
    ix = open_dir(index_dir)

# -----------------------------------------------
# 定义搜索函数，接受查询字符串和分数阈值参数
def search(query_str, score_threshold=0.0):
    try:
        # 使用索引搜索器进行搜索
        with ix.searcher() as searcher:
            # 使用多字段解析器解析查询字符串，支持title和content字段
            query = MultifieldParser(["title", "content"], ix.schema).parse(query_str)
            # 执行搜索，limit=None表示返回所有匹配结果
            results = searcher.search(query, limit=None)

            data = []  # 用于存储符合条件的搜索结果
            for result in results:
                # 只保留得分大于等于阈值的结果
                if result.score >= score_threshold:
                    data.append({
                        "Title": result['title'],
                        "Content": result['content'],
                        "Score": result.score
                    })

            # 如果有符合条件的结果，使用pandas DataFrame格式化输出
            if data:
                df = pd.DataFrame(data)
                print(df)
            else:
                # 无符合条件结果时，给出提示
                print(f"No results found with score >= {score_threshold}.")
    except Exception as e:
        # 捕获并打印搜索过程中的异常，防止程序崩溃
        print(f"An error occurred during search: {e}")

# -----------------------------------------------
# 交互模式函数，支持用户输入查询和命令
def interactive_mode():
    score_threshold = 0.5  # 默认分数阈值
    print("Welcome to the Whoosh search interface.")
    print("Type your search query and press Enter to search.")
    print("Commands:")
    print("  :exit       - Exit the program")
    print("  :threshold  - Set a new score threshold (e.g. ':threshold 0.7')")
    print(f"Current score threshold is {score_threshold}\n")

    while True:
        user_input = input("Enter your search query or command: ").strip()
        if not user_input:
            # 空输入时跳过
            continue

        if user_input.lower() == ':exit':
            # 用户输入退出命令，结束循环
            print("Exiting the search.")
            break

        elif user_input.lower().startswith(':threshold'):
            # 用户输入调整阈值命令
            parts = user_input.split()
            if len(parts) == 2:
                try:
                    new_threshold = float(parts[1])
                    # 限制阈值范围在0到10之间
                    if 0 <= new_threshold <= 10:
                        score_threshold = new_threshold
                        print(f"Score threshold updated to {score_threshold}")
                    else:
                        print("Please enter a threshold between 0 and 10.")
                except ValueError:
                    print("Invalid threshold value. Please enter a numeric value.")
            else:
                print("Usage: :threshold <value>")

        else:
            # 普通查询，调用搜索函数
            print(f"Searching for '{user_input}' with score threshold {score_threshold}:")
            search(user_input, score_threshold)

# -----------------------------------------------
# 程序入口，启动交互模式
if __name__ == "__main__":
    interactive_mode()
