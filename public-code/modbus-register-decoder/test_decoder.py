import unittest

from decoder import decode_signal


class RegisterDecoderTests(unittest.TestCase):
    def test_word_order_changes_32_bit_float(self):
        # 25.5 is 0x41CC0000; the sample source stores its words in reverse order.
        self.assertEqual(25.5, decode_signal(
            [0x0000, 0x41CC], {"type": "FLOAT32", "endian": "CDAB"}))

    def test_signed_bitfield_and_scaling(self):
        self.assertEqual(-0.5, decode_signal(
            [0b11110], {"type": "SINT", "bits_hi": 4, "bits_lo": 1,
                         "scale": 0.5}))

    def test_missing_or_invalid_reading_is_not_reported_as_a_number(self):
        self.assertIsNone(decode_signal([0x7F80, 0], {"type": "FLOAT32"}))
        self.assertIsNone(decode_signal([], {"type": "UINT"}))
        self.assertIsNone(decode_signal([200], {"type": "UINT", "valid_range": [0, 100]}))


if __name__ == "__main__":
    unittest.main()
