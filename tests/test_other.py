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

    def test_other(self):
        """Test the Latin WordNet API (other)."""

        LWN = LatinWordNet()
        assert LWN.lemmatize('virtutem')[0]['lemma']['lemma'] == 'uirtus'
        assert LWN.lemmatize('dicas', 'n')[0]['lemma']['morpho'] == 'n-s---fn1-'
        assert LWN.lemmatize('dicas', 'v1spia--3-')[0]['lemma']['uri'] == 'd1350'

        assert LWN.translate('en', 'offspring')
        assert LWN.translate('en', 'love', 'v')
