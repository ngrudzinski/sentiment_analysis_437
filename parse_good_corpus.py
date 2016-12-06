# This is a script that will parse a file named
# good_corpus.txt into a training and testing set
# formatted correctly.

import re

with open("good_corpus.txt") as f:
    count = 0
    file_name = "pos/0000.txt"
    file_object = open(file_name, "w")
    k = 0
    j = 0
    file_number = 0

    person_filter = re.compile(r'@person:?')
    rt_filter = re.compile(r'RT')

    try:
        # UCS-4
        emoji_filter = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
        # UCS-2
        emoji_filter = re.compile(
            u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')

    #Nate, I'm not really sure what j was supposed to do separately from k.
    for line in f:
        if k < 15000 and (k % 500) == 0:
            line_with_no_generics = line[:len(line)-1]
            if file_number != k // 500:
                file_number += 1
                file_object.close()
                file_name = "pos/" + "0" * (4 - len(str(file_number))) + str(file_number) + ".txt"
                file_object = open(file_name, "w")

            # Strips out "RT", "@person", "@person:"
            # Does this improve the results, Nate?
            line_with_no_generics = person_filter.sub("", line_with_no_generics)
            line_with_no_generics = rt_filter.sub("", line_with_no_generics)

            # Do not need, and probably do not want to strip out emoji anymore
            # Uncomment if we actually should
#            line_with_no_emoji_in_unicode = emoji_filter.sub("", line_with_no_generics.decode('utf-8'))
#            line_with_no_generics = line_with_no_emoji_in_unicode.encode('utf-8')


#            if "@person" in line or "RT" in line:
#                word_list = line.split()
#                line_with_no_generics = " ".join([i for i in word_list if i != "@person" and i != "@person:" and i != "RT"])
            if line_with_no_generics != '':
                file_object.write(line_with_no_generics + "\n")
        k += 1

    file_object.close()
