# coding:utf-8
"""
@Filename: QATypeFliter.py
@Description: 问答对类型筛选
@Author: Li Zongyu
@Time: 2025/10/18 13:40
"""

import json
from tqdm import tqdm
from openai import OpenAI

prompt_template = """给定如下问答对：
问题：{question}
答案：{answer}

请判断给定的问题术语属于以下哪类问题：

煤矿安全法规制度类问题；
煤矿安全操作规程类问题；
煤矿安全名词术语解释类问题；

仅回答问题类型即可，输出的文本不应带有标点符号。
"""

# 问题类型列表
qa_type_list = [
    "煤矿安全法规制度类问题",
    "煤矿安全操作规程类问题",
    "煤矿安全名词术语解释类问题",
]
result_count_list = [9029, 7281, 2225]

with open(r"../apikey/deepseek.txt", "r", encoding='utf-8') as fp:
    apikey = fp.read()

client = OpenAI(api_key=apikey,
                base_url="https://api.deepseek.com")

with open(r"./final_data/data.json", "r", encoding="utf-8") as fp:
    data = json.load(fp)

i = 0
e = False
for conv in tqdm(data["conversations"][7507+3523:]):
    human_value = conv[0]["value"]
    gpt_value = conv[1]["value"]
    prompt = prompt_template.format(question=human_value, answer=gpt_value)
    max_retries = 5
    retry_count = 0
    success = False
    while not success and retry_count < max_retries:
        content = ""
        try:
            content = client.chat.completions.create(
                model="deepseek-chat",
                messages=
                [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                top_p=0.7,
                temperature=0.1,
                stream=False,
                max_tokens=2500,
            ).choices[0].message.content
        except:

            e = True
            break

        if content in qa_type_list:
            type_index = qa_type_list.index(content)
            result_count_list[type_index] += 1
            success = True
        else:
            retry_count += 1
            print("错误的输出：" + content)
            print(f"重试{retry_count}/{max_retries}")
    if e:
        break
    i += 1

if e:
    print(f"程序意外终端, 终端索引值为{i}")

print(qa_type_list)
print(result_count_list)
