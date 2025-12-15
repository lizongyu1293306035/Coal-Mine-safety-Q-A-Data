# coding:utf-8
"""
@Filename: demo.py
@Description:
@Author: Li Zongyu
@Time: 2025/9/13 12:11
"""
import os
from typing import List, Dict, Any
import csv


def write_to_csv(data: List[Dict[str, Any]], filename: str, mode: str = 'w', encoding: str = 'utf-8-sig'):
    """
    公共的方法，将数据保存为csv文件

    :param data: 数据
    :param filename: 输出的文件名
    :param mode: 模式
    :param encoding: 编码
    :return:
    """
    if not data:
        print("警告：数据为空，未写入文件")
        return False
    try:
        fieldnames = set()
        fieldnames.update(data[0].keys())
        fieldnames = sorted(list(fieldnames))

        # 检查文件是否存在，以决定是否需要写入表头
        file_exists = os.path.isfile(filename)
        with open(filename, mode, newline='', encoding=encoding) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # 如果是新文件或者覆盖模式，写入表头
            if mode == 'w' or not file_exists:
                writer.writeheader()

            # 写入数据
            for item in data:
                # 确保每个数据项都包含所有字段，缺失字段用空字符串填充
                row = {field: item.get(field, '') for field in fieldnames}
                writer.writerow(row)
        print(f"数据已成功写入 {filename}")
        return True
    except Exception as e:
        print(f"写入CSV文件时出错: {e}")
        return False
