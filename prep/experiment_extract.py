import numpy as np
import nltk
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer
import torch
from sklearn.cluster import AgglomerativeClustering
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

# 预定义化学实验相关的关键词
EXPERIMENT_KEYWORDS = [
    "experiment", "method", "procedure", "synthesis", "reaction", "experimental",
    "apparatus", "protocol", "sample preparation", "materials", "reagents",
    "titration", "chromatography", "spectroscopy", "extraction", "filtration",
    "precipitation", "solubility", "analysis", "measurement"
]

# 无关内容（如参考文献、致谢）
NON_RELEVANT_KEYWORDS = ["reference", "acknowledgment", "bibliography", "appendix"]


def parse_xml(xml_path):
    """
    解析 XML 文件，提取文本内容并返回句子列表
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    sentences = []
    for page in root.findall("Page"):
        for text in page.findall("Text"):
            if text.text:
                sentences.extend(sent_tokenize(text.text.strip()))  # 按句子分割文本
    return sentences


def compute_similarity_matrix(sentences):
    """
    计算句子相似度矩阵（使用 BERT 句向量）
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")  # 轻量级 BERT 模型
    embeddings = model.encode(sentences, convert_to_tensor=True)

    # 计算余弦相似度，并确保转换到 CPU
    similarity_matrix = torch.nn.functional.cosine_similarity(
        embeddings.unsqueeze(1), embeddings.unsqueeze(0), dim=2
    ).cpu().numpy()

    return similarity_matrix, embeddings

def cluster_sentences(embeddings, num_clusters=5):
    """
    使用层次聚类（Agglomerative Clustering）将句子分类
    """
    clustering_model = AgglomerativeClustering(n_clusters=num_clusters, metric="euclidean", linkage="ward")
    labels = clustering_model.fit_predict(embeddings.cpu().numpy())
    return labels

def extract_experimental_section(sentences, labels):
    """
    根据聚类结果提取实验部分，并去除无关内容（如参考文献、致谢等）
    """
    experimental_part = []
    non_experimental_part = []

    for i, sentence in enumerate(sentences):
        text_lower = sentence.lower()

        if any(keyword in text_lower for keyword in NON_RELEVANT_KEYWORDS):
            continue  # 跳过参考文献、致谢等

        if any(keyword in text_lower for keyword in EXPERIMENT_KEYWORDS) or labels[i] == 0:  # 假设实验部分属于 cluster 0
            experimental_part.append(sentence)
        else:
            non_experimental_part.append(sentence)

    return experimental_part, non_experimental_part


def experiment_text_extract(xml_path, output_txt_path="data/test/experiment_section.txt"):
    """
    解析 XML，提取实验部分，并写入 .txt 文件
    """
    # 1. 解析 XML 提取文本
    sentences = parse_xml(xml_path)

    # 2. 计算句子相似度矩阵
    similarity_matrix, embeddings = compute_similarity_matrix(sentences)

    # 3. 使用层次聚类进行文本分割s
    labels = cluster_sentences(embeddings, num_clusters=5)

    # 4. 提取实验部分 & 过滤无关内容
    experimental_part, non_experimental_part = extract_experimental_section(sentences, labels)

    # 5. 将实验部分写入 .txt 文件
    with open(output_txt_path, "w", encoding="utf-8") as file:
        file.write("\n".join(experimental_part))

    print(f"\n✅ 实验部分已提取并保存至 `{output_txt_path}`")
