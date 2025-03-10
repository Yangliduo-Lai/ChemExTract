import re
import openai

# 读取种子模式
from pattern_mining.refined_seed_patterns import seed_patterns



def match_patterns(text, patterns):
    """ 在文本中匹配模式，并返回匹配的操作类型 """
    matched_actions = []
    for action, regex_list in patterns.items():
        for regex in regex_list:
            if re.search(regex, text, re.IGNORECASE):
                matched_actions.append(action)
                break  # 一个动作匹配一个即可
    return matched_actions

def text_rephrase():
    # 读取科学文本
    with open("data/raw/test_scientific_paragraphs.txt", "r", encoding="utf-8") as f:
        original_text = f.read()

    # 识别文本中的操作模式
    actions = match_patterns(original_text, seed_patterns)

    # Construct GPT-4 prompt
    prompt = f"""
    You are a scientific paper editing assistant. Please rewrite the following chemical synthesis steps while preserving key procedural steps and ensuring clarity. Format the output as a structured step-by-step protocol similar to the following:

    Example format:
    ADD [Reagent]
    WASH with [Solvent] [number of times]
    DRYSOLUTION over [Drying Agent]
    FILTER [instruction]
    CONCENTRATE
    YIELD [Product Information]

    Original text:
    {original_text}

    Identified action patterns:
    {', '.join(actions)}

    Please ensure that:
        1. The language remains in English, using a structured and clear format.
        2. Abbreviations are expanded (e.g., m.p. should be rewritten as melting point).
        3. Key procedural steps are retained and formatted clearly.
        4. Synonyms for procedural actions are replaced with standardized terminology.
        5. Maintain a structured step-by-step format as shown in the example.

    Rewritten text:
    """

    # 调用 GPT-4 API 进行改写
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a chemistry lab assistant, helping to refine experimental procedures."},
            {"role": "user", "content": prompt}
        ]
    )

    rephrased_text = response["choices"][0]["message"]["content"]

    # 保存到新文件
    with open("data/raw/rephrased_scientific_paragraphs.txt", "w", encoding="utf-8") as f:
        f.write(rephrased_text)

    print("改写完成，结果已保存到 data/raw/rephrased_scientific_paragraphs.txt")
