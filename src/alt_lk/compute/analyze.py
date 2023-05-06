import json
import math
import time
import webbrowser

from utils import Log

from alt_lk.compute._constants import DIM_X, DIM_Y
from alt_lk.data.Places import Places

log = Log('matrices')
WINDOW = 100
MIN_ALT = 0.5


def get_peak_list(idx, pers, m_latlng, m_alt, m_beta):
    peak_list = []
    for i_x in range(DIM_X):
        dis0 = pers[DIM_Y - 1, i_x]
        peak = None
        for i_y in range(DIM_Y):
            dis = pers[i_y, i_x]
            if dis != dis0 and (i_x, i_y) in idx:
                i_lat, i_lng = idx[(i_x, i_y)]
                lat, lng = m_latlng[i_lat, i_lng]
                alt = m_alt[i_lat, i_lng]
                beta = m_beta[i_lat, i_lng]
                peak = dict(
                    alt=alt,
                    beta=beta,
                    latlng=(lat, lng),
                )
                break
        peak_list.append(peak)
    return peak_list


def open_peak(peak):
    alt = peak['alt']
    d = dict(
        name="Unknown",
        latlng=peak['latlng'],
        alt=alt * 1_000,
    )
    log.debug(json.dumps(d, indent=2) + ',')

    url = 'https://www.google.lk/maps/place/' + str(peak['latlng'])
    webbrowser.open(url)
    time.sleep(0.5)


def has_nearby_mountain(peak):
    min_d = 1
    for d in Places.mountains():
        latlng_mountain = d['latlng']
        dlat, dlng = (
            peak['latlng'][0] - latlng_mountain[0],
            peak['latlng'][1] - latlng_mountain[1],
        )
        d = math.sqrt(dlat * dlat + dlng * dlng)
        if d < min_d:
            min_d = d
    return min_d < 0.002


def is_local_peak(peak_list, i_x):
    peak = peak_list[i_x]
    local_peak_list = peak_list[i_x - WINDOW: i_x + WINDOW]
    max_beta = max(peak['beta'] if peak else 0 for peak in local_peak_list)
    return peak['beta'] == max_beta


def analyze_peaks(idx, pers, m_latlng, m_alt, m_beta):
    peak_list = get_peak_list(idx, pers, m_latlng, m_alt, m_beta)
    i_display_peaks = 0
    for i_x in range(WINDOW, DIM_X - WINDOW):
        peak = peak_list[i_x]
        if (
            peak is None
            or not is_local_peak(peak_list, i_x)
            or has_nearby_mountain(peak)
            or peak['alt'] < MIN_ALT
        ):
            continue

        open_peak(peak)
        i_display_peaks += 1
        if i_display_peaks >= 10:
            break
