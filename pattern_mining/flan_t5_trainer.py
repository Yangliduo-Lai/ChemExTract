"""
这里是微调 Flan-T5 的脚本。将弱标注的训练数据整理成 QA 格式后，用 huggingface Trainer 训练。
"""
import os
import re
import json
import torch

from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset

"""
用现有的种子模式(seed_patterns.py)，在化学文献里自动搜索并“弱标注”出一些带操作标签的文本片段。
"""
def weak_label_data():
    # 文件路径
    input_text_file = "data/raw/scientific_paragraphs.txt"
    pattern_file = "pattern_mining/seed_patterns.py"
    output_json_file = "data/weak_labeled/weak_labeled.json"

    # 读取种子模式
    pattern_globals = {}
    with open(pattern_file, "r", encoding="utf-8") as f:
        exec(f.read(), pattern_globals)  # 解析 Python 文件
    seed_patterns = pattern_globals["seed_patterns"]

    # 读取科学段落文本
    with open(input_text_file, "r", encoding="utf-8") as f:
        text = f.read()

    # 按句子分割文本
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # 提取实验操作
    extracted_operations = []
    for sentence in sentences:
        for operation, patterns in seed_patterns.items():
            for pattern in patterns:
                if re.search(pattern, sentence, flags=re.IGNORECASE):
                    extracted_operations.append({
                        "sentence": sentence,
                        "operation": operation
                    })
                    break  # 防止同一句匹配多个相同类别

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_json_file), exist_ok=True)

    # 保存到 JSON 文件
    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(extracted_operations, f, indent=4, ensure_ascii=False)

    print(f"Extracted experimental operations saved to {output_json_file}")

"""
将标注过的句子对（原句 + 该句里有哪些操作）整理成「问答式 (QA-style)」的训练样本。
"""
def generate_qa_training_data():
    input_json_file = "data/weak_labeled/weak_labeled.json"
    output_json_file = "data/weak_labeled/qa_training_data.json"

    # 读取弱标注数据
    with open(input_json_file, "r", encoding="utf-8") as file:
        weak_labeled_data = json.load(file)

    qa_data = []
    seen_sentences = {}

    # 处理标注数据
    for item in weak_labeled_data:
        sentence = item["sentence"]
        operation = item["operation"]

        if sentence not in seen_sentences:
            seen_sentences[sentence] = []
        seen_sentences[sentence].append(operation)

    # 生成 QA 样本
    for sentence, operations in seen_sentences.items():
        qa_sample = {
            "question": f"What chemical operations are described in this sentence?",
            "context": sentence,
            "answer": ", ".join(operations)
        }
        qa_data.append(qa_sample)

    # 确保目标目录存在
    os.makedirs(os.path.dirname(output_json_file), exist_ok=True)

    # 保存问答数据
    with open(output_json_file, "w", encoding="utf-8") as file:
        json.dump(qa_data, file, indent=4, ensure_ascii=False)

    print(f"QA training data saved to {output_json_file}")

"""
微调一个 Flan-T5 Small 模型。
"""
def load_data(data_path):
    with open(data_path, "r", encoding="utf-8") as file:
        qa_data = json.load(file)

    return Dataset.from_dict({
        "question": [item["question"] for item in qa_data],
        "context": [item["context"] for item in qa_data],
        "answer": [item["answer"] for item in qa_data],
    })

def preprocess_data(example, tokenizer, max_length=512):
    inputs = [f"question: {q}  context: {c}" for q, c in zip(example["question"], example["context"])]
    model_inputs = tokenizer(inputs, max_length=max_length, padding="max_length", truncation=True)
    labels = tokenizer(example["answer"], max_length=max_length, padding="max_length", truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


def fine_tune_flan_t5(model_name = "google/flan-t5-small"):
    train_path ="data/weak_labeled/qa_training_data.json"
    output_dir = "models/flan_t5_finetuned"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)

    dataset = load_data(train_path)
    tokenized_dataset = dataset.map(lambda x: preprocess_data(x, tokenizer), batched=True)

    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="no",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        num_train_epochs=3,
        weight_decay=0.01,
        save_total_limit=2,
        fp16=False,
        push_to_hub=False,
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model fine-tuned and saved to {output_dir}")