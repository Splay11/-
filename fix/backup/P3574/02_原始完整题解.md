### 思路

* **数据读取与预处理**: 输入为英文文本列表；统一小写、英文分词，去停用词。
* **特征表示**: 用 `TfidfVectorizer` 将每条文本转为 TF-IDF 向量（默认 L2 归一化），降低常见词权重、提升区分性词权重。
* **相似度计算**: 使用余弦相似度 $\text{cosine}(A,B)=\frac{A\cdot B}{\|A\|\,\|B\|}$ 衡量文本向量夹角，值域 \[0,1]。
* **结果格式**: 构造二维列表，元素为保留两位小数的字符串（如 `'0.24'`），对角线为 `'1.00'`。
### 代码
```python
from typing import List
import sys, ast, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def tfidf_cosine_similarity(texts: List[str]) -> List[List[str]]:
    """
    基于 TF-IDF 的文本两两余弦相似度矩阵（字符串两位小数）
    :param texts: 一维列表，每个元素为一条英文文本
    :return: 二维列表，相似度矩阵，每个元素为字符串形式的两位小数
    """
    # 边界处理：空列表
    if not texts:
        return []
    # 使用英文停用词，统一小写；默认 L2 归一化，使用 unigram
    vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 1), norm='l2')

    try:
        # 转为稀疏 TF-IDF 矩阵（文档数 × 词维度）
        tfidf = vectorizer.fit_transform(texts)
    except ValueError:
        # 若全部文本在去停用词后为空导致词汇表为空，则返回对角为 1，其余为 0 的矩阵
        n = len(texts)
        return [[("1.00" if i == j else "0.00") for j in range(n)] for i in range(n)]

    # 计算两两余弦相似度（文档数 × 文档数）
    sim = cosine_similarity(tfidf)

    # 将数值格式化为两位小数字符串
    formatted = [[f"{v:.2f}" for v in row] for row in sim]
    return formatted
def read_texts_from_stdin() -> List[str]:
    """
    从标准输入读取文本：
    1) 若输入以 '[' 开头，则按 JSON/字面量列表解析：["a", "b", ...]
    2) 否则按多行解析：每行一条文本，空行忽略，EOF 结束
    """
    data = sys.stdin.read().strip()
    if not data:
        return []
    if data.lstrip().startswith('['):
        # 先尝试 Python 字面量，再回退到 JSON
        try:
            return ast.literal_eval(data)
        except Exception:
            return json.loads(data)
    else:
        return [line for line in data.splitlines() if line.strip()]


if __name__ == "__main__":
    texts = read_texts_from_stdin()
    matrix = tfidf_cosine_similarity(texts)
    for row in matrix:
        print(row)
```