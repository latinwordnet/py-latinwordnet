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

    def test_lemmas(self):
        """Test the Latin WordNet API (lemmas)."""

        LWN = LatinWordNet()
        assert LWN.lemmas(lemma='uirtus').get()[0]['uri'] == 'u0800'
        assert LWN.lemmas_by_uri('u0800').get()[0]['lemma'] == 'uirtus'
        assert next(LWN.lemmas(lemma='bula').search())['lemma'] == 'adfabulatio'
        assert LWN.lemmas(lemma='uirtus').synsets
        assert LWN.lemmas(lemma='uirtus').relations
