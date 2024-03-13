# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2024 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
Tests for preprocessing of Japanese query for ICU tokenizer.
"""
from pathlib import Path

import pytest
import pytest_asyncio

from nominatim.api import NominatimAPIAsync
from nominatim.api.search.query import Phrase, PhraseType, BreakType
import nominatim.api.search.icu_tokenizer as tok

def make_phrase(query):
    return [Phrase(PhraseType.NONE, s) for s in query.split(',')]

@pytest_asyncio.fixture
async def conn(table_factory):
    """ Create an asynchronous SQLAlchemy engine for the test DB.
    """
    table_factory('nominatim_properties',
                  definition='property TEXT, value TEXT',
                  content=(('tokenizer_import_normalisation', ':: lower();'),
                           ('tokenizer_import_transliteration', "'1' > '/1/'; 'ä' > 'ä '")))
    table_factory('word',
                  definition='word_id INT, word_token TEXT, type TEXT, word TEXT, info JSONB')

    api = NominatimAPIAsync(Path('/invalid'), {})
    async with api.begin() as conn:
        yield conn
    await api.close()

@pytest.mark.asyncio
async def test_split_key_japanese_full(conn):
    ana = await tok.create_query_analyzer(conn)

    query = await ana.analyze_query(make_phrase('大阪府大阪市大阪1-2'))
    assert query.source[0].text == '大阪府, 大阪市, 大阪1-2'

    query = await ana.analyze_query(make_phrase('東京都町田市1-2'))
    assert query.source[0].text == '東京都, 町田市, 1-2'

    query = await ana.analyze_query(make_phrase('東京都中央区1-2'))
    assert query.source[0].text == '東京都, 中央区, 1-2'

    query = await ana.analyze_query(make_phrase('東京都中央區1-2'))
    assert query.source[0].text == '東京都, 中央區, 1-2'

@pytest.mark.asyncio
async def test_split_key_japanese_pattern(conn):
    ana = await tok.create_query_analyzer(conn)

    query = await ana.analyze_query(make_phrase('中央区1-2'))
    assert query.source[0].text == '中央区, 1-2'

    query = await ana.analyze_query(make_phrase('東京都中央区'))
    assert query.source[0].text == '東京都, 中央区'