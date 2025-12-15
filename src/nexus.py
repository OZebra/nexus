import asyncio

from constants import MODEL_RESPONSE_FORMAT
from openai import AsyncOpenAI
from rate_limiter import RateLimitedLauncher
from utils import csv_to_list_of_lists
from dotenv import load_dotenv
load_dotenv()

client = AsyncOpenAI()

async def ask(row, use_context=False, enhance=False):
    """
        From GPT documentation, for additional context we should use 'User' as a messaging role.
        Here we shall add a context message to address beliefBank feedback.
    """

    question, expected, order, context = row[0], row[1], row[2], row[3]

    input = [{ "role": "user", "content": [{ "type": "text", "text": question }]}]

    completion = await client.chat.completions.create(
        model="gpt-5-mini",
        messages=input,
        response_format=MODEL_RESPONSE_FORMAT
        
    )

    choice = completion.choices[0]
    result = eval(choice.message.content)
    answer = result["answer"]
    parsed_answer = True if answer == "True" else False

    return [question, expected, parsed_answer, order, context]


async def main():
    launcher = RateLimitedLauncher(max_calls_per_sec=2)
    
    actual_entries = csv_to_list_of_lists('./src/data/actual_entries_4k.csv')
    false_entries = csv_to_list_of_lists('./src/data/false_entries_4k.csv')

    union_entries = [*actual_entries, *false_entries]
    union_entries = union_entries[:10]

    results = await launcher.run(union_entries, ask)
    
    print("\nResults [FIRST 5] =========================")
    for result in results[:5]:
        print(f"Statement: ", result[0])
        print(f"Expected/Actual answer: {result[1]}/{result[2]}")
        print(f"Order: ", result[3])
        print("\n- - - - - - - - - - - - - - - - ")

asyncio.run(main())