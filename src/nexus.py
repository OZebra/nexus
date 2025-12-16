import asyncio

from constants import MODEL_RESPONSE_FORMAT
from openai import AsyncOpenAI
from rate_limiter import RateLimitedLauncher
from utils import csv_to_list_of_lists, save_to_file
from dotenv import load_dotenv
load_dotenv()

client = AsyncOpenAI()

async def ask(row, use_context=False, enhance=False):
    """
        From GPT documentation, for additional context we should use 'User' as a messaging role.
        Here we shall add a context message to address beliefBank feedback.
    """

    question, expected, order, context = row[0], row[1], row[2], row[3]
    
    input = []

    if enhance:
        input.append({ "role": "system", "content": [{ "type": "text", "text": f"<Enhancement agent prompt (keep it small)>" }]})

    if use_context:
        input.append({ "role": "system", "content": [{ "type": "text", "text": f"Consider that all of these statements are true: {context}" }]})
    
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

    # Here we want our datasets divided by origin type because some metrics wont fit both of them.
    actual_results = await launcher.run(actual_entries, ask)
    false_results = await launcher.run(false_entries, ask)

    save_to_file(actual_results, './src/results/GPT5-mini_STD-TEST_ACTUAL.csv.csv')
    save_to_file(false_results, './src/results/GPT5-mini_STD-TEST_ACTUAL.csv.csv')

asyncio.run(main())