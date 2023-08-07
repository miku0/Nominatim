# from nominatim.tokenizer.sanitizers.tag_japanese import convert_kanji_sequence_to_number

# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2022 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
This icu_tokenizer divides Japanese addresses into three categories:
prefecture, municipality, and other.
The division is not strict but simple using these keywords.
"""
import re

def transliterate(text: str) -> str:
    """
    This function performs a division on the given text using a regular expression.
    """
    pattern = r'''
               (...??[都道府県])            # [group1] prefecture
               (.+?[市区町村])              # [group2] municipalities (city/wards/towns/villages)
               (.+)                         # [group3] other words
               '''
    result = re.match(pattern, text, re.VERBOSE) # perform normalization using the pattern
    if result is not None:
        joined_group = ''.join([result.group(1),', ',result.group(2),', ',result.group(3)])
        #joined_group = ''.join([result.group(1),',',result.group(2),',',result.group(3)])
        #joined_group = ''.join([result.group(1),' ',result.group(2),' ',result.group(3)])
        return joined_group
    return text
