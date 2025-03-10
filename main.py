import argparse

from pattern_mining.flan_t5_trainer import weak_label_data, generate_qa_training_data, fine_tune_flan_t5
from pattern_mining.pattern_labeler import batch_predict_from_file
from pattern_mining.pattern_refiner import update_seed_patterns
from text_formatting.format_text import format_experiment_description


# 模式识别
# 用现有的种子模式(seed_patterns.py)，在化学文献里自动搜索并“弱标注”出一些带操作标签的文本片段。
def run_weak_label_data():
    weak_label_data()

# 将这些标注过的句子对（原句 + 该句里有哪些操作与要素）整理成「问答式 (QA-style)」的训练样本。
def run_generate_qa_training_data():
    generate_qa_training_data()

# 微调 Flan-T5 Large 模型
def run_fine_tune_flan_t5():
    fine_tune_flan_t5()

# 使用微调后的 Flan-T5 预测化学操作
def run_Flan_T5_predict():
    batch_predict_from_file()

# 迭代式挖掘/合并新模式, 更新 seed_patterns
def run_update_seed_patterns():
    update_seed_patterns()



# 文本格式化
def run_text_format():
    format_experiment_description()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="Choose a sub-command to run.")

    # Pattern Mining
    # 1. weak_label_data
    parser_weak_label_data = subparsers.add_parser("weak_label_data", help="Run weak label data.")
    # 2. qa_training_data
    parser_qa_training_data = subparsers.add_parser("generate_qa_training_data", help="Run QA training data.")
    # 3. fine_tune_flan_t5
    parser_fine_tune_flan_t5 = subparsers.add_parser("fine_tune_flan_t5", help="Fine tune FlanT5 model.")
    # 4. flan_t5_predict
    parser_flan_t5_predict = subparsers.add_parser("Flan_T5_predict", help="Run FlanT5 model.")
    # 5. update_seed_patterns
    parser_update_seed_patterns = subparsers.add_parser("update_seed_patterns", help="Update seed patterns.")

    # Text Rephrasing
    parser_text_rephrasing = subparsers.add_parser("text_rephrase", help="Run text rephrase.")

    # Text Formatting
    parser_text_format = subparsers.add_parser("text_format", help="Run text format.")


    # 解析命令行参数
    args = parser.parse_args()

    # 根据子命令选择执行不同流程
    if args.command == "weak_label_data":
        run_weak_label_data()
    elif args.command == "generate_qa_training_data":
        run_generate_qa_training_data()
    elif args.command == "fine_tune_flan_t5":
        run_fine_tune_flan_t5()
    elif args.command == "Flan_T5_predict":
        run_Flan_T5_predict()
    elif args.command == "update_seed_patterns":
        run_update_seed_patterns()
    elif args.command == "text_rephrase":
        run_text_rephrase()
    elif args.command == "text_format":
        run_text_format()
    else:
        parser.print_help()
