from utils import csv_to_list_of_lists

results_files = [
    "./src/results/GPT5-mini_STD-TEST_ACTUAL.csv",
    "./src/results/GPT5-mini_AGENT-TEST_ACTUAL.csv",
    "./src/results/GPT5-mini_CONTEXT-TEST_ACTUAL.csv",
    "./src/results/GPT5-mini_INDIRECT_CONTEXT-TEST_ACTUAL.csv",
]

for x in results_files:
    results = csv_to_list_of_lists(x)

    wrong = 0
    for item in results:
        if item[1] != item[2]:
            wrong += 1

    print(f"Incorrect amount at {x.split("/").pop()} file: {wrong}")