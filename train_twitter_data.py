from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV


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
docs_new = ['I am going to rape you.', 'Fucking faggot', 'I love you', 'School is cool.']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twitter_train.target_names[category]))

text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 1))),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])

#for index in range(0, len(twitter_train.data)):
#    twitter_train.data[index].strip()
text_clf = text_clf.fit(twitter_train.data, twitter_train.target)

twitter_test = load_files('./twitter_data/twitter_data-test', categories=categories, load_content=True,
                          encoding='utf-8', decode_error='ignore', shuffle=True, random_state=42)
docs_test = twitter_test.data
predicted = text_clf.predict(docs_test)
print("Multinomial Naive Bayes Classifier Results: " + str(np.mean(predicted == twitter_test.target)))

text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 1))),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-2, n_iter=5, random_state=42))])

text_clf = text_clf.fit(twitter_train.data, twitter_train.target)
predicted = text_clf.predict(docs_test)
print("SGD Classifier Results: " + str(np.mean(predicted == twitter_test.target)))

print(metrics.classification_report(twitter_test.target, predicted, target_names=twitter_test.target_names))

# Use grid search on small subset of
parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
              'tfidf__use_idf': (True, False),
              'clf__alpha': (1e-2, 1e-3)}
gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(twitter_train.data, twitter_train.target)
print("Result of GS on 'Fuck You': " + str(twitter_train.target_names[gs_clf.predict(['God is love'])[0]]))
print("Best score for GS: " + str(gs_clf.best_score_))
print("\nBest Parameters")
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
