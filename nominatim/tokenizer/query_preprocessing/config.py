# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2023 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
Configuration for Sanitizers.
"""
from typing import Sequence, Union, Optional, Pattern, Callable, Any, TYPE_CHECKING
from collections import UserDict
import re

from nominatim.errors import UsageError

# working around missing generics in Python < 3.8
# See https://github.com/python/typing/issues/60#issuecomment-869757075
if TYPE_CHECKING:
    _BaseUserDict = UserDict[str, Any]
else:
    _BaseUserDict = UserDict

class QueryConfig(_BaseUserDict):
    """ The `QueryConfig` class is a read-only dictionary
        with configuration options for the preprocessor.
        In addition to the usual dictionary functions, the class provides
        accessors to standard preprocessor options that are used by many of the
        preprocessors.
    """
