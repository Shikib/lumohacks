import gensim
import numpy as np
import tensorflow as tf

from classify import get_data
from collections import Counter
from tensorflow.contrib import rnn

train = False

# Training Parameters
learning_rate = 0.001
epochs = 10
batch_size = 128
print_every = 20
eval_every = 200
train_size = 100

# Network parameters
embedding_size = 100
seq_len = 200
hidden_size = 64
num_classes = 2

# Input/output nodes
X = tf.placeholder("float", [None, seq_len, embedding_size])
Y = tf.placeholder("float", [None, num_classes])

# Dense layer weights
weights = {
  'out': tf.Variable(tf.random_normal([2*hidden_size, num_classes]))
}
biases = {
  'out': tf.Variable(tf.random_normal([num_classes]))
}

# Load vocab and w2v
w2v = gensim.models.Word2Vec.load("w2v.emb")
vocab = [e.strip() for e in open("vocab2.wl").readlines()]

def load_data():
  """
  Load the X_data in the form of a numpy array:

  (num_examples, seq_len, embedding_size)
  """
  # Call function from classify file to get data.
  data, labels, vocab, w2i = get_data()
  print("Data acquired")

  # Ignore user names for now.
  sentences = [e[1] for e in data]

  all_vectors = []
  for sentence in sentences:
    sentence_vector = []
    for word in sentence:
      if word in vocab:
        sentence_vector.append(w2v[word])
      else:
        sentence_vector.append(np.zeros(100, dtype=np.float32))

    # Need to pad the data
    if len(sentence_vector) < seq_len:
      padding = (seq_len - len(sentence_vector)) * [np.zeros(100, dtype=np.float32)]
      sentence_vector = padding + sentence_vector
    else:
      sentence_vector = sentence_vector[:seq_len]

    all_vectors.append(np.array(sentence_vector))

  print("Vectorization finished")
  import pdb; pdb.set_trace()
  return np.array(all_vectors), np.eye(2)[np.array(labels)]


if train:
  x_data, y_data = load_data()
  #y_data = load_scores_data("data/y_scores.csv")
  #y_data = load_classes_data("data/y_classes.csv")
  
  indexes = np.random.choice(len(x_data), len(y_data), replace=False)
  x_data = x_data[indexes]
  y_data = y_data[indexes]

def next_batch(n, data, labels):
  """
  Return batch of size n.
  """
  indexes = np.random.choice(len(data)-train_size, n, replace=False)
  return data[indexes], labels[indexes]

def LSTM(x, weights, biases):
  # Transform data.
  # (batch_size, seq_len, vocab_size) -> seq_len * [(batch_size, vocab_size)]
  x = tf.unstack(x, seq_len, 1)

  # Forward
  lstm_fw = rnn.BasicLSTMCell(hidden_size)

  # Backward
  lstm_bw = rnn.BasicLSTMCell(hidden_size)

  # Get lstm cell output
  outputs, _, _ = rnn.static_bidirectional_rnn(lstm_fw, 
                                               lstm_bw, 
                                               x,
                                               dtype=tf.float32)

  # Dense layer using last hidden state
  return tf.matmul(outputs[-1], weights['out']) + biases['out']

# Predict
logits = LSTM(X, weights, biases)
prediction = tf.nn.softmax(logits, name="output")

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, 
                                                                 labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# Evaluate model
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

if train:
  with tf.Session() as sess:
    print("Training started")
    sess.run(init)
  
    for step in range(1, epochs+1):
      batch_x, batch_y = next_batch(batch_size, x_data, y_data)
  
      # Backprop
      sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
      if step % print_every == 0:
        # Calculate batch loss and accuracy
        loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                                                             Y: batch_y})
        print("Step " + str(step) + ", Minibatch Loss= " + \
              "{:.4f}".format(loss) + ", Training Accuracy= " + \
              "{:.3f}".format(acc))
  
      if step % eval_every == 1:
        # Calculate accuracy
        print("Testing Accuracy:", \
              sess.run(accuracy, feed_dict={X: x_data[-train_size:], Y: y_data[-train_size:]}))
  
    # Save the session
    saver = tf.train.Saver()
    saver.save(sess, 'lstm_model',global_step=step)
else:
  sess = tf.Session()    
  saver = tf.train.import_meta_graph('lstm_model-1000.meta')
  saver.restore(sess,tf.train.latest_checkpoint('./'))
  graph = tf.get_default_graph()
  output = graph.get_operation_by_name("output")

def vectorize_sentences(sentences):
  all_vectors = []
  for sentence in sentences:
    sentence_vector = []
    for word in sentence:
      if word in vocab:
        sentence_vector.append(w2v[word])
      else:
        sentence_vector.append(np.zeros(100, dtype=np.float32))

    # Need to pad the data
    if len(sentence_vector) < seq_len:
      padding = (seq_len - len(sentence_vector)) * [np.zeros(100, dtype=np.float32)]
      sentence_vector = padding + sentence_vector
    else:
      sentence_vector = sentence_vector[:seq_len]

    all_vectors.append(np.array(sentence_vector))

  return all_vectors

def predict(sentences):
  vectorized = vectorize_sentences(sentences)

  res = sess.run(output, {X: vectorized})
  import pdb; pdb.set_trace()
  return [0,0], 0


import pdb; pdb.set_trace()
