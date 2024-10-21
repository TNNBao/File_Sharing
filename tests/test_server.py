import unittest
from tracker.server import TrackerServer
from tracker.database import Database

class TestTrackerServer(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')
        self.server = TrackerServer()
        self.server.db = self.db

    def test_register_file(self):
        response = self.server.process_message(json.dumps({
            'action': 'register',
            'filename': 'testfile.txt',
            'peer': '127.0.0.1:9000'
        }))
        self.assertEqual(response, {'status': 'success'})

    def test_search_file(self):
        self.server.db.add_peer('testfile.txt', '127.0.0.1:9000')
        response = self.server.process_message(json.dumps({
            'action': 'search',
            'filename': 'testfile.txt'
        }))
        self.assertEqual(response, {'peers': ['127.0.0.1:9000']})

if __name__ == '__main__':
    unittest.main()
