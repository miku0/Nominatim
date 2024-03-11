# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2023 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
This file normalizes text using ICU, a library that performs conversion of Unicode characters.
"""
from typing import List, Callable, Any, cast
from nominatim.api.search import query as qmod
from nominatim.tokenizer.query_preprocessing.config import QueryConfig
from nominatim.tokenizer.query_preprocessing.base import QueryInfo
from nominatim.api.search import icu_tokenizer
from nominatim.api.connection import SearchConnection
from nominatim.api.search.icu_tokenizer import ICUQueryAnalyzer


class _NormalizationPreprocessing:

    def __init__(self, config: QueryConfig, normalizer: Any) -> None:
        self.config = config
        self.normalizer = normalizer

    def __call__(
        self, phrases: List[qmod.Phrase]
    ) -> List[qmod.Phrase]:
        """Normalize text using ICU.
        """
        normalized = list(filter(lambda p: p.text,
                                (qmod.Phrase(p.ptype, self.normalize_text(p.text))
                                for p in phrases)))
        return normalized
    
    def normalize_text(self, text: str) -> str:
        return cast(str, self.normalizer.transliterate(text))

def create(config: QueryConfig, normalizer: Any) -> Callable[[List[qmod.Phrase]], List[qmod.Phrase]]:
    """ Create a normalization function. 
    """
    return _NormalizationPreprocessing(config, normalizer)