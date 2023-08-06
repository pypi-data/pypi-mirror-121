import numpy as np
import kachery_client as kc
import hither2 as hi
from seriesview.config import job_cache, job_handler
from seriesview.serialize_wrapper import serialize_wrapper

@kc.taskfunction('seriesview.get_array.2', type='pure-calculation')
@serialize_wrapper
def task_get_array(dtype: str, uri: str):
    local_fname = kc.load_file(uri)
    if local_fname is None:
        raise Exception(f'Unable to load array: {uri}')
    return {
        'array': np.fromfile(local_fname, dtype=dtype)
    }