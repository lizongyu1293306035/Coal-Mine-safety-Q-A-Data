# coding:utf-8
"""
@Filename: bleu.py
@Description:
@Author: Li Zongyu
@Time: 2025/9/12 21:42
"""
import csv
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import jieba

# 确保已下载分词所需的数据
nltk.download('punkt', quiet=True)


def calculate_bleu_scores(candidate, references):
    """
    计算BLEU 1-4gram分数和整体BLEU分数

    参数:
    candidate: 模型生成的文本
    references: 参考文本列表

    返回:
    包含各分数和平均值的字典
    """

    # 替换word_tokenize部分
    candidate_tokens = list(jieba.cut(candidate))
    reference_tokens = [list(jieba.cut(references))]

    # 初始化平滑函数
    smoothie = SmoothingFunction().method4

    # 计算各n-gram的分数
    scores = {}
    for n in range(1, 5):
        weights = [0] * 4
        weights[n - 1] = 1
        score = sentence_bleu(reference_tokens, candidate_tokens,
                              weights=weights,
                              smoothing_function=smoothie)
        scores[f'BLEU-{n}'] = score

    # 计算整体BLEU分数（使用标准权重）
    overall_bleu = sentence_bleu(reference_tokens, candidate_tokens,
                                 weights=(0.25, 0.25, 0.25, 0.25),
                                 smoothing_function=smoothie)
    scores['BLEU-Avg'] = overall_bleu
    return scores


def save_bleu_to_csv(results, output_file='bleu_scores.csv'):
    """
    将BLEU分数保存到CSV文件

    参数:
    results: 结果列表，每个元素是包含文本和分数的字典
    output_file: 输出文件名
    """
    # 定义CSV列名
    fieldnames = ['ID', 'Candidate', 'Reference']
    if results:
        # 动态添加BLEU分数列名
        fieldnames.extend(list(results[0]['scores'].keys()))

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            row = {
                'Candidate': result['candidate'],
                'Reference': result['references']
            }
            # 添加所有BLEU分数
            row.update(result['scores'])
            writer.writerow(row)

    print(f"结果已保存到 {output_file}")


# 示例使用
if __name__ == "__main__":
    # 示例测试数据
    predict = "苹果发布了新一代iPhone手机"
    ground_truth = "苹果发布了最新款的iPhone智能手机"
    # 计算所有样本的BLEU分数
    all_results = []
    scores = calculate_bleu_scores(predict, ground_truth)
    result_entry = {
        'predict': predict,
        'ground_truth': ground_truth,
        'BLEU-1': scores["BLEU-1"],
        'BLEU-2': scores["BLEU-2"],
        'BLEU-3': scores["BLEU-3"],
        'BLEU-4': scores["BLEU-4"],
        'BLEU-Avg': scores["BLEU-Avg"],

    }
    all_results.append(result_entry)
    print(all_results)
    # 保存到CSV文件
    # save_bleu_to_csv(all_results, '煤矿安全模型_BLEU评测结果.csv')
