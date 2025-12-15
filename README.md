# 基于大模型的煤矿安全领域知识问答技术研究

## 一、数据集构建以及处理

​	[数据处理](data/readme.md)

## 二、大模型微调

[Lora微调代码](finetune/finetuned.ipynb)

- 方法：`Lora+GRPO+Qwen2.5-7B`模型微调+强化学习+Qwen2.5-7B
  - 监督学习阶段：使用Lora低秩微调方法优化模型，让模型学习煤矿安全领域知识；
  - 后训练阶段：使用GRPO强化学习方法，通过设计奖励函数，通过策略优化提升模型的生成质量和领域适应性。

- 消融实验

|        Method        | 评估指标 |
| :------------------: | :------: |
|      Qwen2.5-7B      |    1     |
|   Qwen2.5-7B+Lora    |    2     |
|   Qwen2.5-7B+GRPO    |    3     |
| Qwen2.5-7B+Lora+GRPO |    4     |

- 对比实验

|        Models        | 评估指标 |
| :------------------: | :------: |
| Qwen2.5-7B+Lora+GRPO |    1     |
|    Qwen2.5-7B+RAG    |    2     |
|     Baichuan2-7B     |    3     |
|  Chinese-llama-2-7b  |    4     |

### 混合奖励函数

​	混合奖励函数由三个部分组成，长度奖励，词频相似度奖励以及词嵌入相似度奖励，公式如下：
$$
R=\alpha R_1+ \beta (R_2+ R_3）
$$

​	其中$R_1$ 为长度奖励，$\alpha$为其比重；$R_2$ 为词频相似度奖励，$\beta$为其比重；$R_3$ 为词嵌入相似度奖励，$\gamma$为其比重；

$$
R_1=
 \begin{cases}
 1 & \frac{len(p)}{len(r)}\in[0.5, 2] \\
 \frac{len(r)}{len(r)+|len(p)-len(r)|}&\frac{len(p)}{len(r)}\in[0,0.5)\bigcup(2,+\infty)\\
 \end{cases}
$$
​	其中，上式中$len(·)$为计算长度的函数。
$$
R_2=\sum^n_{i=1}{min(1,\frac{f(w_i,P)}{f(w_i,R)}) \times\frac{f(w_i,R)}{|R|}}
$$
​	其中，$f(a,b)$为词语$a$ 在文本$b$中的词频，$|R|$为文本$R$的词语总数。$R2$的主要功能是，模型生成的和正确答案的词比值（**词匹配分数**）趋于1越好，而且同时强调了那些词频高的词，也就是较为关键的词的比值情况。
$$
R_3=cosine(Vector(P),Vector(R))
$$
​	其中$cosine(a,b)$为$a$与$b$的余弦相似度值，$Vector(a)$ 为a的词嵌入向量。

### GRPO强化学习算法缺陷

GRPO的核心机制是**重要性采样**，这是一种在统计学中修正分布偏差的方法。GRPO存在致命的缺陷，奖励是针对模型预测的**完整序列**的粒度给出的，而GRPO却试图在**单个词（Token）**这个粒度上进行归因和校正。其根本问题在于：**优化的基本单位（词）与奖励的基本单位（文章）不匹配**。这导致它在理论上就是“病态的（ill-posed）”，训练过程中的不稳定性是其与生俱来的缺陷。

GSPO的核心思想异常简洁：**让优化的单位与奖励的单位保持一致。**

## 三、模型评估指标

可选：

- LLM-Eval方法：使用GPT4 Turbo进行打分，prompt如下所示
  - LIN Y T， CHEN Y N. LLM-Eval： unified multi-dimensional automatic evaluation for open-domain conversations with large language models ［EB/OL］. ［2025-05-11］. https://api. semanticscholar. org/CorpusID:258841681.

```python
# 英文prompt
prompt = """Please evaluate the following response from the LLM regarding a discipline-specific question based on the following criteria. You must score it on a scale of 0, 1, 2 or 3 stars:

Overall Rating:
0 stars indicate wrong answer with a wrong explanation
1 star indicates wrong answer but a partially reasonable explanation
2 stars indicate a correct answer with a partially reasonable explanation
3 stars indicate a correct answer with a reasonable explanation

User: {question}

LLM:{answer_from_llm}

The correct answer to user's question is: {correct_answer}

You must provide your feedback in the following format:
{"Overall Rating":numbers of its stars(int)}"""
```

```python
# 中文prompt
prompt = """请根据以下标准评估煤矿安全领域专家对特定学科问题的以下回答。您必须按照0、1、2或3颗星的评分标准对其进行评分：

总体评价：
0颗星表示错误答案和错误解释
1颗星表示回答错误，但部分解释合理
2颗星表示正确答案，部分合理解释
三星表示正确答案和合理解释

用户：｛问题｝

LLM:{answer_from_LLM}

用户问题的正确答案是：{correct_answer}

您必须按照以下格式提供反馈：
{“总体评分”：星级数（整数）}"""
```





