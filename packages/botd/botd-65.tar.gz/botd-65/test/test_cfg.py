# This file is placed in the Public Domain.

import unittest

from bot.obj import Default, edit
from bot.run import parse_txt

cfg = Default()

class Test_Cfg(unittest.TestCase):
    def test_parse(self):
        parse_txt(cfg, "m=irc")
        self.assertEqual(cfg.sets.m, "irc")

    def test_parse2(self):
        parse_txt(cfg, "m=irc,rss")
        self.assertEqual(cfg.sets.m, "irc,rss")

    def test_edit(self):
        d = Default({"m": "irc,rss"})
        edit(cfg, d)
        self.assertEqual(cfg.m, "irc,rss")
