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
        print(next(LWN.lemmatize('virtutem')))['lemma']['lemma']
        assert next(LWN.lemmatize('virtutem'))['lemma']['lemma'] == 'uirtus'
        assert next(LWN.lemmatize('dicas', 'n'))['lemma']['morpho'] == 'n-s---fn1-'
        assert next(LWN.lemmatize('dicas', 'v1spia--3-'))['lemma']['uri'] == 'd1350'

        assert next(LWN.translate('en', 'offspring'))
        assert next(LWN.translate('en', 'love', 'v'))
