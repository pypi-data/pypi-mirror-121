#!/bin/false
# -*- coding: utf-8 -*-

"""
A collection of functions for text manipulation.
"""


# =======================================================================================================================
# Main imports
# =======================================================================================================================
import collections
from typing import Any


# =======================================================================================================================
# Utility functions: Type introspection
# =======================================================================================================================
def is_string(obj: Any) -> bool:
    """
    Determine whether an object is a string.

    Parameters
    ----------
    obj : Any
        The object to inspect

    Returns
    -------
    bool
        True if the object is a string (i.e. `str`).
    """
    return isinstance(obj, str)


# ------------------------------------------------------------------------------------------------------------------------
def is_mapping(obj: Any) -> bool:
    """
    Determine whether an object is a mapping.

    Parameters
    ----------
    obj : Any
        The object to inspect

    Returns
    -------
    bool
        True if the object is a mapping (i.e. `collections.Mapping`).
    """
    return isinstance(obj, collections.Mapping)


# ------------------------------------------------------------------------------------------------------------------------
def is_iterable(obj: Any) -> bool:
    """
    Determine whether an object is iterable.

    Parameters
    ----------
    obj : Any
        The object to inspect

    Returns
    -------
    bool
        True if the object is iterable (i.e. `collections.Iterable`).
    """
    return isinstance(obj, collections.Iterable)


# ------------------------------------------------------------------------------------------------------------------------
def is_sequence(obj: Any) -> bool:
    """
    Determine whether an object is a sequence (non-string, non-mapping, iterable).

    Parameters
    ----------
    obj : Any
        The object to inspect

    Returns
    -------
    bool
        True if the object is a sequence.
    """
    return ( is_iterable(obj) and not is_mapping(obj) and not is_string(obj) )
