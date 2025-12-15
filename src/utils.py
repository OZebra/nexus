import csv
from random import randint

def csv_to_list_of_lists(filepath):
    matrix = []
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            matrix.append(row)
    return matrix

def make_positive_statement(target, pair):
  return f"{pair} is a hypernym of {target}"

def make_negative_statement(target, pair):
  return f"{pair} is not a hypernym of {target}"

def generate_context(hypernyms, actual):
    rev_hypernyms = hypernyms[::-1]
    list_len = len(rev_hypernyms)

    context = []

    for i in range(0, list_len - 1):
        if actual or i < list_len - 2:
            context.append(make_positive_statement(rev_hypernyms[i+1], rev_hypernyms[i]))
        else:
            context.append(make_negative_statement(rev_hypernyms[i+1], rev_hypernyms[i]))

    return f"{', '.join(context)}."

def generate_entries(data, actual):
    result_entries = []
    for hypernym_list in data:
        context = generate_context(hypernym_list, actual)

        root = hypernym_list[0]
        tail = hypernym_list[1:]

        for i in range (0, len(tail)):
            result_entries.append([f"{make_positive_statement(root, tail[i])}.", actual, i+1, context])
            result_entries.append([f"{make_negative_statement(root, tail[i])}.", not actual, i+1, context])
    
    return result_entries

def parse_csv(csv_path, actual=True):
    #limited to 500 due to api princing restrictions
    data_as_list = csv_to_list_of_lists(csv_path)[:500]
    entries = generate_entries(data_as_list, actual)
    return entries


def print_samples(data, amount=5, random=True):
    data_len = len(data)
    print("================ DATA SAMPLING ==================")
    for i in range(0, amount):
        target = i if not random else randint(0, data_len-1)
        
        print(f"\nEntry: {data[target][0]}")
        print(f"Expected result: {data[target][1]}")
        print(f"Order: {data[target][2]}")
        print(f"Entry context: {data[target][3]}")
        print("\n - - - - - - - - - - - - - - - - - - - - - - -\n")

    print("=================================================")


def save_to_file(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in data:
            csv_writer.writerow(row)