import xml.etree.ElementTree as ET
import re
import importlib.util
import os

def clean_regex_keywords(patterns):
    cleaned = []
    for regex in patterns:
        s = regex.replace(r'\b', '')
        s = s.replace(r'\s+', ' ')
        s = re.sub(r'\\[a-z]+', '', s)
        s = re.sub(r'[^\w\s-]', '', s)
        s = s.strip()
        if len(s) > 1:
            cleaned.append(s)
    return list(set(cleaned))

def load_keywords_from_py(py_path):
    spec = importlib.util.spec_from_file_location("refined_seed_patterns", py_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    all_regex = []
    for group in module.seed_patterns.values():
        all_regex.extend(group)
    cleaned = clean_regex_keywords(all_regex)
    print(f"🔍 提取关键词数: {len(cleaned)}")
    return cleaned

def is_abstract_or_reference(paragraph):
    p_lower = paragraph.lower()
    abstract_indicators = ['abstract', '摘要']
    reference_indicators = ['references', 'reference list', 'et al.', 'doi:', 'https://doi.org/', '[1]', '(1)']

    if any(p_lower.startswith(a) for a in abstract_indicators):
        return True
    if any(ref in p_lower for ref in reference_indicators):
        return True
    if re.match(r'^\[\d+\]', paragraph.strip()):  # 形如 [1] 开头
        return True
    return False

def extract_experimental_paragraphs_from_xml(xml_path, keywords=None, output_path=None):
    if keywords is None:
        raise ValueError("必须提供关键词列表")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    all_text = []
    for page in root.findall('.//Page'):
        for text in page.findall('.//Text'):
            if text.text:
                all_text.append(text.text.strip())

    full_text = '\n'.join(all_text)

    # 拆分段落
    paragraphs = re.split(r'\n(?=[A-Z])', full_text)

    # 筛选关键词匹配段落
    experiment_paragraphs = [
        p for p in paragraphs
        if any(k in p for k in keywords) and not is_abstract_or_reference(p)
    ]

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            for para in experiment_paragraphs:
                f.write(para + '\n\n')

    return experiment_paragraphs

def run_extraction_pipeline(xml_path, keyword_py_path, output_path=None, preview_count=3):
    keywords = load_keywords_from_py(keyword_py_path)

    paragraphs = extract_experimental_paragraphs_from_xml(
        xml_path=xml_path,
        keywords=keywords,
        output_path=output_path
    )

    print(f"\n✅ 提取完成：共提取 {len(paragraphs)} 个实验相关段落（已排除 abstract 和 references）")
    if preview_count > 0:
        print("\n📌 示例段落：")
        for i, para in enumerate(paragraphs[:preview_count]):
            print(f"\n--- 段落 {i+1} ---\n{para.strip()}")

    return paragraphs
