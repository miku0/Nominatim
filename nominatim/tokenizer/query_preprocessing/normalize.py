# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2023 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
This file normalizes text using ICU, a library that performs conversion of Unicode characters.
"""
import re
from typing import List
from nominatim.api.search import query as qmod


class _NormalizationPreprocessing:
    def normalize_text(text: str) -> str:
        """ Bring the given text into a normalized form. That is the
            standardized form search will work with. All information removed
            at this stage is inevitably lost.
        """
        return cast(str, normalizer.transliterate(text))

    def __call__(
        phrases: List[qmod.Phrase]
    ) -> List[qmod.Phrase]:
        """Split a Japanese address using japanese_tokenizer.
        """
        normalized = list(filter(lambda p: p.text,
                                (qmod.Phrase(p.ptype, normalize_text(p.text))
                                for p in phrases)))
        return normalized

def create(config: QueryConfig) -> Callable[[QueryInfo], None]:
    """ Create a normalization function. 
    """
    return _NormalizationPreprocessing(config)