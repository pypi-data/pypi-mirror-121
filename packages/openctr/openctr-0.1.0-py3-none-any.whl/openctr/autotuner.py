import itertools
import subprocess
import yaml
import os
import numpy as np
import glob
import hashlib
from .utils import load_config, print_to_json

# add this line to avoid weird characters in yaml files
yaml.Dumper.ignore_aliases = lambda *args : True

def load_model_config(config_dir, experiment_id):
    params = dict()
    model_configs = glob.glob(os.path.join(config_dir, 'model_config.yaml'))
    if not model_configs:
        model_configs = glob.glob(os.path.join(config_dir, 'model_config/*.yaml'))
    found_keys = []
    for config in model_configs:
        with open(config, 'r') as cfg:
            config_dict = yaml.load(cfg)
            if 'Base' in config_dict:
                params.update(config_dict['Base'])
                found_keys.append('Base')
            if experiment_id in config_dict:
                params.update(config_dict[experiment_id])
                found_keys.append(experiment_id)
        if len(found_keys) == 2:
            break
    if 'dataset_id' not in params:
        raise RuntimeError('experiment_id={} is not valid in config.'.format(experiment_id))
    params['model_id'] = experiment_id
    return params

def load_dataset_config(config_dir, dataset_id):
    params = dict()
    dataset_configs = glob.glob(os.path.join(config_dir, 'dataset_config.yaml'))
    if not dataset_configs:
        dataset_configs = glob.glob(os.path.join(config_dir, 'dataset_config/*.yaml'))
    for config in dataset_configs:
        with open(config, 'r') as cfg:
            config_dict = yaml.load(cfg)
            if dataset_id in config_dict:
                params.update(config_dict[dataset_id])
                break
    return params

def enumerate_params(config_file, expid_blacklist=[]):
    with open(config_file, 'r') as cfg:
        config_dict = yaml.load(cfg)
    # tuning space
    tune_dict = config_dict['tuner_space']
    for k, v in tune_dict.items():
        if not isinstance(v, list):
            tune_dict[k] = [v]
    experiment_id = config_dict['base_expid']
    base_config_dir = config_dict.get('base_config', os.path.dirname(config_file))
    model_dict = load_model_config(base_config_dir, experiment_id)
    dataset_id = model_dict['dataset_id']
    dataset_dict = load_dataset_config(base_config_dir, dataset_id)

    # key checking
    tuner_keys = set(tune_dict.keys())
    base_keys = set(model_dict.keys()).union(set(dataset_dict.keys()))
    if len(tuner_keys - base_keys) > 0:
        raise RuntimeError('Invalid params in tuner config: {}'.format(tuner_keys - base_keys))

    config_dir = config_file.replace('.yaml', '')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # enumerate dataset para combinations
    dataset_dict = {k: tune_dict[k] if k in tune_dict else [v] for k, v in dataset_dict.items()}
    dataset_para_keys = list(dataset_dict.keys())
    dataset_para_combs = dict()
    for idx, values in enumerate(itertools.product(*map(dataset_dict.get, dataset_para_keys))):
        dataset_params = dict(zip(dataset_para_keys, values))
        hash_id = hashlib.md5(print_to_json(dataset_params).encode('utf-8')).hexdigest()[0:8]
        dataset_para_combs[dataset_id + '_{:03d}_{}'.format(idx + 1, hash_id)] = dataset_params

    # dump dataset para combinations to config file
    dataset_config = os.path.join(config_dir, 'dataset_config.yaml')
    with open(dataset_config, 'w') as fw:
        yaml.dump(dataset_para_combs, fw, default_flow_style=None, indent=4)

    # enumerate model para combinations
    model_dict = {k: tune_dict[k] if k in tune_dict else [v] for k, v in model_dict.items()}
    model_para_keys = list(model_dict.keys())
    model_param_combs = dict()
    for idx, values in enumerate(itertools.product(*map(model_dict.get, model_para_keys))):
        model_param_combs[idx + 1] = dict(zip(model_para_keys, values))
        
    # update dataset_id into model params
    merged_param_combs = dict()
    for idx, item in enumerate(itertools.product(model_param_combs.values(),
                                                 dataset_para_combs.keys())):
        para_dict = item[0]
        para_dict['dataset_id'] = item[1]
        hash_id = hashlib.md5(print_to_json(para_dict).encode('utf-8')).hexdigest()[0:8]
        hash_expid = experiment_id + '_{:03d}_{}'.format(idx + 1, hash_id)
        if hash_expid not in expid_blacklist:
            merged_param_combs[hash_expid] = para_dict.copy()

    # dump model para combinations to config file
    model_config = os.path.join(config_dir, 'model_config.yaml')
    with open(model_config, 'w') as fw:
        yaml.dump(merged_param_combs, fw, default_flow_style=None, indent=4)
    print('Enumerate all tuner configurations done.')    
    return config_dir

def load_experiment_ids(config_dir):
    model_configs = glob.glob(os.path.join(config_dir, 'model_config.yaml'))
    if not model_configs:
        model_configs = glob.glob(os.path.join(config_dir, 'model_config/*.yaml'))
    experiment_id_list = []
    for config in model_configs:
        with open(config, 'r') as cfg:
            config_dict = yaml.load(cfg)
            experiment_id_list += config_dict.keys()
    return sorted(experiment_id_list)

def run_all(version, config_dir, gpu_list):
    def _chunk_list(ls, n):
        return [ls[i * n : (i + 1) * n] for i in range((len(ls) + n - 1) // n)]
    
    experiment_id_list = load_experiment_ids(config_dir)
    chunked_expid_list = _chunk_list(experiment_id_list, len(gpu_list))
    for expid in chunked_expid_list:
        np.random.shuffle(expid) # shuffle for load balancing among gpus
    transposed_expid_list = list(itertools.zip_longest(*chunked_expid_list))
    processes = []
    for idx in range(len(gpu_list)):
        exp_list = transposed_expid_list[idx]
        cmd_list = []
        for expid in exp_list:
            if expid is not None:
                gpu_id = gpu_list[idx]
                cmd = 'python benchmark.py --version {} --config {} --expid {} --gpu {}'\
                      .format(version, config_dir, experiment_id, gpu_id)
                cmd_list.append(cmd)
        cmd_sequence = '; '.join(cmd_list)
        processes.append(subprocess.Popen(cmd_sequence, shell=True))
    [p.wait() for p in processes]
    
