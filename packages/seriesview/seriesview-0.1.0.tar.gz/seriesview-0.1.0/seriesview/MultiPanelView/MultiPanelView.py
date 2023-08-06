from typing import Any, Dict, List
import kachery_client as kc
from figurl import Figure
from ..svseries import SVSeries

class Panel:
    def __init__(self, type: str, label: str, data: Any):
        self._type = type
        self._label = label
        self._data = data
    @property
    def type(self):
        return self._type
    @property
    def label(self):
        return self._label
    @property
    def data(self):
        return self._data

# EventAmplitudes
# ContinuousTraces
# RasterPlot
# Position
# ProbabilityDensity

class MultiPanelView:
    def __init__(self):
        self._panels: List[Panel] = []
    def add_event_amplitudes_panel(self, event_amplitudes: SVSeries, *, label: str):
        assert event_amplitudes.type == 'discrete', 'Unexpected type for event amplitudes timeseries'
        self._panels.append(Panel(
            type='EventAmplitudes',
            label=label,
            data={
                'seriesUri': event_amplitudes.to_uri()
            }
        ))
    @property
    def num_panels(self):
        return len(self._panels)
    def panel(self, index: int):
        return self._panels[index]
    def figurl(self):
        data = {
            'panels': [{
                'type': p.type,
                'label': p.label,
                'data': p.data
            } for p in self._panels]
        }
        return Figure(type='seriesview.multipanel-timeseries.2', data=data)
