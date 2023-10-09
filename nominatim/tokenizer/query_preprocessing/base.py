# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2023 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
Common data types and protocols for preprocessing.
"""
from typing import Optional, List, Mapping, Callable

from nominatim.tokenizer.query_preprocessing.config import QueryConfig
from nominatim.typing import Protocol, Final
from nominatim.api.search import query as qmod
from nominatim.tokenizer.query_preprocessing import normalize
from nominatim.tokenizer.query_preprocessing import split-key-japanese-phrases

class QueryInfo:
    """ Container class for information handed into to handler functions.
    QueryInfo has a List[Phrase] that is variable by preprocessor function.
    QueryInfo class allows us to later add more functionality to the preprocessing without breaking existing code.
    """

    def __init__(self, phrases: List[qmod.Phrase]):
        self.phrases: List[qmod.Phrase] = phrases
    
    def preprocessing(self):
        preprocess_query_functions = [
            normalize.normalize,
            split_key_japanese_phrases.split_key_japanese_phrases
        ]
        new_phrases = self.phrases.copy()
        for func in preprocess_query_functions:
            new_phrases = func(new_phrases)
        return new_phrases

class QueryHandler(Protocol):
    """ Protocol for sanitizer modules.
    """
    def create(self, config: QueryConfig) -> Callable[[QueryInfo], None]:
        """
        Create a function for sanitizing a place.

        Arguments:
            config: A dictionary with the additional configuration options
                    specified in the tokenizer configuration

        Return:
            The result is a list modified by the preprocessor.
        """
        pass
