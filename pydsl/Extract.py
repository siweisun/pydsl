#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Check import checker_factory
from pydsl.Lex import lexer_factory
from pydsl.Grammar.Alphabet import Alphabet
from pydsl.Token import PositionToken


def filter_subsets(lst):
    to_remove = []
    for i, j, _ in lst:
        for x,y, _ in lst:
            if (x < i and y >= j) or (x <= i and y > j):
                to_remove.append((i,j))
                break
    result = list(lst)

    for element in lst:
        if (element[0], element[1]) in to_remove:
            result.remove(element)
    return result


def extract_alphabet(alphabet, inputdata, fixed_start = False):
    """Extract every slice of the input data that belongs to the Grammar Definition"""
    lexer = lexer_factory(alphabet, alphabet.alphabet)
    totallen = len(inputdata)
    maxl = totallen
    minl = 1
    if fixed_start:
        max_start = 1
    else:
        max_start = totallen
    result = []
    for i in range(max_start):
        for j in range(i+minl, min(i+maxl, totallen) + 1):
            try:
                lexed = lexer(inputdata[i:j])
                if lexed:
                    result.append((i,j, inputdata[i:j]))
            except:
                continue
    result = filter_subsets(result)
    return [PositionToken(content, None, left, right) for (left, right, content) in result]

def extract(grammar, inputdata, fixed_start = False):
    """Extract every slice of the input data that belongs to the Grammar Definition"""
    checker = checker_factory(grammar)
    totallen = len(inputdata)
    try:
        maxl = grammar.maxsize or totallen
    except NotImplementedError:
        maxl = totallen
    try:
        #minl = grammar.minsize #FIXME: It won't work with incompatible alphabets
        minl = 1
    except NotImplementedError:
        minl = 1
    if fixed_start:
        max_start = 1
    else:
        max_start = totallen
    result = []
    for i in range(max_start):
        for j in range(i+minl, min(i+maxl, totallen) + 1):
            check = checker.check(inputdata[i:j])
            if check:
                result.append(PositionToken(inputdata[i:j], None, i, j))
    return result

