import unittest
from encoder import encode
class TestEncode(unittest.TestCase):

    def test_success(self):
        enc = encode.Encode()
        encodedata = enc.encoded("pass#23")
        self.assertEqual(encodedata, "pass%2323")

if __name__ == '__main__':
    unittest.main()