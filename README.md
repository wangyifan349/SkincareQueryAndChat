# 护肤品查询与问答应用

这是一个基于 Flask 的简单 Web 应用程序，提供护肤品信息查询和问答功能。该应用支持中文和英文输入，并结合使用 LCS 和 TF-IDF 算法处理文本相似性。

## 功能

- **产品搜索**：
  - 通过产品名称进行搜索，展示详细的产品信息，如名称、类型及描述。
- **问答聊天**：
  - 输入问题，返回最匹配的答案。
  - 支持 LCS 和 TF-IDF 算法，确保响应的准确性。
- **多语言支持**：
  - 支持中文和英文输入，使用 `jieba` 库进行中文分词。

## 项目结构

```
/SkincareQueryAndChat
    /templates
        layout.html
        index.html
        product_detail.html
        chat.html
    app.py
    data.py
    requirements.txt
```

- **app.py**：主程序文件，定义了 Flask 应用的路由和逻辑。
- **data.py**：包含产品和问答数据的硬编码数据库。所有用于查询和交互的数据均存储在此文件中。
- **templates/**：存放 HTML 模板文件，其中内嵌了 CSS 样式，用来定义页面布局和主题色彩。

## 数据说明 (data.py)

`data.py` 中存储了应用程序用来提供查询和问答的硬编码数据。以下是一些示例问答：

- **问题**：What is aspirin used for and how does it work?
  - **答案**：Aspirin is commonly used to reduce pain, fever, or inflammation. It is also used as an antiplatelet drug to prevent blood clots, which can help prevent heart attacks and strokes. Aspirin works by blocking the production of certain natural substances that cause inflammation and reduce blood clotting in the circulatory system.
  
- **问题**：How does benzoyl peroxide help in treating acne?
  - **答案**：Benzoyl peroxide helps treat acne by acting as a peeling agent, increasing skin turnover and clearing pores, thus reducing bacterial count and inflammation. It introduces oxygen, creating an environment where acne-causing bacteria cannot survive.

请注意，所有问答数据和产品信息都存储在 `data.py` 文件中，应用程序通过读取这些数据来提供相应的功能。

请补充数据至 data.py，例如医疗数据、护肤品相关信息或其他您专业领域的数据！

## 安装说明

为了成功运行应用，请确保在全局 Python 环境中安装以下依赖项。

1. **克隆仓库**：

   ```bash
   git clone https://github.com/wangyifan349/SkincareQueryAndChat.git
   cd SkincareQueryAndChat
   ```
2. **安装依赖**：
   运行以下命令安装所需的 Python 包：
   ```bash
   pip install -r requirements.txt
   ```
## 运行应用

1. **启动应用**：

   使用以下命令启动 Flask 开发服务器：
   ```bash
   python app.py
   ```
2. **访问应用**：
   打开你的浏览器，访问 `http://127.0.0.1:5000` 查看应用。
## 使用指南

- **主页**：使用产品搜索功能查找特定产品。
- **产品详情**：点击产品名称查看详细信息。
- **聊天页面**：输入问题，基于最接近匹配的预定义问题提供响应。

## 贡献

欢迎贡献！如有任何改进或漏洞修复，请随时 fork 此仓库并提交 pull request。

## 许可

此项目基于 BSD 3-Clause 许可证。有关详细信息，请查阅 `LICENSE` 文件。

## 致谢

特别感谢所有贡献者及此项目中使用的库的开发者，包括 Flask、scikit-learn、jieba 和 numpy。

最后，向所有用户致以谢意。
