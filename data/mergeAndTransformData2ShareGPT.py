# coding:utf-8
"""
@Filename: mergeAndTransformData2ShareGPT.py
@Description: 将数据转换为ShareGPT风格结构数据
@Author: Li Zongyu
@Time: 2025/8/29 17:18
"""
import glob
import json
import os.path
import random
from typing import List

import tqdm


def transform_data_2_shareGPT(data: List[dict], file_index: int) -> List[List[dict]]:
    """
    将数据转换为shareGPT格式

    :param data: 数据列表
    :param file_index: 文件索引号，用于数据的调试纠错
    :return: shareGPT 格式的数据列表
    """
    transformed_data = []
    for item in data:

        try:
            temp_list = [{
                "from": "human",
                "value": item["<input>"]
            }, {
                "from": "gpt",
                "value": item["<output>"]
            }]
        except KeyError:
            print("file:" + str(file_index))
            print("Line " + str(data.index(item)) + " has problem!")
            break

        transformed_data.append(temp_list)
    # 构建最终输出结构
    return transformed_data


def merge_and_transform_data_2_shareGPT(data_folder_path: str, output_file_path: str, shuffle: bool = False):
    """
    合并 data_folder_path 文件夹下的所有数据到 output_file_path文件中。

    :param data_folder_path: 数据文件夹
    :param output_file_path: 输出文件名
    :param shuffle: 是否洗牌, 默认为 False
    :return: None
    """
    if not os.path.exists(data_folder_path):
        print(data_folder_path + "该文件路径不存在！")
        return

    pattern = os.path.join(data_folder_path, "CoalQA_data*.json")
    json_files = glob.glob(pattern)
    json_files.sort(key=lambda x: int(os.path.basename(x).split('CoalQA_data')[1].split('.json')[0]))
    if not json_files:
        print(f"在文件夹 '{data_folder_path}' 中未找到CoalQA_data*.json文件")
        return False

    print(f"找到 {len(json_files)} 个json文件")

    final_data = {"conversations": []}

    # 遍历每个文件并读取其中的数据
    for file_path in tqdm.tqdm(json_files):
        with open(file_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        final_data["conversations"].extend(transform_data_2_shareGPT(data, json_files.index(file_path)))

    if shuffle:
        random.shuffle(final_data["conversations"])

    # 写入文件中
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    data_file = r"P:\Desktop\小论文写作\code\data\final_data\data.json"
    merge_and_transform_data_2_shareGPT(data_folder_path=r"P:\Desktop\小论文写作\code\data\processing_data",
                                        output_file_path=data_file,
                                        shuffle=True)
    with open(data_file, "r", encoding="utf-8") as fp:
        data = json.load(fp)

    print("数据总条数:" + str(len(data["conversations"])))
