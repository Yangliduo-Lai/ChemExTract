import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pattern_mining.refined_seed_patterns import seed_patterns

# 加载 Galactica 模型和分词器
tokenizer = AutoTokenizer.from_pretrained("facebook/galactica-1.3b")
model = AutoModelForCausalLM.from_pretrained("facebook/galactica-1.3b")
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def text_rephrase(input_path, output_path):
    # 检查输入文件
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到输入文件: {input_path}")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 读取原始文本
    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read().strip()

    allowed_actions = [k.upper() for k in seed_patterns.keys()]

    prompt = f"""
You are a scientific protocol assistant.

Your job is to rewrite the following chemical procedure as a clear, structured, step-by-step protocol.

IMPORTANT RULES:
- Use only these action types at the beginning of each step:
  {', '.join(allowed_actions)}
- Each action must be in ALL CAPS.
- Steps should be separated by a semicolon `;`.
- Add any necessary details like reagent, solvent, time, temperature.
- If no chemical action: return NOACTION
- If the text is not in English: return OTHERLANGUAGE

Example:
ADD (Reagent); WASH with (Solvent) (number of times); CONCENTRATE; FILTER (instruction).

Original:
{original_text}

Rewritten protocol:
"""

    # 编码输入
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).to(device)

    # 移除不必要的字段
    inputs.pop("token_type_ids", None)  # 安全地移除该字段

    # 生成输出
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )

    # 解码生成的文本（去掉 prompt 部分）
    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    rephrased_text = full_text[len(prompt):].strip()

    # 写入输出文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rephrased_text)

    print(f"✅ 改写完成，结果已保存到 {output_path}")

# 修改这里的路径为你自己的文件
if __name__ == "__main__":
    input_file = "/Users/cqmrl/PycharmProjects/ChemExTract/evaluation/src.txt"
    output_file = "/Users/cqmrl/PycharmProjects/ChemExTract/evaluation/evaluation_results/galactica.txt"
    text_rephrase(input_file, output_file)
