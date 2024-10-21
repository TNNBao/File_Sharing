import unittest
from tracker.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')

    def test_add_peer(self):
        self.db.add_peer('testfile.txt', '127.0.0.1:9000')
        peers = self.db.get_peers('testfile.txt')
        self.assertEqual(peers, ['127.0.0.1:9000'])

    def test_get_peers(self):
        self.db.add_peer('testfile.txt', '127.0.0.1:9000')
        peers = self.db.get_peers('testfile.txt')
        self.assertEqual(peers, ['127.0.0.1:9000'])

if __name__ == '__main__':
    unittest.main()
