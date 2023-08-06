import numpy as np
from collections import Counter, OrderedDict
import pandas as pd
import pickle
import os
import logging
from collections import defaultdict
from .preprocess import Tokenizer

class FeatureEncoder(object):
    def __init__(self, feature_cols, label_col, dataset_id=None, model_dir="../checkpoints/", **kwargs):
        logging.info("Set up feature encoder...")
        self.dataset_id = dataset_id
        self.pickle_file = os.path.join(model_dir, self.dataset_id, "feature_encoder.pkl")
        self.model_dir = model_dir
        self.feature_cols = self._complete_feature_cols(feature_cols)
        self.label_col = label_col
        self.feature_specs = OrderedDict()
        self.version = kwargs['version']
        self.num_fields = None

    def _complete_feature_cols(self, feature_cols):
        full_feature_cols = []
        for col in feature_cols:
            name_or_namelist = col["name"]
            if isinstance(name_or_namelist, list):
                for _name in name_or_namelist:
                    _col = col.copy()
                    _col["name"] = _name
                    full_feature_cols.append(_col)
            else:
                full_feature_cols.append(col)
        return full_feature_cols

    def read_csv(self, data_path):
        logging.info("Reading file: " + data_path)
        all_cols = self.feature_cols + [self.label_col]
        dtype_dict = dict((x["name"], eval(x["dtype"]) if isinstance(x["dtype"], str) else x["dtype"]) for x in all_cols)
        ddf = pd.read_csv(data_path, dtype=dtype_dict, memory_map=True)
        return ddf

    def _preprocess(self, ddf):
        logging.info("Preprocess feature columns...")
        all_cols = [self.label_col] + self.feature_cols[::-1]
        for col in all_cols:
            name = col["name"]
            if name in ddf.columns and ddf[name].isnull().values.any():
                ddf[name] = self._fill_na(col, ddf[name])
            if "preprocess" in col and col["preprocess"] != "default":
                preprocess_fn = getattr(self, col["preprocess"])
                ddf[name] = preprocess_fn(ddf, name)
        active_cols = [self.label_col["name"]] + [col["name"] for col in self.feature_cols if col["active"]]
        ddf = ddf.loc[:, active_cols]
        return ddf

    def _fill_na(self, col, series):
        na_value = col.get("na_value")
        if na_value is not None:
            return series.fillna(na_value)
        elif col["dtype"] == "str":
            return series.fillna("")
        else:
            raise RuntimeError("Feature column={} requires na_value!".format(col["name"]))

    def set_feature_index(self):
        logging.info("Setting feature index.")
        idx = 0
        for feature, feature_spec in self.feature_specs.items():
            if feature_spec["type"] != "sequence":
                # self.feature_indexs[feature_spec["type"]].append(idx)
                # self.feature_indexs[feature_spec["source"]].append(idx)
                self.feature_specs[feature]["index"] = idx
                idx += 1
            else:
                seq_indices = [i + idx for i in range(feature_spec["max_len"])]
                # self.feature_indexs["sequence"].append(seq_indices)
                # self.feature_indexs[feature_spec["source"]].append(seq_indices)
                self.feature_specs[feature]["index"] = seq_indices
                idx += feature_spec["max_len"]

    def get_feature_index(self, feature_type=None):
        feature_indexes = []
        if feature_type is not None:
            if not isinstance(feature_type, list):
                feature_type = [feature_type]
            feature_indexes = [feature_spec["index"] for feature, feature_spec in self.feature_specs.items()
                               if feature_spec["type"] in feature_type]
        return feature_indexes
    
    def fit(self, train_data, normalizer=None, num_buckets=10, min_categr_count=1, **kwargs):           
        ddf = self.read_csv(train_data)
        ddf = self._preprocess(ddf)
        logging.info("Fit feature encoder...")
        self.num_fields = 0
        for col in self.feature_cols:
            if col["active"]:
                self.num_fields += 1
                name = col["name"]
                self.fit_feature_col(col, ddf.loc[:, name].values, normalizer=normalizer, 
                                     num_buckets=num_buckets, min_categr_count=min_categr_count)
        self.set_feature_index()
        logging.info("Set feature encoder done.")
        if not os.path.exists(self.pickle_file):
            self.save_pickle(self.pickle_file)
        
    def fit_feature_col(self, feature_column, feature_vector, normalizer=None, num_buckets=10,
                        min_categr_count=1):
        name = feature_column["name"]
        feature_type = feature_column["type"]
        feature_source = feature_column["source"] if "source" in feature_column\
                         else "default"
        encoder = feature_column["encoder"] if "encoder" in feature_column else "default"
        self.feature_specs[name] = {"source": feature_source,
                                    "type": feature_type,
                                    "encoder": encoder}
        if "min_categr_count" in feature_column:
            min_categr_count = feature_column["min_categr_count"]
        if feature_type == "numeric":
            if "normalizer" in feature_column and feature_column["normalizer"] is not None:
                normalizer = Normalizer(feature_column["normalizer"])
                normalizer.fit(feature_vector)
                self.feature_specs[name]["normalizer"] = normalizer
        elif feature_type == "categorical":
            if encoder == "default":
                tokenizer = Tokenizer(min_freq=min_categr_count, 
                                      na_value=feature_column.get("na_value", ""))
                tokenizer.fit_on_texts(feature_vector)
                self.feature_specs[name].update({"tokenizer": tokenizer,
                                                 "vocab_size": tokenizer.vocab_size})
            elif encoder == "numeric_bucket":
                if "num_buckets" in feature_column:
                    num_buckets = feature_column["num_buckets"]
                qtf = sklearn_preprocess.QuantileTransformer(n_quantiles=num_buckets + 1)
                qtf.fit(feature_vector)
                boundaries = qtf.quantiles_[1:-1]
                self.feature_specs[name]["boundaries"] = boundaries
            elif encoder == "hash_bucket":
                if "num_buckets" in feature_column:
                    num_buckets = feature_column["num_buckets"]
                uniques = Counter(feature_vector)
                num_buckets = min(num_buckets, len(uniques))
                self.feature_specs[name]["num_buckets"] = num_buckets
        elif feature_type == "sequence":
            splitter = feature_column.get("splitter", " ")
            na_value = feature_column.get("na_value", "")
            tokenizer = Tokenizer(min_freq=min_categr_count, splitter=splitter, 
                                  na_value=na_value, oov_token=1)
            tokenizer.fit_on_texts(feature_vector)
            self.feature_specs[name].update({"tokenizer": tokenizer,
                                             "vocab_size": tokenizer.vocab_size,
                                             "max_len": tokenizer.max_len})
        else:
            raise NotImplementedError("feature_col={}".format(feature_column))

    def transform(self, ddf):
        ddf = self._preprocess(ddf)
        logging.info("Transform feature encoder...")
        data_arrays = []
        for feature, feature_spec in self.feature_specs.items():
            feature_type = feature_spec["type"]
            if feature_type == "numeric":
                numeric_array = ddf.loc[:, feature].fillna(0).apply(lambda x: float(x)).values
                if "normalizer" in feature_spec:
                     numeric_array = feature_spec["normalizer"].normalize(numeric_array)
                data_arrays.append(numeric_array) 
            elif feature_type == "categorical":
                if feature_spec["encoder"] == "default":
                    data_arrays.append(feature_spec["tokenizer"].encode_category(ddf.loc[:, feature].values))
                elif feature_spec["encoder"] == "numeric_bucket":
                    pass
                elif feature_spec["encoder"] == "hash_bucket":
                    pass
            elif feature_type == "sequence":
                data_arrays.append(feature_spec["tokenizer"].encode_sequence(ddf.loc[:, feature].values))
        label_name = self.label_col["name"]
        if ddf[label_name].dtype != np.float64:
            ddf.loc[:, label_name] = ddf.loc[:, label_name].apply(lambda x: float(x))
        data_arrays.append(ddf.loc[:, label_name].values) # add the label column at last
        data_arrays = [item.reshape(-1, 1) if item.ndim == 1 else item for item in data_arrays]
        data_array = np.hstack(data_arrays)
        return data_array

    def load_pickle(self, pickle_file=None):
        """ Load feature encoder from cache """
        if pickle_file is None:
            pickle_file = self.pickle_file
        if os.path.exists(pickle_file):
            pickled_feature_encoder = pickle.load(open(pickle_file, "rb"))
            if self._check_validity(pickled_feature_encoder):
                pickled_feature_encoder.version = self.version
                logging.info("Load pickled feature encoder from " + pickle_file)
                return pickled_feature_encoder
        raise IOError("pickle_file={} not valid!".format(pickle_file))

    def save_pickle(self, pickle_file):
        os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
        pickle.dump(self, open(pickle_file, "wb"))
        logging.info("Pickle feature encode to file: " + pickle_file)

    def _check_validity(self, pickled_feature_encoder):
        if pickled_feature_encoder.dataset_id == self.dataset_id:
            return True
        return False



