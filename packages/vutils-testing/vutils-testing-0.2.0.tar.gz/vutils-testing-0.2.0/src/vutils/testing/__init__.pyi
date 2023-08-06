#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/testing/__init__.pyi
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-17 14:14:50 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Type hints for `vutils.testing`."""

from typing import Callable, Dict, Optional, Tuple, Union
from unittest.mock import Mock, _patch

_ReturnsType = Optional[Union[object, Callable[[object], object]]]
_SetupFuncType = Optional[Callable[[Union[Mock, object]], None]]
_BasesType = Optional[Union[type, Tuple[type, ...]]]
_MembersType = Optional[Dict[str, object]]

def _make_patch(
    target: object, mock: Union[Mock, object], **kwargs: object
) -> _patch[Union[Mock, object]]: ...
