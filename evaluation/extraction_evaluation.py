import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher
from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from Levenshtein import ratio
from difflib import SequenceMatcher

from text_rephrasing.rephrase_scientific_text import text_rephrase

def compute_bleu_score(gt_actions, extracted_actions):
    reference = [word_tokenize(" ".join(gt_actions))]
    candidate = word_tokenize(" ".join(extracted_actions))
    return sentence_bleu(reference, candidate, smoothing_function=SmoothingFunction().method1)

def compute_levenshtein_similarity(gt_actions, extracted_actions):
    gt_text = " ".join(gt_actions)
    extracted_text = " ".join(extracted_actions)
    return ratio(gt_text, extracted_text)

def fuzzy_match(a, b, threshold=0.75):
    return SequenceMatcher(None, a, b).ratio() >= threshold

def compute_f1(gt_actions, extracted_actions, threshold=0.75):
    matched_gt = set()
    matched_extracted = set()

    for i, e_action in enumerate(extracted_actions):
        for j, g_action in enumerate(gt_actions):
            if fuzzy_match(e_action, g_action, threshold):
                matched_extracted.add(i)
                matched_gt.add(j)
                break

    TP = len(matched_extracted)
    FP = len(extracted_actions) - TP
    FN = len(gt_actions) - TP
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    return round(precision, 4), round(recall, 4), round(f1, 4)

def build_action_graph(actions):
    G = nx.DiGraph()
    prev_action = None
    for i, action in enumerate(actions):
        G.add_node(i, label=action)
        if prev_action is not None:
            G.add_edge(prev_action, i)
        prev_action = i
    return G

def compute_graph_matching_score(gt_actions, extracted_actions):
    G_gt = build_action_graph(gt_actions)
    G_extracted = build_action_graph(extracted_actions)
    GM = DiGraphMatcher(G_gt, G_extracted)
    Gsub_nodes = max([set(m.values()) for m in GM.subgraph_isomorphisms_iter()], key=len, default=set())
    return len(Gsub_nodes) / max(len(G_gt.nodes), len(G_extracted.nodes)) if max(len(G_gt.nodes), len(G_extracted.nodes)) > 0 else 0

def compute_seqmatch_o(gt_actions, extracted_actions):
    gt_operations = [action.split()[0] for action in gt_actions]
    extracted_operations = [action.split()[0] for action in extracted_actions]
    matches = sum(1 for op in extracted_operations if op in gt_operations)
    return matches / max(len(gt_operations), len(extracted_operations)) if max(len(gt_operations), len(extracted_operations)) > 0 else 0

def compute_seqmatch_a(gt_actions, extracted_actions):
    matches = sum(1 for action in extracted_actions if action in gt_actions)
    return matches / max(len(gt_actions), len(extracted_actions)) if max(len(gt_actions), len(extracted_actions)) > 0 else 0

def evaluation():
    # file_path = "evaluation/result.txt"
    # file_path = "evaluation/evaluation_results/Paragraph2Actions.txt"
    # file_path = "evaluation/evaluation_results/ChemTrans.txt"
    # file_path = "evaluation/evaluation_results/gpt4.txt"
    # file_path = "evaluation/evaluation_results/qwen_max.txt"
    # file_path = "evaluation/evaluation_results/deepseek.txt"
    file_path = "evaluation/evaluation_results/ERNIE.txt"

    # ground_truth_file = "evaluation/tgt.txt"
    ground_truth_file = "evaluation/rephrased_tgt.txt"

    with open(file_path, 'r', encoding='utf-8') as f_pred, open(ground_truth_file, 'r', encoding='utf-8') as f_gt:
        pred_lines = [line.strip() for line in f_pred if line.strip()]
        gt_lines = [line.strip() for line in f_gt if line.strip()]

    assert len(pred_lines) == len(gt_lines), "预测结果与参考答案行数不一致"

    total_bleu = 0
    total_lev = 0
    total_graph = 0
    total_prec, total_rec, total_f1 = 0, 0, 0
    total_smo, total_sma = 0, 0
    n = len(gt_lines)

    for gt, pred in zip(gt_lines, pred_lines):
        gt_actions = [a.strip() for a in gt.split(';') if a.strip()]
        pred_actions = [a.strip() for a in pred.split(';') if a.strip()]

        total_bleu += compute_bleu_score(gt_actions, pred_actions)
        total_lev += compute_levenshtein_similarity(gt_actions, pred_actions)
        total_graph += compute_graph_matching_score(gt_actions, pred_actions)
        prec, rec, f1 = compute_f1(gt_actions, pred_actions)
        total_prec += prec
        total_rec += rec
        total_f1 += f1
        total_smo += compute_seqmatch_o(gt_actions, pred_actions)
        total_sma += compute_seqmatch_a(gt_actions, pred_actions)

    print(f"BLEU Score: {total_bleu / n:.4f}")
    print(f"Levenshtein Similarity Score: {total_lev / n:.4f}")
    print(f"Precision: {total_prec / n:.4f}, Recall: {total_rec / n:.4f}, F1: {total_f1 / n:.4f}")
    print(f"Graph Matching Similarity Score: {total_graph / n:.4f}")
    print(f"SM-O Score: {total_smo / n:.4f}")
    print(f"SM-A Score: {total_sma / n:.4f}")
