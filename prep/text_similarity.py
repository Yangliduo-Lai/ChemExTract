import xml.etree.ElementTree as ET
import numpy as np
from sentence_transformers import SentenceTransformer, util


def parse_xml(xml_path):
    """
    解析 XML 文件，提取 <Text> 节点，并按照页面组织文本，确保上下文完整。
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    page_texts = {}  # 按页存储文本
    for page in root.findall("Page"):
        page_number = page.get("number")
        text_elements = [text.text.strip() for text in page.findall("Text") if text.text]
        if text_elements:
            page_texts[page_number] = " ".join(text_elements)  # 连接同一页的文本

    return page_texts


def compute_similarity(text_dict):
    """
    计算文本相似性，返回相似度矩阵
    """
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")  # 轻量级的 SBERT 模型
    texts = list(text_dict.values())
    embeddings = model.encode(texts, convert_to_tensor=True)

    # 计算余弦相似度
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()

    return similarity_matrix, texts


def caculate_text_similarity(xml_path):
    text_dict = parse_xml(xml_path)
    similarity_matrix, texts = compute_similarity(text_dict)

    print("\n📌 计算文本相似度完成，输出结果如下：")
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            print(
                f"📄 Page {list(text_dict.keys())[i]} vs Page {list(text_dict.keys())[j]} → 相似度: {similarity_matrix[i][j]:.4f}")


