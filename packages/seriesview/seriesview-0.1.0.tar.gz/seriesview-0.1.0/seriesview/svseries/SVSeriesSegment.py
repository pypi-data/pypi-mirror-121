import numpy as np
from typing import Union
import kachery_client as kc


class SVSeriesSegment:
    def __init__(self, *,
        start_time: float,
        end_time: float,
        num_samples: float,
        min_value: float,
        max_value: float,
        timestamps_dtype: str,
        timestamps_uri: str,
        values_dtype: str,
        values_uri: str
    ) -> None:
        self._start_time = start_time
        self._end_time = end_time
        self._num_samples = num_samples
        self._min_value = min_value
        self._max_value = max_value
        self._timestamps_dtype = timestamps_dtype
        self._timestamps_uri = timestamps_uri
        self._values_dtype = values_dtype
        self._values_uri = values_uri
        self._timestamps: Union[np.array, None] = None
        self._values: Union[np.array, None] = None
    def to_dict(self):
        return {
            'start_time': float(self._start_time),
            'end_time': float(self._end_time),
            'num_samples': int(self._num_samples),
            'min_value': float(self._min_value),
            'max_value': float(self._max_value),
            'timestamps_dtype': self._timestamps_dtype,
            'timestamps_uri': self._timestamps_uri,
            'values_dtype': self._values_dtype,
            'values_uri': self._values_uri
        }
    @property
    def start_time(self): return self._start_time
    @property
    def end_time(self): return self._end_time
    @property
    def num_samples(self): return self._num_samples
    def get_samples(self):
        if self._timestamps is None:
            self._timestamps = _load_timestamps_from_uri(self._timestamps_uri, dtype=self._timestamps_dtype)
        if self._values is None:
            self._values = _load_values_from_uri(self._values_uri, dtype=self._values_dtype)
        return self._timestamps, self._values
    @staticmethod
    def from_dict(d: dict):
        return SVSeriesSegment(
            start_time=d['start_time'],
            end_time=d['end_time'],
            num_samples=d['num_samples'],
            min_value=d['min_value'],
            max_value=d['max_value'],
            timestamps_dtype=d['timestamps_dtype'],
            timestamps_uri=d['timestamps_uri'],
            values_dtype=d['values_dtype'],
            values_uri=d['values_uri']
        )
    @staticmethod
    def from_numpy(*,
        start_time: float,
        end_time: float,
        timestamps: np.array,
        values: np.array
    ):
        if values.dtype == np.float32:
            values_dtype = 'float32'
        elif values.dtype == np.int16:
            values_dtype = 'int16'
        else:
            raise Exception(f'Unsupported dtype for values: {values.dtype}')
        if timestamps.dtype == np.float32:
            timestamps_dtype = 'float32'
        elif timestamps.dtype == np.float64:
            timestamps_dtype = 'float64'
        else:
            raise Exception(f'Unsupported dtype for timestamps: {values.dtype}')
        with kc.TemporaryDirectory() as tmpdir:
            timestamps_fname = f'{tmpdir}/timestamps.dat'
            timestamps.tofile(timestamps_fname)
            values_fname = f'{tmpdir}/values.dat'
            values.tofile(values_fname)
            timestamps_uri = kc.store_file(timestamps_fname)
            values_uri = kc.store_file(values_fname)
        return SVSeriesSegment(
            start_time=start_time,
            end_time=end_time,
            num_samples=len(timestamps),
            min_value=np.min(values),
            max_value=np.max(values),
            timestamps_dtype=timestamps_dtype,
            timestamps_uri=timestamps_uri,
            values_dtype=values_dtype,
            values_uri=values_uri
        )

def _load_timestamps_from_uri(uri: str, *, dtype: str):
    if dtype == 'float32':
        d = np.float32
    elif dtype == 'float64':
        d = np.float64
    else:
        raise Exception(f'Unexpected dtype for loading timestamps: {dtype}')
    local_fname = kc.load_file(uri)
    if local_fname is None:
        raise Exception(f'Unable to load timestamps: {uri}')
    return np.fromfile(local_fname, dtype=d)

def _load_values_from_uri(uri: str, *, dtype: str):
    if dtype == 'float32':
        d = np.float32
    elif dtype == 'int16':
        d = np.int16
    else:
        raise Exception(f'Unexpected dtype for loading values: {dtype}')
    local_fname = kc.load_file(uri)
    if local_fname is None:
        raise Exception(f'Unable to load values: {uri}')
    return np.fromfile(local_fname, dtype=d)