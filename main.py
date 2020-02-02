#!/usr/bin/env python

import sys
import random
import re
import time
import datetime

print("\n")

genes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
if 2 <= len(sys.argv) and sys.argv[1] == "--allow-symbols":
    genes += "!\"#$%&\'\(\)-=^~\\|@`[{;+:*]},<.>/?\_ "

model_genes = sys.stdin.read()

model_newline_positions = [len(match) for match in re.split("\n", model_genes)]
model_newline_positions = [sum(model_newline_positions[:i+1]) for i, _ in enumerate(model_newline_positions)]

model_genes = re.sub("\n", "", model_genes)

model_genes_len = len(model_genes)

genes_dict = {s: i for i, s in enumerate(genes)}
number_of_genes = len(genes)

def calc_distance_between_genes(geneA, geneB):
    indA = genes_dict[geneA]
    indB = genes_dict[geneB]
    distance = abs(indA - indB)
    return min([distance, number_of_genes - distance])

def move_gene(gene, distance):
    ind = genes_dict[gene]
    ind += distance
    new_ind = ind % number_of_genes
    new_gene = genes[new_ind]
    return new_gene

def calc_score(model_genes, target_genes):
    distances = [calc_distance_between_genes(model_gene, target_gene) for model_gene, target_gene in zip(model_genes, target_genes)]
    return sum(distances)

def random_genes(length):
    return "".join([random.choice(genes) for k in range(length)])

def make_child(parents):
    t_parents = list(zip(*parents))
    child = "".join([random.choice(gene) for gene in t_parents])
    child = mutate(child)
    return child

def mutate(genes):
    return "".join([gene if mutation_rate < random.random() else move_gene(gene, random.randint(-mutation_range, mutation_range)) for gene in genes])

def print_monkey(monkey, do_back=False):
    result = ""
    if do_back:
        result += "\033[" + str(len(model_newline_positions) + 3) + "A\r"
    start_position = 0
    for end_position in model_newline_positions:
        result += monkey[start_position:end_position] + "\n"
        start_position = end_position
    result += "\n\033[2Kcurrent distance: " + str(calc_score(model_genes, monkey))
    result += "\n\033[2Kelapsed time    : " + str(datetime.datetime.now() - start_time)
    print(result)

generation = 1
start_time = datetime.datetime.now()

number_of_monkeys = 50
number_of_parent = 4
mutation_rate = 0.05
mutation_range = 10

monkeys = [random_genes(model_genes_len) for k in range(number_of_monkeys)]
scores = [calc_score(model_genes, monkey) for monkey in monkeys]
scores_monkeys = sorted(zip(scores, monkeys))
print_monkey(scores_monkeys[0][1])

while (scores_monkeys[0][0] != 0):
    generation += 1
    parents = [score_monkey[1] for score_monkey in scores_monkeys[:number_of_parent]]
    monkeys = [make_child(parents) for k in range(number_of_monkeys)]
    scores = [calc_score(model_genes, monkey) for monkey in monkeys]
    scores_monkeys = sorted(zip(scores, monkeys))
    print_monkey(scores_monkeys[0][1], True)
    time.sleep(0.01)

print("generation: " + str(generation))
