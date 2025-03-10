"""
迭代式挖掘/合并新模式, 更新 seed_patterns
"""
import json
import os
import re
from collections import defaultdict

def load_final_labeled_data(input_path):
    # 从 JSON 文件加载最终标注的数据
    with open(input_path, "r", encoding="utf-8") as file:
        return json.load(file)

def extract_common_patterns(data):
    # 分析最常见的文本结构和短语模板，生成新的模式
    pattern_counts = defaultdict(int)

    for item in data:
        operation = item["operation"].strip()
        if operation:
            pattern_counts[operation] += 1

    # 选出出现频率较高的操作模式（阈值可调整）
    threshold = 2  # 至少出现 2 次才认为是可靠模式
    refined_patterns = {op: [rf"\b{re.escape(op)}\b"] for op, count in pattern_counts.items() if count >= threshold}

    return refined_patterns

def update_seed_patterns():
    final_labeled_path = "data/final_labeled/final_labeled.json"
    seed_patterns_path = "pattern_mining/seed_patterns.py"
    output_path = "pattern_mining/refined_seed_patterns.py"

    # 读取最终标注数据
    labeled_data = load_final_labeled_data(final_labeled_path)

    # 提取新的模式
    new_patterns = extract_common_patterns(labeled_data)

    # 将新的模式合并到现有种子模式集合里
    with open(seed_patterns_path, "r", encoding="utf-8") as file:
        seed_patterns = {}
        exec(file.read(), {}, seed_patterns)

    # 确保 `seed_patterns` 存在并进行更新
    if "seed_patterns" in seed_patterns:
        for key, patterns in new_patterns.items():
            if key in seed_patterns["seed_patterns"]:
                seed_patterns["seed_patterns"][key].extend(patterns)
                seed_patterns["seed_patterns"][key] = list(set(seed_patterns["seed_patterns"][key]))  # 去重
            else:
                seed_patterns["seed_patterns"][key] = patterns

    # 转换为 Python 脚本格式
    seed_patterns_str = "seed_patterns = " + json.dumps(seed_patterns["seed_patterns"], indent=4, ensure_ascii=False)
    seed_patterns_str = seed_patterns_str.replace("\\\\", "\\")  # 确保格式正确

    # 保存更新后的模式文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("# 定义种子模式/种子正则\n\n" + seed_patterns_str)

    print(f"Updated seed patterns saved to {output_path}")