#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from context import predicting_jams
from predicting_jams.predict import *


@pytest.mark.parametrize("predicted,expected,result", [
    (['a'], ['a'], 1),
    (['a'], ['b'], 0),
    (['a', 'b'], ['a', 'b'], 1),
    (['a'], ['a', 'b'], 3/4),
    (['b', 'c'], ['a', 'b'], 1/4),
    (['b', 'c'], ['a', 'b', 'c'], (1/2 + 2/3) / 3),
    (['a', 'b', 'c'], ['b', 'c'], (1/2 + 2/3) / 3),
    (['a', 'b', 'c', 'd'], ['a', 'b', 'd', 'c'], (1 + 1 + 2/3 + 1) / 4)
])
def test_quality(predicted, expected, result):
    assert quality(predicted, expected) == result
