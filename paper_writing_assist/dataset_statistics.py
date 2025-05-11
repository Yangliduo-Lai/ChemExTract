from collections import Counter
import re

# 读取文件内容
with open('/Users/cqmrl/PycharmProjects/ChemExTract/evaluation/rephrased_tgt.txt',
          'r',
          encoding='utf-8') as file:
    text = file.read()

# 匹配大写的action关键词（如 ADD、WAIT、SETTEMPERATURE 等）
actions = re.findall(r'\b[A-Z]{2,}\b', text)

# 统计每种动作的出现次数
action_counts = Counter(actions)

# 打印统计结果
if __name__=='__main__':
    for action in sorted(action_counts, key=lambda x: (x[0], x)):
        print(f"{action}: {action_counts[action]}")
