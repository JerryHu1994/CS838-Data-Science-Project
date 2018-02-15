# import numpy as np
# import matplotlib.pyplot as plt
'''
example code to taging all tokens which pass check() function
'''

def check(token):
    d = set(["AA", "BB", "CC"])
    if token[:2] in d:
        return True
    return False

def tag(token, tag_name="person"):
    lst = ["<", tag_name, ">", token, "<\\>"]
    return ''.join(lst)

if __name__ == "__main__":
    filename = "test.in"
    with open(filename, 'r') as f:
        lines = f.readlines()
    out_lines = []
    for line in lines:
        tokens = [tag(token, 'people') if check(token) else token for token in line.split()]
        out_lines.append(' '.join(tokens))
    with open("test.out", 'w') as f:
        for line in out_lines:
            f.write(line + "\n")
