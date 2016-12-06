from __future__ import print_function

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

from scraper import scrape_tweets

from sys import stdout

def evaluate_user(user_id, output_file):

    categories = ['neg', 'pos']

    twitter_train = load_files('./twitter_data/twitter_data-train', encoding='utf-8', decode_error='ignore',
                               categories=categories, load_content=True, shuffle=True, random_state=42)

    count_vect = CountVectorizer(decode_error='ignore')
    text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2))),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                               alpha=1e-3, n_iter=5, random_state=42))])
    text_clf = text_clf.fit(twitter_train.data, twitter_train.target)

    if scrape_tweets(user_id, 3) == 1:
        return 1

    f = open("scrapings.text", "r")
    neg_count = 0.0
    pos_count = 0.0
    doubleprint(user_id + "'s twitter classification:\n", output_file)
    doubleprint("~~~~~~~~~~~~~~~~~\n", output_file)
    for line in f:
        line_list = [line]
        predicted = str(text_clf.predict(line_list))
        category = str(twitter_train.target_names[int(predicted[1])])
        doubleprint(line, output_file)
        if category == "neg":
            neg_count += 1
            doubleprint("NEGATIVE\n\n", output_file)
        elif category == "pos":
            pos_count += 1
            doubleprint("POSITIVE\n", output_file)
    doubleprint("\nNegative: " + str(neg_count) + " Positive: " +  str(pos_count) + "\n", output_file)
    doubleprint("Percent Positive: " + str(pos_count / (pos_count + neg_count)) + "\n", output_file)
    doubleprint("~~~~~~~~~~~~~~~~~\n", output_file)
    return 0

def doubleprint(text, output_file):
    print(text)
    if output_file is not None:
        output_file.write(text)


if __name__ == "__main__":
    evaluate_user("potus", None)

