import kachery_client as kc

from ..svseries import SVSeries


@kc.taskfunction('seriesview.get_series_manifest.1', type='pure-calculation')
def task_get_series_manifest(series_uri):
    S = SVSeries.from_uri(series_uri)
    return S.to_dict()
