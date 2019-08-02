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
        """Test the Latin WordNet 2.0 API (synsets)."""

        LWN = LatinWordNet()
        assert LWN.synsets(pos='n', offset='04349777').get()[0]['gloss'].startswith(
            'possession of the qualities'
        )
        assert LWN.synsets(pos='n', offset='04349777').lemmas
        assert 'antonyms' in LWN.synsets(pos='n', offset='04349777').relations
        assert len(LWN.synsets(pos='p').get()) > 3
        assert LWN.synsets(pos='n', offset='04349777').sentiment['objectivity'] == 0.75
        assert LWN.synsets(gloss='warfare').search()
