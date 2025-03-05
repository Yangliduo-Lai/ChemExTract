import os
import pandas as pd

def format_experiment_description():
    input_file = "data/raw/rephrased_scientific_paragraphs.txt"
    output_file = "output/formatted_text.csv"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        steps = []
        for line in lines:
            step_description = line.lstrip("0123456789. ").strip()
            if step_description:
                steps.append([step_description])

        # 创建 DataFrame
        df = pd.DataFrame(steps, columns=["Experiment Steps"])

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # 保存为 CSV 文件
        df.to_csv(output_file, index=False, encoding='utf-8')

        print(f"Formatted table has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")