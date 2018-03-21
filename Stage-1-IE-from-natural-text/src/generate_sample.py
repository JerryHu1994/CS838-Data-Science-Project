#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
# saved into a dat file with following format:
# [name string, string length, isCapitalized, postion index from sentence head, sentence length, pos/neg]
#########################################################################################################

import sys
import os
import re


def is_capitalized(sentence):
    """check if a sentence is capitalized or not"""
    return 1 if all(word[0].isupper() for word in sentence.split()) else 0


def num_word(sentence):
    """compute number of words in a string"""
    return len(sentence.split())


def split_sentence(sentence, word_num=1):
    """return the substrings with length word_num"""
    tokens = sentence.split()
    n = len(tokens)
    return [" ".join(tokens[i:i + word_num]) for i in range(0, n - word_num + 1)]


def generate_samples(folder_name, positive, start_tag='<person>', end_tag='</person>'):
    start_tag_len, end_tag_len = len(start_tag), len(end_tag)
    sentence_delimiter = r"[,.!?;]\s*"
    samples = []
    word_nums = [1, 2, 3]
    file_lst = os.listdir(folder_name)
    for file_name in file_lst:
        input_path = os.path.join(folder_name, file_name)
        with open(input_path, 'r') as in_file:
            content = in_file.read()
        sentences = re.split(sentence_delimiter, content)
        if positive:
            # positive samples
            for sentence in sentences:
                sentence_len = num_word(sentence)
                for match in re.finditer(r"{}[^<]*{}".format(start_tag, end_tag), sentence):
                    string = sentence[match.start():match.end()]
                    name = string[start_tag_len : -end_tag_len]
                    sample = (name, num_word(name), is_capitalized(name), \
                            num_word(sentence[:match.start()]), sentence_len, 1)
                    samples.append(sample)
        else:
            # negative samples
            for sentence in sentences:
                sentence_len = num_word(sentence)
                for word_num in word_nums:
                    substrings = split_sentence(sentence, word_num)
                    for index, substring in enumerate(substrings):
                        if not (start_tag in substring or end_tag in substring):
                            sample = (substring, num_word(substring), is_capitalized(substring),\
                                    index, sentence_len, 0)
                            samples.append(sample)
    return samples


def write_samples_to_file(output_file_name, samples):
    with open(output_file_name, 'w') as out_file:
        for sample in samples:
            out_file.write("{}\n".format(str(sample)[1:-1]))
    print("writing {:d} samples to {}".format(len(samples), output_file_name))


def main():
    '''extract names from taged files in a folder'''
    if len(sys.argv) != 4:
        print("Usage: >> python {} <input_folder> <output_file> <pos or neg>".format(sys.argv[0]))
        sys.exit(1)
    folder_name, output_file_name = sys.argv[1:-1]
    positive = True if sys.argv[-1] == 'pos' else False
    # setting parameters
    start_tag, end_tag = '<person>', '</person>'
    samples = generate_samples(folder_name, positive, start_tag, end_tag)
    write_samples_to_file(output_file_name, samples)


if __name__ == "__main__":
     main()
