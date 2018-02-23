#!/usr/bin/env python3
"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import random
import numpy as np
import matplotlib.pyplot as plt

def has_numbers(string):
    return any(char.isdigit() for char in string)

if __name__ == "__main__":
    numbers = [660, 795, 45]
    filename = "negative.dat"
    blacklist = set()
    with open("blacklist.dat", 'r') as f:
        lines = f.readlines()
    for line in lines:
        blacklist.add(line.strip())
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        # lines = [line.split(", ")[0] for line in f.readlines()]
    count = 0
    lst = [[], [], []]
    lens = set()
    for line in lines:
        word = line.split(", ")[0]
        tokens = word.lower().split()
        for token in tokens:
            if token in blacklist or has_numbers(token):
                break
        else:
            lens.add(len(tokens))
            lst[len(tokens) - 1].append(line)
            count += 1
    print(count)
    picked = []
    picked.extend(random.sample(lst[0], numbers[0]))
    picked.extend(random.sample(lst[1], numbers[1]))
    picked.extend(random.sample(lst[2], numbers[2]))

    with open("negative_pruned.dat", 'w') as f:
        for line in picked:
            f.write(line + "\n")
    print(len(lst[0]))
    print(len(lst[1]))
    print(len(lst[2]))
