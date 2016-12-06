from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

from scraper import scrape_tweets


def evaluate_user(user_id):

    categories = ['neg', 'pos']

    twitter_train = load_files('./twitter_data/twitter_data-train', encoding='utf-8', decode_error='ignore',
                               categories=categories, load_content=True, shuffle=True, random_state=42)

    count_vect = CountVectorizer(decode_error='ignore')
    text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 1))),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                               alpha=1e-2, n_iter=5, random_state=42))])
    text_clf = text_clf.fit(twitter_train.data, twitter_train.target)

    scrape_tweets(user_id, 3)
    f = open("scrapings.text", "r")
    neg_count = 0.0
    pos_count = 0.0
    for line in f:
        line_list = [line]
        predicted = str(text_clf.predict(line_list))
        category = str(twitter_train.target_names[int(predicted[1])])
        if category == "neg":
            neg_count += 1
        elif category == "pos":
            pos_count += 1
    print("neg: ", neg_count, " pos: ", pos_count)
    print("Percent Positive: " + str(pos_count / (pos_count + neg_count)))
    print("Percent Negative: " + str(neg_count / (pos_count + neg_count)))

