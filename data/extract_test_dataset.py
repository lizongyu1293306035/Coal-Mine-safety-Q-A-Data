# coding:utf-8
"""
@Filename: extract_test_dataset.py
@Description: 随机的从每个数据文件中抽取10条数据，并将这些数据写入到一个output.json文件中。

@Author: Li Zongyu
@Time: 2025/8/31 15:25
"""
import json
import glob


def extract_and_combine_json_files(input_pattern, output_file, samples_per_file=10):
    """
    从多个JSON文件中抽取数据并合并到一个输出文件中

    Args:
        input_pattern: 输入文件的匹配模式（如 "*.json"）
        output_file: 输出文件名
        samples_per_file: 每个文件抽取的样本数（默认10条）
    """
    # 获取所有匹配的JSON文件
    json_files = glob.glob(input_pattern)

    if not json_files:
        print("未找到任何JSON文件")
        return

    print(f"找到 {len(json_files)} 个JSON文件")

    all_data = []

    for file_path in json_files:
        try:
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查数据格式是否为列表
            if not isinstance(data, list):
                print(f"警告: {file_path} 的数据不是列表格式，跳过该文件")
                continue

            # 抽取指定数量的数据
            n_samples = min(samples_per_file, len(data))
            sampled_data = data[:n_samples]  # 取前n_samples条数据

            print(f"从 {file_path} 抽取了 {n_samples} 条数据")

            # 添加到总数据中
            all_data.extend(sampled_data)

        except json.JSONDecodeError:
            print(f"错误: {file_path} 不是有效的JSON文件，跳过")
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")

    # 将合并的数据写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        print(f"成功将 {len(all_data)} 条数据写入 {output_file}")

    except Exception as e:
        print(f"写入输出文件时出错: {str(e)}")


# 使用示例
if __name__ == "__main__":
    # 方法1: 使用通配符匹配所有JSON文件
    extract_and_combine_json_files(r"./processing_data/CoalQA_data*.json", r"./final_data/test.json", 10)
