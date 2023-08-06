import os
import hither2 as hi
import yaml
from copy import deepcopy

default_config_yaml = '''
job_handlers:
    misc:
        type: parallel
        params:
            num_workers: 4
    timeseries:
        type: parallel
        params:
            num_workers: 4
'''
default_config = yaml.safe_load(default_config_yaml)

config = deepcopy(default_config)

job_handler_config_path = os.getenv('SERIESVIEW_JOB_HANDLER_CONFIG', None)
if job_handler_config_path is not None:
    print(f'Using job handler config file: {job_handler_config_path}')
    with open(job_handler_config_path, 'r') as f:
        config0 = yaml.safe_load(f)
        config['job_handlers'].update(config0['job_handlers'])
else:
    print('Using default job handler config. To override, set SERIESVIEW_JOB_HANDLER_CONFIG to path of a yaml file.')

def _job_handler_from_config(x):
    type0 = x['type']
    params0 = x['params']
    if type0 == 'parallel':
        return hi.ParallelJobHandler(params0['num_workers'])
    else:
        raise Exception(f'Invalid type for job handler: {type0}')

print(yaml.safe_dump(config))

class job_handler:
    misc = _job_handler_from_config(config['job_handlers']['misc'])
    timeseries = _job_handler_from_config(config['job_handlers']['timeseries'])