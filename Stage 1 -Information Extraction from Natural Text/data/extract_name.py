"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import sys
import os
import re


if __name__ == "__main__":
    '''extract names from taged files in a folder'''
    if len(sys.argv) != 3:
        print("Usage: >> python " + sys.argv[0] + " <input_folder> <output_file>")
        sys.exit(1)
    folder_name = sys.argv[1]
    output_file = sys.argv[2]
    file_lst = os.listdir(folder_name)

    out_file = open(output_file, 'w')
    for file_name in file_lst:
        # print(file_name)
        input_path = folder_name + "/" + file_name
        in_file = open(input_path, 'r')
        content = in_file.read()
        in_file.close()
        persons = re.findall(r"<person>[^<]*</person>", content)
        for person in persons:
            out_file.write(person[8:-9] + '\n')
    out_file.close()
