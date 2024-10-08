import dotenv
dotenv.load_dotenv()

import openai
from openai import OpenAI
import requests
client = OpenAI()

def gen_query_answer(corpus):
    query_prompt = query_gen_prompt(corpus)
    query = base_gen(query_prompt)

    answer_prompt = answer_gen_prompt(corpus, query)
    answer = base_gen(answer_prompt)

    return {"query": query, "answer": answer}

def base_gen(prompt):
    response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
    return response.choices[0].message.content

def query_gen_prompt(corpus):
    prompt = f"""
    너는 주어진 Text 속에서, 일반 사용자들이 가질 만한 질문을 생성해 주는 봇이야.
    <Text>
    {corpus}
    </Text>

    위의 Text 속에서 사용자가 가질만한 질문을 하나만 생성해 줘
    """
    return prompt

def answer_gen_prompt(corpus, query):
    prompt = f"""
    너는 주어진 Text와 Query를 입력 받아, 답변을 생성해 주는 봇이야.
    <Text>
    {corpus}
    </Text>

    <Query>
    {query}
    </Query>

    위의 Text 속에서 Query에 대한 답변을 하나만 생성해 줘.
    이때, Text속에 담겨 있는 정보 외에 다른 거짓 정보가 담겨서는 안돼.
    """
    return prompt