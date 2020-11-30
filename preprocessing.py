import os
import glob
from sklearn.utils import shuffle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import re
from bs4 import BeautifulSoup
import pickle
import numpy as np


def read_imdb_data(data_dir='aclImdb'):
	data = {}
	labels = {}

	for data_type in ['train', 'test']:
		data[data_type] = {}
		labels[data_type] = {}

		for sentiment in ['pos', 'neg']:
			data[data_type][sentiment] = []
			labels[data_type][sentiment] = []

			path = os.path.join(data_dir, data_type, sentiment, '*.txt')
			files = glob.glob(path)

			for f in files:
				with open(f, encoding='utf8') as review:
					data[data_type][sentiment].append(review.read())
					labels[data_type][sentiment].append(1 if sentiment == 'pos' else 0)
			assert len(data[data_type][sentiment]) == len(labels[data_type][sentiment]), '{}/{} data size does not match labels size'.format(data_type,sentiment)
	return data, labels

data, labels = read_imdb_data()
print('IMDB reviews: train = {} pos / {} neg, test = {} pos / {} neg'.format(len(data['train']['pos']), len(data['train']['neg']), len(data['test']['pos']), len(data['test']['neg'])))

def prepare_imdb_data(data, labels):
	data_train = data['train']['pos'] + data['train']['neg']
	data_test = data['test']['pos'] + data['test']['neg']
	labels_train = labels['train']['pos'] + labels['train']['neg']
	labels_test = labels['test']['pos'] + labels['test']['neg']

	data_train, labels_train = shuffle(data_train, labels_train)
	data_test, labels_test = shuffle(data_test, labels_test)

	return data_train, data_test, labels_train, labels_test

train_X, test_X, train_Y, test_Y = prepare_imdb_data(data, labels)
print('IMDB reviews (combined): train = {}, test = {}'.format(len(train_X), len(test_X)))

def review_to_words(review):
	stemmer = PorterStemmer()

	text = BeautifulSoup(review, 'html.parser').get_text()
	text = re.sub(r'[^a-zA-Z0-9]', ' ', text.lower())
	words = text.split()
	words = [w for w in words if w not in stopwords.words('english')]
	words = [stemmer.stem(w) for w in words]

	return words

cache_dir = os.path.join('cache', 'sentiment_analysis')
os.makedirs(cache_dir, exist_ok=True)

def preprocess_data(data_train, data_test, labels_train, labels_test, cache_dir=cache_dir, cache_file='preprocesssed_data.pkl'):
	cache_data = None
	if cache_file is not None:
		try:
			with open(os.path.join(cache_dir, cache_file), 'rb') as f:
				cache_data = pickle.load(f)
				print('Read preprocesssed data from cache file:', cache_file)
		except Exception as e:
			pass

	if cache_data is None:
		print('Writing cache_file...')
		words_train = [review_to_words(review) for review in data_train]
		words_test = [review_to_words(review) for review in data_test]
		if cache_file is not None:
			cache_data = dict(words_train=words_train,words_test=words_test, labels_train=labels_train, labels_test=labels_test)
			with open(os.path.join(cache_dir, cache_file), 'wb') as f:
				pickle.dump(cache_data, f)
			print('Wrote preprocesssed data to cache file:', cache_file)
	else:
		words_train, words_test, labels_train, labels_test = (cache_data['words_train'], cache_data['words_test'], cache_data['labels_train'], cache_data['labels_test'])
	return words_train, words_test, labels_train, labels_test


train_X, test_X, train_Y, test_Y = preprocess_data(train_X, test_X, train_Y, test_Y)

def build_dict(data, vocab_size = 5000):
	word_count = {}
	for sentence in data:
		for word in sentence:
			if word in word_count:
				word_count[word] += 1
			else:
				word_count[word] = 1
	sorted_words = [word for word, count in sorted(word_count.items(), key=lambda x:x[1], reverse=True)]

	word_dict = {}
	for idx, word in enumerate(sorted_words[:vocab_size-2]):
		word_dict[word] = idx + 2

	return word_dict

word_dict = build_dict(train_X)

data_dir = os.path.join('data', 'pytorch')
os.makedirs(data_dir, exist_ok=True)
with open(os.path.join(data_dir, 'word_dict.pkl'), 'wb') as f:
	pickle.dump(word_dict, f)

def convert_and_pad(word_dict, sentence, pad=500):
	NOWORD = 0
	INFREQ = 1
	working_sentence = [NOWORD]*pad

	for word_idx, word in enumerate(sentence[:pad]):
		if word in word_dict:
			working_sentence[word_idx] = word_dict[word]
		else:
			working_sentence[word_idx] = INFREQ
	return working_sentence, min(len(sentence), pad)

def convert_and_pad_data(word_dict, data, pad=500):
	result = []
	lengths = []

	for sentence in data:
		converted, leng = convert_and_pad(word_dict, sentence, pad)
		result.append(converted)
		lengths.append(leng)
	return np.array(result), np.array(lengths)

train_X, train_X_len = convert_and_pad_data(word_dict, train_X)
test_X, test_X_len = convert_and_pad_data(word_dict, test_X)


pd.concat([pd.DataFrame(train_Y), pd.DataFrame(train_X_len), pd.DataFrame(train_X)], axis=1).to_csv(os.path.join(data_dir, 'train.csv'), header=False, index=False)
