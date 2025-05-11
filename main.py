import argparse
import os

from evaluation.extraction_evaluation import evaluation
from pdf_rephrasing.experiment_extract import run_extraction_pipeline
from pattern_mining.flan_t5_trainer import weak_label_data, generate_qa_training_data, fine_tune_flan_t5
from pattern_mining.pattern_labeler import batch_predict_from_file
from pattern_mining.pattern_refiner import update_seed_patterns
from pdf_rephrasing.pdf2xml import pdf_to_xml_pdfplumber
from text_rephrasing.rephrase_scientific_text import text_rephrase

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


# 数据准备
def run_text_pre():
    pdf_to_xml_pdfplumber(
        "data/raw_pdf_xml/McGrath et al. - Modulating the Potency of BRD4 PROTACs at the Systems Level with Amine-Acid Coupling Reactions.pdf",
        "data/raw_pdf_xml/paper.xml")

    xml_path = "data/raw_pdf_xml/paper.xml"
    keyword_path = "pattern_mining/refined_seed_patterns.py"
    output_path = "data/parsed_txt/experiment_paragraphs.txt"
    run_extraction_pipeline(xml_path, keyword_path, output_path)


# 文本格式化
# 文本重写
def run_text_rephrase(src_file="evaluation/src.txt",
                      result_file="evaluation/evaluation_results/gpt4.txt"):
    text_rephrase(src_file, result_file)



# 评估
def run_evaluation():
    # src_path = "evaluation/src.txt"
    # result_path = "evaluation/result.txt"
    #
    # temp_input = "evaluation/temp_input.txt"
    # temp_output = "evaluation/temp_output.txt"
    #
    # # 清空最终输出文件
    # open(result_path, 'w', encoding='utf-8').close()
    #
    # with open(src_path, 'r', encoding='utf-8') as src_file:
    #     for line in src_file:
    #         sentence = line.strip()
    #         if not sentence:
    #             continue
    #
    #         # 写入临时输入文件
    #         with open(temp_input, 'w', encoding='utf-8') as f_temp_in:
    #             f_temp_in.write(sentence + '\n')
    #
    #         # 调用改写函数
    #         text_rephrase(temp_input, temp_output)
    #
    #         # 读取改写后的结果并追加写入到最终结果文件
    #         with open(temp_output, 'r', encoding='utf-8') as f_temp_out:
    #             rephrased_line = f_temp_out.read().strip()
    #             with open(result_path, 'a', encoding='utf-8') as f_result:
    #                 f_result.write(rephrased_line + '\n')
    #
    # # 清理临时文件（可选）
    # os.remove(temp_input)
    # os.remove(temp_output)

    evaluation()


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

    # Text preparation
    parser_text_preparation = subparsers.add_parser("text_preparation", help="Run text preparation.")

    # Evaluation
    parser_evaluation = subparsers.add_parser("evaluation", help="Run evaluation.")

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
    elif args.command == "text_preparation":
        run_text_pre()
    elif args.command == "evaluation":
        run_evaluation()
    else:
        parser.print_help()
