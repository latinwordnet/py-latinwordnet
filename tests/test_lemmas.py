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
        assert LWN.lemmas(lemma='virtus').get()[0]['uri'] == 'u0800'
        assert len(LWN.lemmas(pos='n').get()) > 30000
        assert len(LWN.lemmas(morpho='rp--------').get()) > 4000
        assert LWN.lemmas_by_uri('u0800').get()[0]['lemma'] == 'uirtus'
        assert next(LWN.lemmas(lemma='bula').search())['lemma'] == 'adfabulatio'
        assert LWN.lemmas(lemma='virtus').synsets
        assert LWN.lemmas(lemma='virtus').relations
        LWN.lemmas(lemma='uirtus').synsets_relations
