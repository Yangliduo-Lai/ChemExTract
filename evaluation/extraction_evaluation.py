import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher
from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from Levenshtein import ratio
from difflib import SequenceMatcher

from text_rephrasing.rephrase_scientific_text import text_rephrase


def read_actions_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    actions = [line.strip() for line in lines if line.strip()]
    return actions

def compute_bleu_score(gt_actions, extracted_actions):
    # 分词处理
    reference = [word_tokenize(" ".join(gt_actions))]
    candidate = word_tokenize(" ".join(extracted_actions))
    bleu_score = sentence_bleu(reference, candidate)
    return bleu_score

def compute_levenshtein_similarity(gt_actions, extracted_actions):
    gt_text = " ".join(gt_actions)
    extracted_text = " ".join(extracted_actions)
    return ratio(gt_text, extracted_text)

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
    score = len(Gsub_nodes) / max(len(G_gt.nodes), len(G_extracted.nodes)) if len(G_gt.nodes) > 0 else 0
    return score

def fuzzy_match(a, b, threshold=0.75):
    return SequenceMatcher(None, a, b).ratio() >= threshold

def compute_seqmatch_o(gt_actions, extracted_actions):
    gt_operations = [action.split()[0] for action in gt_actions]
    extracted_operations = [action.split()[0] for action in extracted_actions]
    matches = sum(1 for op in extracted_operations if op in gt_operations)
    return matches / max(len(gt_operations), len(extracted_operations)) if max(len(gt_operations), len(extracted_operations)) > 0 else 0

def compute_seqmatch_a(gt_actions, extracted_actions):
    matches = sum(1 for action in extracted_actions if action in gt_actions)
    return matches / max(len(gt_actions), len(extracted_actions)) if max(len(gt_actions), len(extracted_actions)) > 0 else 0

def evaluation():
    file_path = "result.txt"
    ground_truth_file = "tgt.txt"
    ground_truth_actions = read_actions_from_file(ground_truth_file)
    extracted_actions = read_actions_from_file(file_path)

    graph_score = compute_graph_matching_score(ground_truth_actions, extracted_actions)
    bleu_score = compute_bleu_score(ground_truth_actions, extracted_actions)
    levenshtein_score = compute_levenshtein_similarity(ground_truth_actions, extracted_actions)
    fuzzy_precision, fuzzy_recall, fuzzy_f1 = compute_f1(ground_truth_actions, extracted_actions)
    smo_score = compute_seqmatch_o(ground_truth_actions, extracted_actions)
    sma_score = compute_seqmatch_a(ground_truth_actions, extracted_actions)

    print(f"BLEU Score: {bleu_score:.4f}")
    print(f"Levenshtein Similarity Score: {levenshtein_score:.4f}")
    print(f"Precision: {fuzzy_precision:.4f}, Recall: {fuzzy_recall:.4f}, F1: {fuzzy_f1:.4f}")
    print(f"Graph Matching Similarity Score: {graph_score:.4f}")
    print(f"SM-O Score: {smo_score:.4f}")
    print(f"SM-A Score: {sma_score:.4f}")
