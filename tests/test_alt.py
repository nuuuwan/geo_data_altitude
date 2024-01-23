import unittest

from alt_lk import Alt

TEST_DATA_LIST = [
    {
        "name": "Lipton Circus, Colombo",
        "latlng": (6.917283145461265, 79.8647928104344),
        "expected_alt": 13,
    },
    {
        "name": "Pidurutalagala",
        "latlng": (7.000925069638563, 80.77341850688242),
        "expected_alt": 2504,
    },
    {
        "name": "Sri Paada",
        "latlng": (6.809498226498262, 80.49925188865949),
        "expected_alt": 2184,
    },
    {
        "name": "Kandy Clock Tower, Kandy",
        "latlng": (7.2931324033205325, 80.63502748186357),
        "expected_alt": 505,
    },
    {
        "name": "Grand Roundabout, Nuwara Eliya",
        "latlng": (6.967671358450489, 80.76758495578306),
        "expected_alt": 1883,
    },
    {
        "name": "War Memorial, Galle",
        "latlng": (6.030583497505944, 80.21599402784966),
        "expected_alt": 13,
    },
    {
        "name": "Thiruvalluvar Statue, Jaffna",
        "latlng": (9.665119015313726, 80.00934379594969),
        "expected_alt": 5,
    },
    {
        "name": "Railway Station, Trincomalee",
        "latlng": (8.584698672875373, 81.22584654491557),
        "expected_alt": 7,
    },
    {
        "name": "Clock Tower, Batticaloa",
        "latlng": (7.714131775076944, 81.69771058017439),
        "expected_alt": 11,
    },
    {
        "name": "Thuparamaya, Anuradhapura",
        "latlng": (8.355336201802075, 80.39648276371774),
        "expected_alt": 90,
    },
    {
        "name": "Kirigalpotta",
        "latlng": (6.798998326979714, 80.7666713506962),
        "expected_alt": 2341,
    },
    {
        "name": "Totapola",
        "latlng": (6.833308152755971, 80.81967069953289),
        "expected_alt": 2338,
    },
    {
        "name": "Gongala",
        "latlng": (6.38585242759519, 80.65383469745277),
        "expected_alt": 1313,
    },
]


class TestCase(unittest.TestCase):
    def test_alt(self):
        for d in TEST_DATA_LIST:
            name = d['name']
            latlng = d['latlng']
            expected_alt = d['expected_alt']
            computed_alt = Alt.from_latlng(latlng)
            self.assertEqual(
                expected_alt,
                computed_alt,
                f'{name} ({latlng}): {expected_alt} != {computed_alt}',
            )
