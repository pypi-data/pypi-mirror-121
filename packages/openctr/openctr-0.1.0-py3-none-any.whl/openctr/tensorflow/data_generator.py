import numpy as np
from tensorflow.python.keras.utils import Sequence

class DataGenerator(Sequence):
    def __init__(self, data_array, batch_size=32, shuffle=False, neg_samples=-1, **kwargs):
        self.darray = data_array
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.neg_samples = neg_samples
        self.index_pool = list(range(self.darray.shape[0]))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.index_pool) * 1.0 / self.batch_size))

    def __getitem__(self, index):
        indexes = self.index_pool[index * self.batch_size : (index + 1) * self.batch_size]
        X = self.darray[indexes, 0:-1]
        y = self.darray[indexes, -1]
        return X, y

    def on_epoch_end(self):
        if self.neg_samples > 0:
            self.index_pool = self.neg_sampling()
        if self.shuffle:
            np.random.shuffle(self.index_pool)

    def get_labels(self):
        # Get labels along with the order of data generator
        return self.darray[self.index_pool, -1]

    def neg_sampling(self):
        # Down sampling of negatives
        pos_index = np.where(self.darray[:, -1] > 0.5)[0]
        neg_index = np.where(self.darray[:, -1] < 0.5)[0]
        num_neg = min(len(pos_index) * self.neg_samples, len(neg_index))
        sampled_neg_index = np.random.choice(neg_index, num_neg, replace=False)
        data_index = np.sort(np.hstack([pos_index, sampled_neg_index]))
        return list(data_index)

