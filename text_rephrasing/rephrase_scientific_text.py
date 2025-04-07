import os
import openai
from pattern_mining.refined_seed_patterns import seed_patterns

# 设置 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def text_rephrase(input_path, output_path):
    # 检查 API key
    if not openai.api_key:
        raise ValueError("未设置 OpenAI API Key。请设置环境变量 OPENAI_API_KEY 或直接在代码中指定。")

    # 检查输入文件
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到输入文件: {input_path}")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 读取原始文本
    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read().strip()

    # 允许的动作类别（取 seed_patterns 顶层 key，全部大写）
    allowed_actions = [k.upper() for k in seed_patterns.keys()]

    # 构造 prompt
    prompt = f"""
You are a scientific protocol assistant.

Your job is to rewrite the following chemical procedure as a clear, structured, step-by-step protocol.

🔒 IMPORTANT RULES:
- You MUST use only the following action types as your step starters:
  {', '.join(allowed_actions)}
- The action must appear in ALL CAPS at the beginning of each step.
- Each step should be separated by a semicolon `;`.
- Additional details (reagents, solvents, time, temperature) can follow the action, written in normal English.
- If no chemical action is present, return: NOACTION
- If the text is in a non-English language, return: OTHERLANGUAGE

✅ Example format:
ADD (Reagent); WASH with (Solvent) (number of times); CONCENTRATE; FILTER (instruction).

📄 Original text:
{original_text}

✍️ Rewritten protocol:
"""

    # 调用 GPT-4 API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a chemistry assistant converting text into standardized lab protocol format using only allowed action types."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # 提取返回内容
    rephrased_text = response["choices"][0]["message"]["content"]

    # 写入输出文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rephrased_text.strip())

    print(f"✅ 改写完成，结果已保存到 {output_path}")
