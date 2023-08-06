#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/testing/utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-14 17:12:48 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Miscellaneous utilities."""

import importlib
from typing import TYPE_CHECKING, Iterable

from vutils.testing.mock import PatcherFactory

if TYPE_CHECKING:
    from vutils.testing import _BasesType, _MembersType


def make_type(
    name: str,
    bases: "_BasesType" = None,
    members: "_MembersType" = None,
    **kwargs: object,
) -> type:
    """
    Make a new type.

    :param name: The type name
    :param bases: The type's bases
    :param members: The definition of type's members and methods
    :param kwargs: Additional arguments passed to `type`
    :return: the new type

    This function becomes handy when creating types used as test data. For
    instance, instead of ::

        class ErrorA(Exception):
            pass

        class ErrorB(Exception):
            pass

        class MyTestCase(TestCase):

            def setUp(self):
                self.error_a = ErrorA
                self.error_b = ErrorB

    it is possible to write::

        class MyTestCase(TestCase):

            def setUp(self):
                self.error_a = make_type("ErrorA", Exception)
                self.error_b = make_type("ErrorB", Exception)

    This helps to keep test data in the proper scope and to reduce the size of
    the code base.
    """
    if bases is None:
        bases = ()
    if not isinstance(bases, tuple):
        bases = (bases,)
    if members is None:
        members = {}
    return type(name, bases, members, **kwargs)


class TypingPatcher(PatcherFactory):
    """Patch type hints."""

    __slots__ = ()

    def setup(self) -> None:
        """Set up the patcher."""
        self.add_spec("typing.TYPE_CHECKING", new=True)

    def extend(self, target: str, symbols: Iterable[str]) -> None:
        """
        Specify patches for *symbols*.

        :param target: The target module
        :param symbols: The list of symbols to be patched in the *target*
        """
        for symbol in symbols:
            self.add_spec(f"{target}.{symbol}", new=symbol, create=True)


def cover_typing(name: str, symbols: Iterable[str]) -> None:
    """
    Cover the ``if typing.TYPE_CHECKING`` branch.

    :param name: The module name
    :param symbols: The list of symbols

    To make the code like ::

        if typing.TYPE_CHECKING:
            from foo import _TypeA, _TypeB

    in ``foo.bar`` module covered by tests, call ::

        cover_typing("foo.bar", ["_TypeA", "_TypeB"])

    in the test code after imports.
    """
    module = importlib.import_module(name)
    patcher = TypingPatcher()
    patcher.extend(name.rsplit(".", 1)[0], symbols)

    with patcher.patch():
        importlib.reload(module)
    importlib.reload(module)
