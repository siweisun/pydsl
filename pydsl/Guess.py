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


"""
guess which types are the input data. 
"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger(__name__)
from pkg_resources import Requirement, resource_filename, DistributionNotFound
from pydsl.Memory.Storage.Loader import load_checker

class Guesser:
    def __init__(self, memorylist = []):
        from pydsl.Memory.Search.Searcher import MemorySearcher
        from pydsl.Memory.Storage.Directory.Grammar import GrammarDirStorage 
        from pydsl.Memory.Storage.Dict import FileTypeDictStorage
        if not memorylist:
            try:
                dirname = resource_filename(Requirement.parse("pydsl_contrib"),"")
            except DistributionNotFound:
                pass
            else:
                memorylist.append(GrammarDirStorage(dirname + "/grammar/"))
                memorylist.append(FileTypeDictStorage(dirname + "/dict/filetype.dict"))
        self.memorylist = memorylist
        self.searcher = MemorySearcher([x.indexer() for x in memorylist])

    def __call__(self, inputstring) -> set:
        result = set()
        for summary in self.searcher.search():
            typ = None
            name = None
            try:
                for mem in self.memorylist:
                    if summary["identifier"] in mem:
                        name = summary["identifier"]
                        typ = mem.load(name)
                        break
                checker = load_checker(typ)
                if checker.check(inputstring):
                    result.add(str(name))
            except TypeError:
                continue
        return result

class FileGuesser(Guesser):
    """Guesser subclass for files only. Works like file command"""
    def __init__(self, memorylist = []):
        from pydsl.Memory.Search.Searcher import MemorySearcher
        from pydsl.Memory.Storage.Dict import FileTypeDictStorage

        if not memorylist:
            dirname = resource_filename(Requirement.parse("pydsl_contrib"),"")
            memorylist.append(FileTypeDictStorage(dirname + "/dict/filetype.dict"))
        Guesser.__init__(self, memorylist)

