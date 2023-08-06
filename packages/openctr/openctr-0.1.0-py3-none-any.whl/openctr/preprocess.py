from collections import Counter
import itertools
import numpy as np
import pandas as pd
import sklearn.preprocessing as sklearn_preprocess
from tensorflow.python.keras.preprocessing.sequence import pad_sequences


class Tokenizer(object):
    def __init__(self, num_words=None, na_value=None, min_freq=1, splitter=None, oov_token=0, lower=False):
        self._num_words = num_words
        self._na_value = na_value
        self._min_freq = min_freq
        self._lower = lower
        self._splitter = splitter
        self.oov_token = oov_token
        self.word_counts = Counter()
        self.word_index = dict()
        self.vocab_size = 0 # include oov and padding if any
        self.max_len = 1

    def fit_on_texts(self, texts):
        tokens = list(texts)
        if self._splitter is not None:
            text_splits = [text.split(self._splitter) for text in texts if not pd.isnull(text)]
            self.max_len = max(len(x) for x in text_splits)
            tokens = list(itertools.chain(*text_splits))
        if self._lower:
            tokens = [tk.lower() for tk in tokens]
        if self._na_value is not None:
            tokens = [tk for tk in tokens if tk != self._na_value]
        self.word_counts = Counter(tokens)
        words = [token for token, count in self.word_counts.items() if count >= self._min_freq]
        if self._num_words:
            words = words[0:self._num_words]
        self.word_index = dict((token, idx + 1 + self.oov_token) for idx, token in enumerate(words))
        self.vocab_size = len(self.word_index) + 1 + self.oov_token

    def encode_category(self, categories):
        category_indices = [self.word_index.get(x, self.oov_token) for x in categories]
        return np.array(category_indices)

    def encode_sequence(self, texts):
        sequence_list = []
        for text in texts:
            if pd.isnull(text) or text == '':
                sequence_list.append([])
            else:
                sequence_list.append([self.word_index.get(x, self.oov_token) for x in text.split(self._splitter)])
        sequence_list = pad_sequences(sequence_list, maxlen=self.max_len, padding='post', truncating='post')
        return np.array(sequence_list)
    
    def gen_embedding_matrix(self, pretrain_path, cache_path, embedding_size=300):
        from gensim.models import Word2Vec, KeyedVectors
        try:
            word_vec_dict = Word2Vec.load(pretrain_path)
        except:
            word_vec_dict = KeyedVectors.load_word2vec_format(pretrain_path, binary=False)
        index_word = {index: word for word, index in self.word_index.items()}
        emb_mat = np.random.randn(len(index_word), embedding_size)
        for idx, word in index_word.items():
            if word in word_vec_dict:
                emb_mat[idx] = word_vec_dict[word]
                
        
class Normalizer(object):
    def __init__(self, normalizer):
        if not callable(normalizer):
            self.callable = False
            if normalizer in ['StandardScaler', 'MinMaxScaler']:
                self.normalizer = getattr(sklearn_preprocess, normalizer)()
            else:
                raise NotImplementedError('normalizer={}'.format(normalizer))
        else:
            # normalizer is a method
            self.normalizer = normalizer
            self.callable = True

    def fit(self, X):
        if not self.callable:
            null_index = np.isnan(X)
            self.normalizer.fit(X[~null_index].reshape(-1, 1))

    def normalize(self, X):
        if self.callable:
            return self.normalizer(X)
        else:
            return self.normalizer.transform(X.reshape(-1, 1)).flatten()