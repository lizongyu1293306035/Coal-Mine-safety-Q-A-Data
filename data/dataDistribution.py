# coding:utf-8
"""
@Filename: dataDistribution.py
@Description: 计算数据分布
@Author: Li Zongyu
@Time: 2025/10/16 20:26
"""
import json
import pandas as pd

file_path = r"./final_data/data.json"

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
q_len_distribution = {}
a_len_distribution = {}

for conv in data["conversations"]:
    human_value = conv[0]["value"]
    gpt_value = conv[1]["value"]
    human_value_len = len(human_value)
    gpt_value_len = len(gpt_value)

    if human_value_len in q_len_distribution.keys():
        q_len_distribution[human_value_len] += 1
    else:
        q_len_distribution[human_value_len] = 1

    if gpt_value_len in a_len_distribution.keys():
        a_len_distribution[gpt_value_len] += 1
    else:
        a_len_distribution[gpt_value_len] = 1


def save_map_to_excel(data_map, filename='./data_distribution/map_data.xlsx'):
    """
    将map保存到xlsx文件

    参数:
    data_map: 要保存的字典
    filename: 保存的文件名
    """
    try:
        # 将map转换为DataFrame
        df = pd.DataFrame({
            'length': list(data_map.keys()),
            'count': list(data_map.values())
        })

        # 保存到xlsx文件
        df.to_excel(filename, index=False)
        print(f"map已成功保存到 {filename} 文件")
        print("数据内容：")
        print(df)

    except Exception as e:
        print(f"保存文件时出错: {e}")


save_map_to_excel(q_len_distribution, r"./data_distribution/question_distribution.xlsx")
save_map_to_excel(a_len_distribution, r"./data_distribution/answer_distribution.xlsx")
