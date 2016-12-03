# This is a script that will parse a file named
# good_corpus.txt into a training and testing set
# formatted correctly.

with open("good_corpus.txt") as f:
    count = 0
    file_name = "pos/0000.txt"
    file_object = open(file_name, "w")
    k = 0
    j = 0
    file_number = 0
    for line in f:
        if k < 15000 and (j % 500) == 0:
            line_with_no_generics = line[:len(line)-1]
            if file_number != k // 500:
                file_number += 1
                file_object.close()
                file_name = "pos/" + "0" * (4 - len(str(file_number))) + str(file_number) + ".txt"
                file_object = open(file_name, "w")
            if "@person" in line or "RT" in line:
                word_list = line.split()
                line_with_no_generics = " ".join([i for i in word_list if i != "@person" and i != "@person:" and i != "RT"])
            if line_with_no_generics != '':
                file_object.write(line_with_no_generics + "\n")
                j += 1
                k += 1
        elif k > 3000:
            break

    file_object.close()
