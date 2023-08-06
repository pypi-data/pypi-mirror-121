from typing import List, Literal, Union
import numpy as np
import math
import kachery_client as kc
from .SVSeriesSegment import SVSeriesSegment

SeriesType = Union[Literal['continuous'], Literal['discrete'], Literal['event']]

class SVSeries:
    def __init__(self, *,
        type: SeriesType,
        sampling_frequency: Union[float, None]
    ) -> None:
        self._type = type
        self._sampling_frequency = sampling_frequency
        self._segments: List[SVSeriesSegment] = []
    def add_segment(self, segment: SVSeriesSegment):
        self._segments.append(segment)
    def add_numpy_segment(self, *, start_time: float, end_time: float, timestamps: np.array, values: np.array):
        self.add_segment(SVSeriesSegment.from_numpy(
            start_time=start_time,
            end_time=end_time,
            timestamps=timestamps,
            values=values
        ))
    @property
    def type(self): return self._type
    @property
    def sampling_frequency(self): return self._sampling_frequency
    def get_samples(self, start: Union[None, float]=None, end: Union[None, float]=None):
        timestamps_list: List[np.array] = []
        values_list: List[np.array] = []
        for s in self._segments:
            if start < s.end_time and end > s.start_time:
                ts, v = s.get_samples()
                inds = np.argwhere((start <= ts) & (ts < end))
                if len(inds) > 0:
                    timestamps_list.append(ts[inds])
                    values_list.append(v[inds])
        if len(timestamps_list) == 0:
            return np.array([]), np.array([])
        timestamps = np.concatenate(timestamps_list)
        values = np.concatenate(values_list)
        return timestamps, values
    def to_dict(self):
        return {
            'type': self._type,
            'sampling_frequency': float(self._sampling_frequency) if self._sampling_frequency is not None else None,
            'segments': [s.to_dict() for s in self._segments]
        }
    def to_uri(self):
        return kc.store_json(self.to_dict())
    @staticmethod
    def from_dict(d: dict):
        x = SVSeries(type=d['type'], sampling_frequency=d['sampling_frequency'])
        for s in d['segments']:
            x.add_segment(SVSeriesSegment.from_dict(s))
        return x
    @staticmethod
    def from_uri(uri: str):
        return SVSeries.from_dict(kc.load_json(uri))
    @staticmethod
    def from_numpy(*,
        type: SeriesType,
        sampling_frequency: Union[float, None],
        start_time: float,
        end_time: float,
        segment_duration: float,
        timestamps: np.array,
        values: np.array
    ):
        x = SVSeries(type=type, sampling_frequency=sampling_frequency)
        num_segments = math.ceil((end_time - start_time) / segment_duration)
        for i in range(num_segments):
            t1 = start_time + i * segment_duration
            t2 = min(t1 + segment_duration, end_time)
            inds = np.argwhere((t1 <= timestamps) & (timestamps < t2))
            ts = timestamps[inds]
            v = values[inds]
            x.add_numpy_segment(
                start_time=t1,
                end_time=t2,
                timestamps=ts,
                values=v
            )
        return x