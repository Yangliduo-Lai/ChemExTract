# 用微调好的 Flan-T5 去重新扫描语料，得到比种子模式匹配更丰富、更泛化的标注。

import os
import re
import json
import torch

from transformers import T5Tokenizer, T5ForConditionalGeneration

def load_finetuned_model(model_path="models/flan_t5_finetuned"):
    # 加载微调后的 Flan-T5 模型和 tokenizer
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return tokenizer, model, device


def predict_operation(sentence, tokenizer, model, device):
    # 使用微调后的 Flan-T5 预测化学操作
    input_text = f"question: What chemical operations are described in this sentence?  context: {sentence}"
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=50)

    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return predicted_text.split(", ")  # 确保多个操作可以正确拆分

def split_text_into_sentences(text):
    """使用正则表达式将文本拆分成句子"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def batch_predict_from_file(file_path= "data/raw/scientific_paragraphs.txt", output_path = "data/final_labeled/final_labeled.json", model_path="models/flan_t5_finetuned"):
    # 从文本文件中读取句子并批量预测化学操作，输出 JSON
    tokenizer, model, device = load_finetuned_model(model_path)

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    sentences = split_text_into_sentences(text)
    results = []

    for sentence in sentences:
        operations = predict_operation(sentence, tokenizer, model, device)
        for operation in operations:
            results.append({"sentence": sentence, "operation": operation})

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)

    print(f"Final labeled data saved to {output_path}")