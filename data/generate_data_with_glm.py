# coding:utf-8
"""
@Filename: generate_data.py
@Description: 处理源数据, 使用glm4
@Author: Li Zongyu
@Time: 2025/8/27 21:47
"""
import json
from tqdm import tqdm
from zhipuai import ZhipuAI
from openai import OpenAI

with open("../apikey/glm.txt", "r", encoding="utf-8") as fp:
    apikey = fp.read()
client = ZhipuAI(api_key=apikey)
output_file_path = "processing_data/CoalQA_data11.json"
raw_data_file_name = "11-煤矿井下运输设计规范.txt"
with open('./raw_data/' + raw_data_file_name, 'r', encoding='utf-8') as f:
    content = f.read()


def return_random_prompt(chunk: str):
    system_prompt = "根据下面提供的{}一段文本，".format(raw_data_file_name)
    system_prompt += "请你仔细阅读给定的文本，你需要依据该文本：\n\n######\n{}######\n尽可能给出多样化的问题和对应的回答。我们将用于人工评估GLM-4模型对问答对数据的完成情况。要求:\n".format(
        chunk)
    system_prompt += "1. 生成问题有价值且遵守该文本信息，回答准确专业。\n"
    system_prompt += "2. 生成问答对不能重复。\n"
    system_prompt += "3. 问题多样化，同个问题可以换成不同表述方式，但意思保持不变。\n"
    system_prompt += "4. 为问题生成作为<input>，不应该只包含简单的占位符。<input>应提供实质性的内容问题，具有挑战性且较为复杂的问题。"
    system_prompt += "5. <output>应该是对问题的适当且真实的回答，不能只回复答应或拒绝请求。如果需要额外信息才能回复时，请努力预测用户意图并尝试回复，但不能胡编乱造，请严格按照给定文本生成问答对，禁止生成超出给定文本的任何问答对。"
    system_prompt += "6. <output>应该回答完整不能有省略号；\n"
    system_prompt += "7. 问答对应覆盖文本的所有信息\n"
    system_prompt += "8. 请不要生成“根据第几条”,“根据相关规定”这种指代不明的问题”\n"
    system_prompt += "9. 不需要使用```json ```。\n\n"
    system_prompt += "输出案例如下:"
    system_prompt += """[
    {
        "<input>": "县级以上人民政府管理矿山企业的主管部门对矿山安全工作应该行使哪些管理职责?", 
        "<output>": "(一)检查矿山企业贯彻执行矿山安全法律、法规的情况；(二)审查批准矿山建设工程安全设施的设计；(三)负责矿山建设工程安全设施的竣工验收；(四)组织矿长和矿山企业安全工作人员的培训工作；(五)调查和处理重大矿山事故；(六)法律、行政法规规定的其他管理职责。"
    }
]"""
    system_prompt += "请给出满足条件的JSON格式数据，并存储在一个列表中，便于整理使用，不要输出非法的字符，只要列表形式存储JSON数据\n"
    return system_prompt


if __name__ == '__main__':
    output_file = open(output_file_path, 'w', encoding='utf-8')
    chunk_list = content.split(r"\n")
    output_file.write("[\n")
    for i in tqdm(range(len(chunk_list))):
        qa_list = []
        max_retries = 5
        retry_count = 0
        success = False
        while not success and retry_count < max_retries:

            content = client.chat.completions.create(
                model="glm-4-flash-250414",
                messages=
                [
                    {
                        "role": "user",
                        "content": return_random_prompt(chunk_list[i])
                    }
                ],
                top_p=0.7,
                temperature=0.9,
                stream=False,
                max_tokens=2500,
            ).choices[0].message.content
            if content != '':
                try:
                    qa_list = json.loads(content)
                    success = True
                except json.JSONDecodeError as e:
                    retry_count += 1
                    print(f"解析失败: {chunk_list[i]}，错误: {e}，重试 {retry_count}/{max_retries}")
                    continue

        for j in range(len(qa_list)):
            output_file.write(json.dumps(qa_list[j], ensure_ascii=False))
            is_qaList_end = j == len(qa_list) - 1
            is_chunkList_end = i == len(chunk_list) - 1
            if not (is_chunkList_end and is_qaList_end):
                output_file.write(",")
            output_file.write("\n")
    output_file.write("]")
    output_file.close()
