#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
"""
saved into a dat file with following format:
[name string, string length, isCapitalized,
postion index from sentence head, sentence length, pos/neg]
"""

# standard library
import sys
import os
import re


def _is_capitalized(sentence):
    """
    check if a sentence is capitalized or not

    Args:
        sentence: a string

    Returns:
        1 if all word in the sentence is capitalized else 0
    """
    return 1 if all(word[0].isupper() for word in sentence.split()) else 0


def _num_word(sentence):
    """
    compute number of words in a string

    Args:
        sentence: a string

    Returns:
        number of word in the sentence
    """
    return len(sentence.split())


def _split_sentence(sentence, word_num=1):
    """
    return all the substrings with length word_num

    Args:
        sentence: a string
        word_num: number of word in a substring

    Returns:
        substring list
    """
    tokens = sentence.split()
    n = len(tokens)
    return [" ".join(tokens[i:i + word_num])
            for i in range(0, n - word_num + 1)]


def generate_samples(dir_name, is_positive, start_tag='<person>',
                     end_tag='</person>'):
    """
    generate pos/neg examples from files in a directory

    Args:
        dir_name: path of the directory
        is_positive: generate positive or negative samples
        start_tag:
        end_tag:

    Returns:
        samples
    """
    start_tag_len, end_tag_len = len(start_tag), len(end_tag)
    sentence_delimiter = r"[,.!?;]\s*"
    samples = []
    word_nums = [1, 2, 3]
    file_lst = os.listdir(dir_name)
    for file_name in file_lst:
        input_path = os.path.join(dir_name, file_name)
        with open(input_path, 'r') as in_file:
            content = in_file.read()
        sentences = re.split(sentence_delimiter, content)
        if is_positive:
            # positive samples
            for sentence in sentences:
                sentence_len = _num_word(sentence)
                for match in re.finditer(
                        r"{}[^<]*{}".format(start_tag, end_tag), sentence):
                    string = sentence[match.start():match.end()]
                    name = string[start_tag_len: -end_tag_len]
                    sample = (name, _num_word(name), _is_capitalized(name),
                              _num_word(sentence[:match.start()]), sentence_len, 1)
                    samples.append(sample)
        else:
            # negative samples
            for sentence in sentences:
                sentence_len = _num_word(sentence)
                for word_num in word_nums:
                    substrings = _split_sentence(sentence, word_num)
                    for index, substring in enumerate(substrings):
                        if not (start_tag in substring or end_tag in substring):
                            sample = (substring, _num_word(substring), _is_capitalized(substring),
                                      index, sentence_len, 0)
                            samples.append(sample)
    return samples


def write_samples_to_file(output_file_name, samples):
    """
    write samples to a outfile

    Args:
        output_file_name: name of output file
        samples: sample list
    """
    with open(output_file_name, 'w') as out_file:
        for sample in samples:
            out_file.write("{}\n".format(str(sample)[1:-1]))
    print("writing {:d} samples to {}".format(len(samples), output_file_name))


def main():
    """
    extract names from taged files in a folder
    """
    if len(sys.argv) != 4:
        print(
            "Usage: >> python {} <input_folder> <output_file> <pos or neg>".format(
                sys.argv[0]))
        sys.exit(1)
    dir_name, output_file_name = sys.argv[1:-1]
    positive = True if sys.argv[-1] == 'pos' else False
    # setting parameters
    start_tag, end_tag = '<person>', '</person>'
    samples = generate_samples(dir_name, positive, start_tag, end_tag)
    write_samples_to_file(output_file_name, samples)


if __name__ == "__main__":
    main()
