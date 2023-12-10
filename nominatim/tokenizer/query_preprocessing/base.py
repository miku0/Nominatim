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
from nominatim.api.search import Phrase

class QueryInfo:
    """ Container class for information handed into to handler functions.
    QueryInfo has a List[Phrase] that is variable by preprocessor function.
    QueryInfo class allows us to later add more functionality to the preprocessing without breaking existing code.
    """
    def __init__(self, phrases: List[Phrase]):
        self.phrases: List[Phrase] = phrases


class QueryHandler(Protocol):
    """ Protocol for query modules.
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
