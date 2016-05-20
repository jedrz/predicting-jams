#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _precision(predicted, target, i):
    predicted = set(predicted[:i])
    target = set(target[:i])
    in_common = predicted & target
    return len(in_common) / i


def quality(predicted, target):
    n = max(len(predicted), len(target))
    precisions = [_precision(predicted, target, i) for i in range(1, n + 1)]
    return sum(precisions) / n
