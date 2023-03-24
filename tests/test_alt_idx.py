import unittest

from alt_lk import AltIdx

TEST_ALT_IDX = AltIdx((7, 80))


class TestAltIdx(unittest.TestCase):
    def test_init(self):
        self.assertEqual(TEST_ALT_IDX.idx_latlng, (7, 80))
        self.assertEqual(TEST_ALT_IDX.max_lat, 7)
        self.assertEqual(TEST_ALT_IDX.min_lng, 80)
        self.assertEqual(TEST_ALT_IDX.min_lat, 6)
        self.assertEqual(TEST_ALT_IDX.max_lng, 81)

    def test_is_included(self):
        for latlng, expected_is_included in [
            [(6, 80), True],
            [(6.5, 80.5), True],
            [(6.9999, 80.9999), True],
            [(7, 80), False],
            [(6, 81), False],
            [(7, 81), False],
        ]:
            self.assertEqual(
                TEST_ALT_IDX.is_included(latlng),
                expected_is_included,
            )

    def test_get(self):
        for latlng, expected_alt in [
            [
                (7.000903534417337, 80.77334660665547),
                2519,
            ],  # Pidurutalagala, Nuwara-Eliya
            [
                (6.809685383463292, 80.49934524308341),
                2161,
            ],  # Sri Pada, Ratnapura
            [
                (6.93337572096937, 81.11417756846475),
                2027,
            ],  # Namunukula
            [
                (7.455236415682045, 80.75044300043233),
                1882,
            ],  # Gombaniya, Knuckles
            [
                (7.189690332388084, 80.43430099425271),
                767,
            ],  # Bible Rock
            [
                (8.118475410630339, 80.6511716706701),
                529,
            ],  # Ritigala
            [
                (7.293064971344079, 80.63769056474186),
                512,
            ],  # Kandy
            [
                (7.875209118437386, 80.65122359594757),
                165,
            ],  # Dambulla
            [
                (6.917295379444161, 79.86478500974187),
                12,
            ],  # Town Hall, Colombo
            []
        ]:
            self.assertEqual(AltIdx.get(latlng), expected_alt)
