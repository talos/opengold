# -*- coding: utf-8 -*-

"""
Test server.py with HTML requests.  Starts server and mongrel at start
of test class.
"""

import requests

from helpers import TestOpengoldServer, HOST

class TestServerTemplates(TestOpengoldServer):
    """
    Tests serving templates directly.
    """

    def new_session(self):
        return requests.session(timeout=10)

    def test_load_game_index_no_games(self):
        s = self.new_session()
        resp = s.get(HOST + '/')
        self.assertRegexpMatches(resp.content, "No games currently available")

    def test_load_game_index_several_games(self):
        s = self.new_session()

        s.post(HOST + '/piper at the gates of dawn/join', data={'player':'barrett'})
        s.post(HOST + '/saucerful of secrets/join', data={'player':'gilmour'})
        s.post(HOST + '/meddle/join', data={'player':'gilmour'})
        resp = s.get(HOST + '/')
        self.assertRegexpMatches(resp.content, "piper at the gates of dawn")
        self.assertRegexpMatches(resp.content, "saucerful of secrets")
        self.assertRegexpMatches(resp.content, "meddle")

    def test_load_nonexistent_game(self):
        """
        Going to a nonexistent game just generates the page to join the game.
        """
        s = self.new_session()
        resp = s.get(HOST + '/nada/')
        self.assertRegexpMatches(resp.content, '(?i)join this game as')

    def test_join_game_notice(self):
        s = self.new_session()

        s.post(HOST + '/mount/join', data={'player': 'joseph'})

        resp = s.get(HOST + '/mount/')
        self.assertRegexpMatches(resp.content, "(?i)joined")

    def test_start_game_notice(self):
        s = self.new_session()

        s.post(HOST + '/mount/join', data={'player': 'joseph'})
        s.post(HOST + '/mount/start')

        resp = s.get(HOST + '/mount/')
        self.assertRegexpMatches(resp.content, "(?i)wants to start venturing")

    def test_cant_start_game_alone(self):
        s = self.new_session()

        s.post(HOST + '/cave/join', data={'player': 'hermit'})
        s.post(HOST + '/cave/start')

        resp = s.get(HOST + '/cave/')
        self.assertRegexpMatches(resp.content, "(?i)waiting for more players")

    def xtest_game_not_started_notice(self):
        jack = self.new_session()
        jill = self.new_session()

        jack.post(HOST + '/hill/join', data={'player': 'jack'})
        jill.post(HOST + '/hill/join', data={'player': 'jill'})

        resp = jack.get(HOST + '/hill/')
        self.assertRegexpMatches(resp.content, "(?i)game has not yet started")

    def test_start_game(self):
        jack = self.new_session()
        jill = self.new_session()

        jack.post(HOST + '/hill/join', data={'player': 'jack'})
        jack.post(HOST + '/hill/start')
        jill.post(HOST + '/hill/join', data={'player': 'jill'})
        jill.post(HOST + '/hill/start')

        resp = jack.get(HOST + '/hill/')
        self.assertRegexpMatches(resp.content, "(?i)round .*1")
        self.assertRegexpMatches(resp.content, "(?i)is in the deck")

    def test_move(self):
        jack = self.new_session()
        jill = self.new_session()

        jack.post(HOST + '/hill/join', data={'player': 'jack'})
        jack.post(HOST + '/hill/start')
        jill.post(HOST + '/hill/join', data={'player': 'jill'})
        jill.post(HOST + '/hill/start')
        jack.post(HOST + '/hill/move', data={'move': 'han'})

        resp = jack.get(HOST + '/hill/')
        self.assertRegexpMatches(resp.content, "(?i) made their move")

    def test_next_round_double_landos(self):
        jack = self.new_session()
        jill = self.new_session()

        jack.post(HOST + '/hill/join', data={'player': 'jack'})
        jack.post(HOST + '/hill/start')
        jill.post(HOST + '/hill/join', data={'player': 'jill'})
        jill.post(HOST + '/hill/start')

        jack.post(HOST + '/hill/move', data={'move': 'lando'})
        jill.post(HOST + '/hill/move', data={'move': 'lando'})

        resp = jack.get(HOST + '/hill/')
        self.assertRegexpMatches(resp.content, r'(?i) landoed out, capturing .*\d+.* gold and leaving .*\d+.* behind')
        self.assertRegexpMatches(resp.content, r'(?i)round .*2')
