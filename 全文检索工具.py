import os
import jieba
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser
from whoosh.analysis import Token
from whoosh.query import FuzzyTerm
# ------------------------- 索引和检索相关函数 -------------------------
def jieba_tokenizer_func(text):
    """使用 jieba 对 text 进行分词，并生成 Whoosh 所需的 token"""
    for term in jieba.cut(text, cut_all=False):
        token = Token()
        token.text = term
        yield token
def chinese_analyzer(text):
    """返回自定义 jieba 分词生成器"""
    return jieba_tokenizer_func(text)
def define_schema():
    """定义索引文档的 Schema"""
    return Schema(
        doc_id=ID(stored=True, unique=True),
        title=TEXT(stored=True, analyzer=chinese_analyzer),
        content=TEXT(stored=True, analyzer=chinese_analyzer)
    )
def get_or_create_index(index_dir, schema):
    """获取或创建索引目录"""
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return index.create_in(index_dir, schema)
    else:
        return index.open_dir(index_dir)

def add_or_update_documents(ix, docs):
    """添加或更新文档到索引中，docs 为字典列表"""
    with ix.writer() as writer:
        for doc in docs:
            writer.update_document(doc_id=doc['doc_id'], title=doc['title'], content=doc['content'])

def delete_document(ix, doc_id):
    """基于 doc_id 删除索引中的文档"""
    with ix.writer() as writer:
        writer.delete_by_term('doc_id', doc_id)
def search_documents(ix, query_str, page=1, page_size=5, sort_field=None):
    """
    全文检索，并分页显示结果。
    参数：
      query_str：查询语句；
      page：页码；
      page_size：每页结果数量；
      sort_field：排序字段（可选，仅支持 'title' 或 'content'）
    返回：查询结果组成的字符串信息
    """
    with ix.searcher() as searcher:
        parser = MultifieldParser(['title', 'content'], schema=ix.schema)
        query = parser.parse(query_str)
        results = searcher.search(query, limit=None, sortedby=sort_field)
        total = len(results)
        out = []
        if total == 0:
            out.append("无匹配结果。")
            return "\n".join(out)
        start = (page - 1) * page_size
        end = start + page_size
        if start >= total:
            out.append(f"无第 {page} 页内容，结果数量：{total}")
            return "\n".join(out)
        out.append(f"共 {total} 条结果，显示第 {page} 页（每页 {page_size} 条）：")
        out.append("-" * 50)
        for hit in results[start:end]:
            out.append(f"文档ID: {hit['doc_id']}")
            out.append(f"标题  : {hit['title']}")
            out.append(f"内容  : {hit['content']}")
            out.append("-" * 50)
        return "\n".join(out)
def search_fuzzy(ix, field, term, maxdist=1):
    """
    使用模糊匹配查询，参数：
      field：字段名（仅支持 title、content）；
      term：查询词；
      maxdist：最大编辑距离。
    返回拼接好的字符串结果。
    """
    with ix.searcher() as searcher:
        query = FuzzyTerm(field, term, maxdist=maxdist)
        results = searcher.search(query)
        total = len(results)
        out = []
        if total == 0:
            out.append(f"模糊查询 '{term}' 无匹配结果。")
            return "\n".join(out)
        out.append(f"模糊查询 '{term}' 最大编辑距离 {maxdist}，共 {total} 条匹配：")
        out.append("-" * 50)
        for hit in results:
            out.append(f"文档ID: {hit['doc_id']}")
            out.append(f"标题  : {hit['title']}")
            out.append(f"内容  : {hit['content']}")
            out.append("-" * 50)
        return "\n".join(out)
def init_index_and_data():
    """
    初始化索引及预置数据。首次运行时将建立索引并加入预置文档。
    """
    index_dir = "w_skincare_index"
    schema = define_schema()
    ix = get_or_create_index(index_dir, schema)
    documents = [
        {"doc_id": "1", "title": "The Ordinary Niacinamide 10% + Zinc 1%",
         "content": "主要成分：烟酰胺10%、锌1%。功效：控油，收缩毛孔，抗炎，适合痘痘皮肤使用。"},
        {"doc_id": "2", "title": "The Ordinary Hyaluronic Acid 2% + B5",
         "content": "主要成分：透明质酸，维生素B5。功效：深层补水，修复肌肤屏障，适合干性及敏感皮肤。"},
        {"doc_id": "3", "title": "The Ordinary AHA 30% + BHA 2% Peeling Solution",
         "content": "主要成分：果酸30%，水杨酸2%。功效：物理去角质，提亮肤色，建议敏感肌慎用。"},
        {"doc_id": "4", "title": "Kiehl's Calendula Herbal Extract Toner",
         "content": "主要成分：金盏花提取物，甘油。功效：舒缓镇静，控油保湿，适合油性及敏感皮。"},
        {"doc_id": "5", "title": "La Roche-Posay Cicaplast Baume B5",
         "content": "主要成分：泛醇，修复成分。功效：修复屏障，缓解干燥，适合修复受损肌肤使用。"}
    ]
    add_or_update_documents(ix, documents)
    return ix
# ------------------------- 图形界面 Application -------------------------
class SkincareSearchApp:
    def __init__(self, master):
        """
        初始化图形界面，设置控件及布局。
        """
        self.master = master
        master.title("护肤品全文检索系统")
        master.geometry("800x600")
        # 可设置窗口图标，如：master.iconbitmap('icon.ico')

        # 初始化索引并预置数据
        self.ix = init_index_and_data()

        # 日志输出区域，使用滚动文本框
        self.txt_output = ScrolledText(master, state="disabled", wrap="word", font=("Consolas", 11))
        self.txt_output.pack(expand=True, fill="both", padx=10, pady=10)

        # 命令输入区域
        cmd_frame = ttk.Frame(master)
        cmd_frame.pack(fill="x", padx=10, pady=5)
        self.ent_command = ttk.Entry(cmd_frame, font=("Consolas", 11))
        self.ent_command.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.ent_command.bind("<Return>", self.do_command)
        self.btn_command = ttk.Button(cmd_frame, text="执行", command=self.do_command)
        self.btn_command.pack(side="right")

        # 默认显示帮助信息
        self.print_output("欢迎使用护肤品全文检索系统 (Whoosh + jieba)")
        self.print_output(self.cmd_help([]))

    def print_output(self, text):
        """在输出区域追加文本，并换行显示"""
        self.txt_output.configure(state="normal")
        self.txt_output.insert(tk.END, text + "\n")
        self.txt_output.configure(state="disabled")
        self.txt_output.see(tk.END)

    def do_command(self, event=None):
        """获取命令行输入，处理命令后显示结果"""
        cmd_line = self.ent_command.get().strip()
        self.ent_command.delete(0, tk.END)
        if not cmd_line:
            return
        self.print_output(">> " + cmd_line)
        result = self.process_command(cmd_line)
        if result:
            self.print_output(result)

    def process_command(self, cmd_line):
        """
        解析命令行，并调用对应命令方法：
          search, fuzzy, add, delete, help, exit
        """
        parts = cmd_line.split()
        if not parts:
            return ""
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd == "exit":
            self.master.quit()
            return "退出程序。"
        cmd_map = {
            "search": self.cmd_search,
            "fuzzy": self.cmd_fuzzy,
            "add": self.cmd_add,
            "delete": self.cmd_delete,
            "help": self.cmd_help
        }
        if cmd in cmd_map:
            return cmd_map[cmd](args)
        else:
            return "未知命令，请输入 help 查看使用说明。"

    # 以下各命令实现，均不嵌套其他函数，保持结构清晰

    def cmd_search(self, args):
        """
        search <查询语句> [page] [pagesize] [sort_field]
        说明：全文检索，支持布尔运算、短语、通配符。参数 page, pagesize, sort_field 为可选。
        """
        if not args:
            return "错误：请提供查询语句。"
        query_list = []
        page = 1
        page_size = 5
        sort_field = None
        optional_idx = len(args)
        # 遍历参数，当遇到数字或排序字段时，则认为后续为可选参数
        for idx, arg in enumerate(args):
            if arg.isdigit() or arg in ("title", "content"):
                optional_idx = idx
                break
            query_list.append(arg)
        query_str = " ".join(query_list)
        try:
            if optional_idx < len(args):
                page = int(args[optional_idx])
            if optional_idx + 1 < len(args):
                page_size = int(args[optional_idx + 1])
            if optional_idx + 2 < len(args):
                sort_field = args[optional_idx + 2]
                if sort_field not in ("title", "content"):
                    sort_field = None
        except Exception as e:
            return f"参数解析异常，采用默认参数。错误信息：{e}"
        result = f"执行全文检索: '{query_str}'，页码: {page}, 每页: {page_size}, 排序字段: {sort_field}"
        result += "\n" + search_documents(self.ix, query_str, page, page_size, sort_field)
        return result

    def cmd_fuzzy(self, args):
        """
        fuzzy <字段名> <查询词> [最大编辑距离]
        说明：模糊查询，字段仅支持 title 或 content，最大编辑距离默认为 1。
        """
        if len(args) < 2:
            return "错误：请提供字段名和查询词。"
        field = args[0]
        term = args[1]
        if field not in ("title", "content"):
            return "错误：字段名必须为 title 或 content。"
        maxdist = 1
        if len(args) >= 3 and args[2].isdigit():
            maxdist = int(args[2])
        result = f"执行模糊查询：字段 {field}，词 {term}，最大编辑距离 {maxdist}"
        result += "\n" + search_fuzzy(self.ix, field, term, maxdist)
        return result

    def cmd_add(self, args):
        """
        add
        说明：添加新文档，通过弹窗方式输入 doc_id、标题和内容。
        """
        # 弹出添加文档窗口
        AddDocWindow(self.master, self.ix, self.print_output)
        return "正在添加新文档，请完成弹窗内的填写。"

    def cmd_delete(self, args):
        """
        delete <doc_id>
        说明：删除指定 doc_id 的文档。
        """
        if not args:
            return "错误：请提供 doc_id。"
        delete_document(self.ix, args[0])
        return f"文档 {args[0]} 已删除（如果存在）。"

    def cmd_help(self, args):
        """返回帮助信息字符串"""
        help_text = (
            "命令说明：\n"
            "  search <查询语句> [page] [pagesize] [sort_field]  ：全文搜索，支持布尔运算、短语、通配符\n"
            "  fuzzy <字段名> <查询词> [最大编辑距离]            ：模糊查询，字段仅支持 title 或 content\n"
            "  add                                             ：添加新文档（弹出窗口交互）\n"
            "  delete <doc_id>                                 ：删除指定 doc_id 的文档\n"
            "  help                                            ：显示该帮助信息\n"
            "  exit                                            ：退出程序\n"
            "示例：\n"
            "  search 控油 AND 补水 1 5 title\n"
            "  fuzzy title Hyali 2\n"
        )
        return help_text
# ------------------------- 添加文档弹窗 -------------------------
class AddDocWindow:
    def __init__(self, master, ix, callback):
        """
        弹窗窗口，用于添加新文档。
        参数：
          master：主窗口；
          ix：索引对象；
          callback：回调函数，将添加结果输出到主窗口。
        """
        self.ix = ix
        self.callback = callback
        self.top = tk.Toplevel(master)
        self.top.title("添加新文档")
        self.top.grab_set()  # 模态对话框

        self.label_id = ttk.Label(self.top, text="文档ID：", font=("Arial", 11))
        self.label_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_id = ttk.Entry(self.top, width=40, font=("Arial", 11))
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)

        self.label_title = ttk.Label(self.top, text="标题：", font=("Arial", 11))
        self.label_title.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_title = ttk.Entry(self.top, width=40, font=("Arial", 11))
        self.ent_title.grid(row=1, column=1, padx=5, pady=5)

        self.label_content = ttk.Label(self.top, text="内容：", font=("Arial", 11))
        self.label_content.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ent_content = ttk.Entry(self.top, width=40, font=("Arial", 11))
        self.ent_content.grid(row=2, column=1, padx=5, pady=5)

        self.btn_ok = ttk.Button(self.top, text="确定", command=self.on_ok)
        self.btn_ok.grid(row=3, column=0, columnspan=2, pady=10)

    def on_ok(self):
        """获取输入信息，若有效则添加文档，并调用回调函数显示结果"""
        doc_id = self.ent_id.get().strip()
        title = self.ent_title.get().strip()
        content = self.ent_content.get().strip()
        if not doc_id or not title or not content:
            self.callback("错误：doc_id、标题、内容均不能为空。")
        else:
            add_or_update_documents(self.ix, [{"doc_id": doc_id, "title": title, "content": content}])
            self.callback(f"文档 {doc_id} 添加或更新成功。")
        self.top.destroy()
# ------------------------- 程序入口 -------------------------
def main():
    root = tk.Tk()
    app = SkincareSearchApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()





"""
import os
import jieba
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser
from whoosh.analysis import Tokenizer, Token
from whoosh.query import FuzzyTerm
# -------------------------------------------------------------------
# 1. jieba分词生成词元函数
# -------------------------------------------------------------------
def jieba_tokenizer_func(value):
    """
    jieba分词，将文本分割成词，逐个生成Whoosh可识别的Token
    """
    seg_list = jieba.cut(value, cut_all=False)
    for term in seg_list:
        token = Token()
        token.text = term
        yield token
def chinese_analyzer(value):
    """
    返回jieba_tokenizer_func结果，作为Whoosh自定义分析器
    """
    return jieba_tokenizer_func(value)

# -------------------------------------------------------------------
# 2. 定义Schema（doc_id唯一，title和content分词中文）
# -------------------------------------------------------------------

def define_schema():
    return Schema(
        doc_id=ID(stored=True, unique=True),
        title=TEXT(stored=True, analyzer=chinese_analyzer),
        content=TEXT(stored=True, analyzer=chinese_analyzer)
    )

# -------------------------------------------------------------------
# 3. 创建或打开索引目录及索引对象
# -------------------------------------------------------------------

def get_or_create_index(index_dir, schema):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return index.create_in(index_dir, schema)
    else:
        return index.open_dir(index_dir)

# -------------------------------------------------------------------
# 4. 添加或更新文档接口
# -------------------------------------------------------------------

def add_or_update_documents(ix, docs):
    writer = ix.writer()
    for doc in docs:
        writer.update_document(
            doc_id=doc["doc_id"],
            title=doc["title"],
            content=doc["content"],
        )
    writer.commit()

# -------------------------------------------------------------------
# 5. 删除文档函数，按doc_id删除
# -------------------------------------------------------------------

def delete_document(ix, doc_id):
    writer = ix.writer()
    writer.delete_by_term("doc_id", doc_id)
    writer.commit()

# -------------------------------------------------------------------
# 6. 搜索函数，支持分页、排序、多字段解析
# -------------------------------------------------------------------

def search_documents(ix, query_str, page=1, page_size=5, sort_field=None):
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "content"], schema=ix.schema)
        query = parser.parse(query_str)

        results = searcher.search(query, limit=None, sortedby=sort_field)
        total_results = len(results)
        start = (page - 1)*page_size
        end = start + page_size

        if start >= total_results:
            print(f"没有第 {page} 页内容，结果总数: {total_results}")
            return

        page_results = results[start:end]

        print(f"共找到 {total_results} 条结果，显示第 {page} 页（每页 {page_size} 条）:")
        print("-" * 40)
        for hit in page_results:
            print(f"Doc ID: {hit['doc_id']}")
            print(f"标题  : {hit['title']}")
            print(f"内容  : {hit['content']}")
            print("-" * 40)

# -------------------------------------------------------------------
# 7. 额外示范：模糊查询函数（因为Whoosh没内置模糊查询解析器，这里演示用searcher.query）
# -------------------------------------------------------------------

def search_fuzzy(ix, field, term, maxdist=1):
    with ix.searcher() as searcher:
        # 创建模糊查询对象
        query = FuzzyTerm(field, term, maxdist=maxdist)
        results = searcher.search(query)
        total_results = len(results)

        print(f"模糊查询Field:'{field}' Term:'{term}' 最大编辑距离={maxdist}，找到 {total_results} 条结果：")
        print("-" * 40)
        for hit in results:
            print(f"Doc ID: {hit['doc_id']}")
            print(f"标题  : {hit['title']}")
            print(f"内容  : {hit['content']}")
            print("-" * 40)
# -------------------------------------------------------------------
# 8. 主程序演示所有功能，包含各种查询示例
# -------------------------------------------------------------------
def main():
    index_dir = "w_skincare_index"
    print("Step1: 构建索引Schema")
    schema = define_schema()
    print("Step2: 创建或打开索引目录")
    ix = get_or_create_index(index_dir, schema)
    print("Step3: 添加护肤品数据文档")
    documents = [
        {
            "doc_id": "1",
            "title": "The Ordinary Niacinamide 10% + Zinc 1%",
            "content": "主要成分：烟酰胺10%、锌1%。功效：控油，收缩毛孔，抗炎，适合痘痘皮肤使用。",
        },
        {
            "doc_id": "2",
            "title": "The Ordinary Hyaluronic Acid 2% + B5",
            "content": "主要成分：透明质酸，维生素B5。功效：深层补水，修复肌肤屏障，适合干性及敏感皮肤。",
        },
        {
            "doc_id": "3",
            "title": "The Ordinary AHA 30% + BHA 2% Peeling Solution",
            "content": "主要成分：果酸30%，水杨酸2%。功效：物理去角质，提亮肤色，建议敏感肌慎用。",
        },
        {
            "doc_id": "4",
            "title": "Kiehl's Calendula Herbal Extract Toner",
            "content": "主要成分：金盏花提取物，甘油。功效：舒缓镇静，控油保湿，适合油性及敏感肌。",
        },
        {
            "doc_id": "5",
            "title": "La Roche-Posay Cicaplast Baume B5",
            "content": "主要成分：泛醇，修复成分。功效：修复屏障，缓解干燥，适合修复受损肌肤使用。",
        },
    ]
    add_or_update_documents(ix, documents)
    print("文档添加完毕。\n")
    print("\nStep4: 关键词‘烟酰胺’ 查询")
    search_documents(ix, "烟酰胺")
    print("\nStep5: 布尔查询 - 包含‘Whoosh’或者‘控油’（布尔 OR）")
    # 注意这里没Whoosh词，演示将改成‘控油 OR 补水’
    search_documents(ix, "控油 OR 补水")
    print("\nStep6: 短语查询 - 精确匹配‘全文检索’（示例换成‘修复屏障’）")
    search_documents(ix, '"修复屏障"')
    print("\nStep7: 通配符查询 - 查询以‘果’开头的词（例：果酸）")
    search_documents(ix, "果*")
    print("\nStep8: 模糊查询 - 查询标题中模糊匹配‘Hyali’（应该匹配Hyaluronic）")
    search_fuzzy(ix, "title", "Hyali", maxdist=2)
    print("\nStep9: 分页查询示例（关键词‘适合’，每页2条，第1页）")
    search_documents(ix, "适合", page=1, page_size=2, sort_field="title")
    print("\nStep10: 分页查询示例（关键词‘适合’，每页2条，第2页）")
    search_documents(ix, "适合", page=2, page_size=2, sort_field="title")
    print("\nStep11: 删除一条文档示例 - 删除 doc_id='1'")
    delete_document(ix, "1")
    print("删除后再搜索关键词‘烟酰胺’看看结果")
    search_documents(ix, "烟酰胺")
if __name__ == "__main__":
    main()
"""
