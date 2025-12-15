# coding:utf-8
"""
@Filename: llm_eval.py
@Description: 使用LLM-eval方法评估模型表现
@Author: Li Zongyu
@Time: 2025/8/31 14:41
"""
import json
from transformers import TrainingArguments
from openai import OpenAI

with open("../apikey/deepseek.txt", "r", encoding="utf-8") as fp:
    apikey = fp.read()
client = OpenAI(api_key=apikey,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
prompt_template = """请根据以下标准评估煤矿安全领域专家对特定学科问题的以下回答。您必须按照0、1、2或3颗星的评分标准对其进行评分：

总体评价：
0颗星表示错误答案和错误解释
1颗星表示回答错误，但部分解释合理
2颗星表示正确答案，部分合理解释
三星表示正确答案和合理解释

用户: {query}

LLM: {answer}

用户问题的正确答案是: {correct_answer}

您必须按照以下格式提供反馈: 
{"总体评分"：星级数（整数）}"""


def predict(prompt: str):
    return client.chat.completions.create(
        model="deepseek-v3",
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


def eval(query: str, answer: str, correct_answer: str) -> int:
    _prompt = prompt_template.replace("{query}", query).replace("{answer}",answer).replace("{correct_answer}", correct_answer)
    llm_response_str = predict(_prompt)
    success = False
    retry_time = 0
    retry_max_time = 5
    eval_score = -1
    while not success and retry_time < retry_max_time:
        try:
            # 转化为字典
            eval_score = json.loads(llm_response_str)["总体评分"]
            success = True
        except:
            retry_time += 1
            continue
    return eval_score


if __name__ == '__main__':
    eval()
