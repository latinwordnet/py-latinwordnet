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

    def test_index(self):
        """Test the Latin WordNet 2.0 API (index)."""

        LWN = LatinWordNet()
        assert next(LWN.index())['lemma'] == 'Aaron'
        assert next(LWN.index(pos='v'))['lemma'] == 'abaestumo'
        assert next(LWN.index(morpho='aps---mn1-'))['lemma'] == 'abacinus'


