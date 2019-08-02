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
        """Test the Latin WordNet 2.0 API (semfields)."""

        LWN = LatinWordNet()
        assert LWN.semfields(code='611').get()[0]['english'].startswith('Human Anatomy')
        assert len(next(LWN.semfields(code='611').lemmas)['lemmas']) > 1
        assert len(next(LWN.semfields(code='611').synsets)['synsets']) > 1
        assert LWN.semfields(english='anatomy').search()[0]['code'] == '581.4'
