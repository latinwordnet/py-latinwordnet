#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `latinwordnet` package."""

import unittest
from latinwordnet import LatinWordNet


class TestIndex(unittest.TestCase):
    """Tests for `latinwordnet` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_semfield(self):
        """Test the Latin WordNet API (semfields)."""

        LWN = LatinWordNet()
        assert LWN.semfields(code='611').get()[0]['english'].startswith('Human anatomy')
        assert len(LWN.semfields(code='611').lemmas[0]['lemmas']) > 1
        assert len(LWN.semfields(code='611').synsets[0]['synsets']) > 1
        assert LWN.semfields(english='anatomy').search()[0]['code'] == '581.4'
