#!/bin/false
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------------------------------------
# Import and pathing setup
# ------------------------------------------------------------------------------------------------------------------------
import os
import pathlib
from typing import Any, Dict, Iterable, Optional, Union

from pt.ptutils.io import get_loader, get_saver, load_txt, save_txt
from pt.ptutils.globbing import get_subdirs, get_subfiles
from pt.ptutils.text import strip_line_ending
from pt.ptutils.undefined import UNDEFINED, is_defined


# ------------------------------------------------------------------------------------------------------------------------
# Typehint helpers
# ------------------------------------------------------------------------------------------------------------------------
PathLike = Union[str, pathlib.Path, 'Path', 'File', 'Folder']
PathList = Iterable[PathLike]


# ------------------------------------------------------------------------------------------------------------------------
# Class: Path
# ------------------------------------------------------------------------------------------------------------------------
class Path(pathlib.Path):
    def __init__(self, path: PathLike):
        super().__init__(path)

    # --------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def path_of(path: PathLike) -> 'Path':
        return Path(path)

    # --------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def names_of(paths: PathList) -> Iterable[str]:
        for path in paths:
            return Path.path_of(path).name

    # --------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def relative_paths_to(paths: PathList, reference: PathLike) -> Iterable[str]:
        return (pathlib.Path(path).relative_to(reference) for path in paths)


# =======================================================================================================================
# Class: File
# =======================================================================================================================
class File(Path):
    """ Class to simplify common file operations. """

    # --------------------------------------------------------------------------------------------------------------------
    def __init__(self, path: PathLike):
        super().__init__(path)
        self._loader  = get_loader(str(self), default=load_txt)
        self._saver   = get_saver(str(self), default=save_txt)

    # --------------------------------------------------------------------------------------------------------------------
    def initialize_content(self, content: Any = UNDEFINED) -> None:
        if is_defined(content):
            if not self.exists:
                self.content = content

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def content(self) -> Any:
        return self._loader(self)

    # --------------------------------------------------------------------------------------------------------------------
    @content.setter
    def content(self, value) -> None:
        self._saver(self, value)

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def lines(self) -> Iterable[str]:
        with open(self, 'r') as filp:
            for line in filp.readlines():
                yield strip_line_ending( line )


# =======================================================================================================================
# Class: Folder
# =======================================================================================================================
class Folder(Path):

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def subdirectories(self) -> PathList:
        return self.search_subdirectories(self)

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def files(self) -> PathList:
        return self.search_files(self)

    # --------------------------------------------------------------------------------------------------------------------
    def search_subdirectories(self, pattern=None, recursive=False):
        for fullpath in get_subdirs(self, pattern=pattern, recursive=recursive):
            yield Folder(fullpath)

    # --------------------------------------------------------------------------------------------------------------------
    def search_files(self, pattern=None, recursive=False):
        for fullpath in get_subfiles(self, pattern=pattern, recursive=recursive):
            yield File(fullpath)

    # --------------------------------------------------------------------------------------------------------------------
    def child(self, name) -> Path:
        return Path(self / name)

    # --------------------------------------------------------------------------------------------------------------------
    def child_file(self, path: PathLike) -> 'File':
        return File(self / path)

    # --------------------------------------------------------------------------------------------------------------------
    def child_folder(self, path: PathLike) -> 'Folder':
        return Folder(self / path)


# =======================================================================================================================
# Class: FolderSet
# =======================================================================================================================
class FolderSet:
    def __init__(self, root: PathLike, structure: Optional[Dict[str, Any]] = None):
        self._root      = Folder(root)
        self._structure = structure
        self._cache     = dict()

    # --------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, name: PathLike):
        head, tail = os.path.split(name)
        child = self[head]
        return child / tail if tail else child

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def folder(self) -> Folder:
        return self._root

    # --------------------------------------------------------------------------------------------------------------------
    def __getattr__(self, name: str) -> Union['FolderSet', 'File']:
        try:
            return self[name]
        except Exception as e:
            raise AttributeError(f"Object of type {type(self)} has no '{name}' attribute.") from e

    # --------------------------------------------------------------------------------------------------------------------
    def __getitem__(self, name: str) -> Union['FolderSet', 'File']:
        if name.startswith('$$'):
            name = name[2:]

        child = self._root.child(name)
        if not child.exists():
            raise KeyError(f"Object '{name}' is not found in directory '{self._root}'.")

        if child.is_dir():
            if self._structure is not None:
                if name not in self._structure:
                    if (
                        ('$$folders' not in self._structure) or
                        (name not in self._structure['$$folders'])
                    ):
                        raise KeyError(
                            f"Object '{name}' is not defined in the "
                            f"FolderSet structure for '{self._root}', and "
                            "so may not be accessed."
                        )
                    return FolderSet(root=child, structure=None)
                return FolderSet(root=child, structure=self._structure[name])
            return FolderSet(root=child, structure=None)

        elif child.is_file():
            if (self._structure is not None) and ('$$files' in self._structure):
                if name not in self._structure['$$files']:
                    raise KeyError(
                        f"Object '{name}' is not defined in the "
                        f"FolderSet structure for '{self._root}', and "
                        "so may not be accessed."
                    )
            return File(path=child)

        raise KeyError(f"Object '{name}' found in directory '{self._root}' is neither a file nor a directory.")
