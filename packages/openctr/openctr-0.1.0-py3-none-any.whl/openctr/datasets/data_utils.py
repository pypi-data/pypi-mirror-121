import h5py
import os
import logging
import numpy as np

class DataIO(object):
    def __init__(self, feature_encoder):
        self.feature_encoder = feature_encoder
        self.cache_dir = os.path.join(feature_encoder.model_dir, feature_encoder.dataset_id)

    def load_data(self, data_path, use_hdf5=False):
        hdf5_file = os.path.join(self.cache_dir, 
                    os.path.splitext(os.path.basename(data_path))[0] + '.hdf5')
        if use_hdf5 and os.path.exists(hdf5_file):
            try:
                data_array = self.load_hdf5(hdf5_file)
                return data_array
            except:
                logging.info('Loading hdf5 failed, reloading from {}'.format(data_path))
        ddf = self.feature_encoder.read_csv(data_path)
        data_array = self.feature_encoder.transform(ddf)
        if use_hdf5:
            self.save_hdf5(data_array, hdf5_file)
        return data_array

    def save_hdf5(self, data_array, data_path, key="data"):
        logging.info("Saving data to " + data_path)
        with h5py.File(data_path, 'w') as hf:
            hf.create_dataset(key, data=data_array)

    def load_hdf5(self, data_path, key="data"):
        logging.info('Loading data from ' + data_path)
        with h5py.File(data_path, 'r') as hf:
            data_array = hf[key][:]
        return data_array

def data_generator(feature_encoder, stage="both", train_data=None, valid_data=None, test_data=None,
                   validation_samples=0, split_type="sequential", batch_size=32, shuffle=True, 
                   use_hdf5=False, neg_samples=-1, **kwargs):
    logging.info("Loading data...")
    # Choose different DataGenerator versions
    if feature_encoder.version == 'tensorflow':
        from ..tensorflow.data_generator import DataGenerator
    elif feature_encoder.version == 'pytorch':
        from ..pytorch.data_generator import DataGenerator
    train_gen = None
    valid_gen = None
    test_gen = None
    data_io = DataIO(feature_encoder)
    if stage in ["both", "train"]:
        train_array =  data_io.load_data(train_data, use_hdf5=use_hdf5)
        num_samples = len(train_array)
        if valid_data:
            valid_array = data_io.load_data(valid_data, use_hdf5=use_hdf5)
            validation_samples = len(valid_array)
            train_samples = num_samples
        else:
            if validation_samples < 1:
                validation_samples = int(num_samples * validation_samples)
            train_samples = num_samples-validation_samples
            instance_IDs = np.arange(num_samples)
            if split_type == "random":
                np.random.shuffle(instance_IDs)
            valid_array = train_array[instance_IDs[train_samples:], :]
            train_array = train_array[instance_IDs[0:train_samples], :]
        train_gen = DataGenerator(train_array, batch_size=batch_size, shuffle=shuffle, neg_samples=neg_samples, **kwargs)
        valid_gen = DataGenerator(valid_array, batch_size=batch_size, shuffle=False, neg_samples=-1, **kwargs)
        logging.info("Train samples: total/{:d} pos/{:.0f} neg/{:.0f} ratio/{:.2f}%" \
                     .format(train_samples, train_array[:, -1].sum(), train_samples-train_array[:, -1].sum(),
                        100 * train_array[:, -1].sum() / train_samples))
        logging.info("Validation samples: total/{:d} pos/{:.0f} neg/{:.0f} ratio/{:.2f}%" \
                     .format(validation_samples, valid_array[:, -1].sum(), validation_samples-valid_array[:, -1].sum(),
                             100 * valid_array[:, -1].sum() / validation_samples))
        if stage == "train":
            logging.info("Loading train data done.")
            return train_gen, valid_gen

    if stage in ["both", "test"]:
        test_array = data_io.load_data(test_data, use_hdf5=use_hdf5)
        test_samples = len(test_array)
        test_gen = DataGenerator(test_array, batch_size=batch_size, shuffle=False, neg_samples=-1, **kwargs)
        logging.info("Test samples: total/{:d} pos/{:.0f} neg/{:.0f} ratio/{:.2f}%" \
                     .format(test_samples, test_array[:, -1].sum(), test_samples-test_array[:, -1].sum(),
                             100 * test_array[:, -1].sum() / test_samples))
        if stage == "test":
            logging.info("Loading test data done.")
            return test_gen

    logging.info("Loading data done.")
    return train_gen, valid_gen, test_gen