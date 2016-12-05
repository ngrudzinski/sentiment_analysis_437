from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer


categories = ['neg', 'pos']

twitter_train = load_files('./twitter_data/twitter_data-train', categories=categories, load_content=True, shuffle=True, random_state=42)

#Ignoring decode errors may harm our results, but at least it works now
count_vect = CountVectorizer(decode_error='ignore')
X_train_counts = count_vect.fit_transform(twitter_train.data)
print(X_train_counts.shape)