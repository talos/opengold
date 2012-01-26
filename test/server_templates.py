# -*- coding: utf-8 -*-

"""
Test server.py with HTML requests.  Starts server and mongrel at start
of test class.
"""

import unittest
import requests
import urllib2

from helpers import TestOpengoldServer, HOST

class TestServerTemplates(TestOpengoldServer):
    """
    Test JSON methods on the server.  Does not hit the template side of things.
    """

    def test_load_game_index_no_games(self):
        s = requests.session()
        resp = s.get(HOST + '/')
        self.assertRegexpMatches(resp.content, "No games currently available")

    def test_load_nonexistent_game(self):
        s = requests.session()
        self.assertEquals(404, s.get(HOST + '/nada').status_code)

# Primitive runner!
if __name__ == '__main__':
    unittest.main()
