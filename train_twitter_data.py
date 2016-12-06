from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier


categories = ['neg', 'pos']

twitter_train = load_files('./twitter_data/twitter_data-train', encoding='utf-8', decode_error='ignore', categories=categories, load_content=True, shuffle=True, random_state=42)

#Ignoring decode errors may harm our results, but at least it works now
count_vect = CountVectorizer(decode_error='ignore')
X_train_counts = count_vect.fit_transform(twitter_train.data)
X_train_counts.shape

# Use frequencies, not occurrences
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
print(X_train_tf.shape)

# Tf-idf get rid of redundant terms.
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print(X_train_tfidf.shape)

# Train the classifier
clf = MultinomialNB().fit(X_train_tfidf, twitter_train.target)
docs_new = ['I am going to rape you.', 'School is cool.']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twitter_train.target_names[category]))

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])

#for index in range(0, len(twitter_train.data)):
#    twitter_train.data[index].strip()
text_clf = text_clf.fit(twitter_train.data, twitter_train.target)

twitter_test = load_files('./twitter_data/twitter_data-test', categories=categories, load_content=True,
                          encoding='utf-8', decode_error='ignore', shuffle=True, random_state=42)
docs_test = twitter_test.data
predicted = text_clf.predict(docs_test)
print(np.mean(predicted == twitter_test.target))

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, n_iter=5, random_state=42))])

test_clf = text_clf.fit(twitter_train.data, twitter_train.target)
predicted = text_clf.predict(docs_test)
print(np.mean(predicted == twitter_test.target))
