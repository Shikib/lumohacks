"""
Training a classifier.
"""
import numpy as np
import string

from collections import Counter
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

def non_ascii(sentence):
  return sum([int(ord(c) > 128) for c in sentence]) >= 1

lemmatizer = WordNetLemmatizer()
def preprocess_sentence(sentence):
  """
  Given a sentence, tokenize it, lemmatize it (using POS tags), then rejoin
  it into a string.
  """
  def _wordnet_pos(tag):
    if tag.startswith('J'):
      return wordnet.ADJ
    elif tag.startswith('V'):
      return wordnet.VERB
    elif tag.startswith('R'):
      return wordnet.ADV
    else: 
      # Default for WordNet is NOUN
      return wordnet.NOUN

  stop = stopwords.words("english") + list(string.punctuation)

  sentence = sentence.lower()
  words = [word for word in word_tokenize(sentence) if word not in stop]
  tagged_words = pos_tag(words)
  return ' '.join([ 
    lemmatizer.lemmatize(word, _wordnet_pos(tag)) for word,tag in tagged_words 
  ])

def vectorize_X(sentences):
  vectors = []
  for sent in sentences:
    vector = np.zeros(len(w2i))
    for word in sent.split():
      if word in w2i:
        vector[w2i[word]] += 1
    vectors.append(vector)

  return np.array(vectors)

def vectorize_y(labels):
  return np.array(labels)

def vectorize_Xy(data, labels):
  sentence_vectors = vectorize_X([e[1] for e in data])
  user_indices = {user:[] for user,_ in data}
  for i,e in enumerate(data):
    user_indices[e[0]].append(i)

  user_vectors = []
  user_labels = []
  for user,indices in user_indices.items():
    user_vectors.append(
      sentence_vectors[user_indices[user]].mean(axis=0)
    )
    user_labels.append(labels[user_indices[user][0]])

  return np.array(user_vectors), np.array(user_labels)

  
def get_data():
  depressed_data = [line.strip().split("\t") for line in open("depressed_data.csv").readlines()]
  nondepressed_data = [line.strip().split("\t") for line in open("nondepressed_data.csv").readlines()]
  
  depressed_data = [s for s in depressed_data if not non_ascii(s[1])]
  nondepressed_data = [s for s in nondepressed_data if not non_ascii(s[1])]
  
  sentences = [(s[0],preprocess_sentence(s[1])) for s in depressed_data + nondepressed_data]
  labels = [1]*len(depressed_data) + [0]*len(nondepressed_data)
  
  vocab = [e[0] for e in Counter(" ".join([e[1] for e in sentences]).split()).most_common(1000)]
  w2i = {e:i for i,e in enumerate(vocab)}

  return sentences,labels,vocab,w2i

classifier = joblib.load('random_forest.pkl')
vocab = [e.strip() for e in open("vocab.wl")]
w2i = {e:i for i,e in enumerate(vocab)}

def predict(sentences):
  # Pre-process sentences
  processed = [preprocess_sentence(s) for s in sentences]
  # Vectorize sentence
  X = vectorize_X(processed)
  # Single
  y = classifier.predict_proba(X)
  # Mean
  merged_y = classifier.predict_proba([X.mean(axis=0)])
  return y, merged_y

if __name__ == '__main__':
  sentences, labels, vocab, w2i = get_data()
  
  #X = vectorize_X(sentences)
  #y = vectorize_y(labels)
  X,y = vectorize_Xy(sentences, labels)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
  
  #classifier = RandomForestClassifier(n_estimators=50, verbose=1000)
  #classifier.fit(X_train, y_train)
  
  y_pred = classifier.predict(X_test)
  print(classification_report(y_test, y_pred, target_names=['non-depressed', 'depressed']))
