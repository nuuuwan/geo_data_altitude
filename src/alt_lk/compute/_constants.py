import math

from utils import Log

log = Log('_constants')

MAX_ALT = 2524

DIM = 1201
DIM2 = DIM * 5
MAX_DISTANCE = 100

MID_ALPHA = 90
ALPHA_SPAN = 90
MIN_ALPHA, MAX_ALPHA = MID_ALPHA - ALPHA_SPAN, MID_ALPHA + ALPHA_SPAN
MIN_BETA, MAX_BETA = 0, 2.5
log.debug(f'{MIN_ALPHA=}, {MAX_ALPHA=}')
log.debug(f'{MIN_BETA=}, {MAX_BETA=}')
DIM_Y = 1000
DIM_X = int(DIM_Y * (MAX_ALPHA - MIN_ALPHA) / (MAX_BETA - MIN_BETA) / 2)
log.debug(f'{DIM_X=} x {DIM_Y=}')

LATLNG0 = (6.9188473380988125, 79.85911404345833)

h0 = 0.15
R = 6371
d = math.sqrt(2 * R * h0)
log.debug(f'{R=}km, {h0=:.2f}km, {d=:.2f}km')
