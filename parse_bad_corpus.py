# This is a script that will parse a file named
# bad_corpus.txt into a training and testing set
# formatted correctly.

import re

with open("bad_corpus.txt") as f:
    count = 0
    file_name = "neg/0000.txt"
    file_object = open(file_name, "w")
    person_filter = re.compile(r'@person:?')
    rt_filter = re.compile(r'RT')

    for line in f:
        if line[0] != "#":
            length = len(line)
            line = line[:length-1]
#            line = rt_filter.sub("", line)
            line_with_no_person = person_filter.sub("", line)
#            if "@person" in line:
#                word_list = line.split()
#                line_with_no_person = " ".join([i for i in word_list if i != "@person" and i != "@person:"])
#            else:
#                line_with_no_person = line
            if line_with_no_person != '':
                file_object.write(line_with_no_person + "\n")
            else:
                file_object.close()
                count += 1
                count_string = str(count)
                count_length = len(count_string)
                file_name = "neg/" + "0" * (4 - count_length) + count_string + ".txt"
                file_object = open(file_name, "w")
