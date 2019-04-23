import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, SpatialDropout1D
from keras.layers import LSTM, Dense, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

data = pd.read_csv('input/uci-news-aggregator.csv', usecols=['TITLE', 'CATEGORY'])
print(data.CATEGORY.value_counts()) #最后看是否可以删去
num_of_categories = 20000

# take 45000 data of each category to have balanced data
# and shuffle the dataset
shuffled = data.reindex(np.random.permutation(data.index))
e = shuffled[shuffled['CATEGORY'] == 'e'][:num_of_categories]
b = shuffled[shuffled['CATEGORY'] == 'b'][:num_of_categories]
t = shuffled[shuffled['CATEGORY'] == 't'][:num_of_categories]
m = shuffled[shuffled['CATEGORY'] == 'm'][:num_of_categories]
concated = pd.concat([e, b, t, m], ignore_index=True)
concated = concated.reindex(np.random.permutation(concated.index))

# one-hot encode the labels
concated['LABEL'] = 0
concated.loc[concated['CATEGORY'] == 'e', 'LABEL'] = 0
concated.loc[concated['CATEGORY'] == 'b', 'LABEL'] = 1
concated.loc[concated['CATEGORY'] == 't', 'LABEL'] = 2
concated.loc[concated['CATEGORY'] == 'm', 'LABEL'] = 3
labels = to_categorical(concated['LABEL'], num_classes=4)
concated.drop(['CATEGORY'], axis=1)

# tokenize the title data
max_num_words = 8000
max_sequence_length = 130
tokenizer = Tokenizer(num_words = max_num_words)
tokenizer.fit_on_texts(concated['TITLE'].values)
sequences = tokenizer.texts_to_sequences(concated['TITLE'].values)
word_index = tokenizer.word_index
print('Found {} unique tokens.'.format(len(word_index)))
data_processed = pad_sequences(sequences, maxlen=max_sequence_length)

# prepare the training and test data
x_train, x_test, y_train, y_test = train_test_split(data_processed, labels, random_state=7)

# define hyperparameters
epochs = 6
embedding_dim = 128
batch_size = 256

# build the model
model = Sequential()
model.add(Embedding(max_num_words, embedding_dim, input_length=data_processed.shape[1]))
model.add(SpatialDropout1D(0.7))
model.add(LSTM(64, dropout=0.7, recurrent_dropout=0.7))
model.add(Dense(4, activation='softmax'))

model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['acc'])

model.summary()

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.25)

scores = model.evaluate(x_test, y_test)

print('test loss:', scores[0])
print('test accuracy:', scores[1])
