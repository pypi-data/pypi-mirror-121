#!/bin/false
# -*- coding: utf-8 -*-

""" Object-oriented filesystem helper classes. """


# ------------------------------------------------------------------------------------------------------------------------
# Import and pathing setup
# ------------------------------------------------------------------------------------------------------------------------
import pathlib
from typing import Any, Callable, Dict, Generator, Iterable, Optional, Pattern, Union

from ptutils.io import get_loader, get_saver, load_txt, save_txt
from ptutils.globbing import get_subdirs, get_subfiles
from ptutils.text import strip_line_ending
from ptutils.undefined import UNDEFINED, is_defined


# ------------------------------------------------------------------------------------------------------------------------
# Typehint helpers
# ------------------------------------------------------------------------------------------------------------------------
""" Typehint for things which are like a filesystem path. """
PathLike = Union[str, pathlib.Path, 'Path', 'File', 'Folder']

""" Typehint for things which are like a list of filesystem paths. """
PathList = Iterable[PathLike]


# ------------------------------------------------------------------------------------------------------------------------
# Class: Path
# ------------------------------------------------------------------------------------------------------------------------
class Path(pathlib.Path):
    """ A filesystem path. """

    def __init__(self, path: PathLike):
        """
        Create a new filesystem path object.

        Parameters
        ----------
        path : PathLike
            The filesystem path. May be a `Path`, a `pathlib.Path`, a string, or any type deriving from `Path`.
        """
        super().__init__(path)

    # --------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def path_of(path: PathLike) -> 'Path':
        """
        Given a `PathLike` object, coerce it into being a `Path`.

        Returns
        -------
        Path
            A path object referencing the same path as `path`
        """
        return Path(path)

    # --------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def names_of(paths: PathList) -> Generator[str, None, None]:
        """
        Given a list of path objects, return a list of the filename portion of each path.

        Parameters
        ----------
        paths : PathList
            An iterable of `PathLike` objects. To determine filename, these will be coerced
            into `Path` objects before retrieving the filename portion of the path.

        Yields
        ------
        str
            The filename portion of each path provided in `paths`
        """
        for path in paths:
            yield Path.path_of(path).name

    # --------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def relative_paths_to(paths: PathList, reference: PathLike) -> Generator[str, None, None]:
        """
        Given a list of paths and a reference path, compute and return a list of the relative paths.

        Parameters
        ----------
        paths : PathList
            An iterable of `PathLike` objects. To relative path filename, these will be coerced
            into `Path` objects before retrieving the relative path with respect to `reference`.
        reference: PathLike
            A path from which to compute the relative paths of each path in `paths`. this will be
            coerced to a `Path` object before use.

        Yields
        ------
        str
            The filename portion of each path provided in `paths`
        """
        reference = Path.path_of(reference)
        for path in paths:
            yield pathlib.Path(path).relative_to(reference)


# =======================================================================================================================
# Class: File
# =======================================================================================================================
class File(Path):
    """ Class to simplify common file operations. """

    # --------------------------------------------------------------------------------------------------------------------
    def __init__(self, path: PathLike):
        """
        Create a new File path object.

        Parameters
        ----------
        path : PathLike
            The filesystem path of a file. This file may or may not exist.
        """
        super().__init__(path)
        self._loader  = None
        self._saver   = None

    # --------------------------------------------------------------------------------------------------------------------
    def exists(self) -> bool:
        """
        Test whether this path exists and refers to a file.

        Returns
        -------
        bool
            True if the path refers to an existing file.
        """
        return super().exists() and self.is_file()

    # --------------------------------------------------------------------------------------------------------------------
    def initialize_content(self, content: Any = UNDEFINED) -> None:
        """
        Initialize a file's contents by setting the content property if the file doesn't already exist.

        Parameters
        ----------
        content : Any, optional
            [description], by default UNDEFINED
        """
        if is_defined(content):
            if not self.exists():
                self.content = content

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def loader(self) -> Callable[[PathLike], Any]:
        """
        Get the most appropriate loader for this path based on the filename's extension.

        Returns
        -------
        Callable[[PathLike], Any]
            A function which loads the content of the file.

        """
        if self._loader is None:
            self._loader = get_loader(
                filename = str(self),
                default  = load_txt
            )
        return self._loader

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def saver(self) -> Callable[[PathLike, Any], None]:
        """
        Get the most appropriate saver for this path based on the filename's extension.

        Returns
        -------
        Callable[[PathLike, Any], None]
            A function which saves an object to the file in whatever format is most appropriate.

        """
        if self._saver is None:
            self._saver = get_saver(
                filename = str(self),
                default  = save_txt
            )
        return self._saver

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def content(self) -> Any:
        """
        Load the file's contents using the loader determined when the `File` object was created.

        Returns
        -------
        Any
            The loaded/decoded file content. The structure and format is determined by the
        """
        return self.loader(self)

    # --------------------------------------------------------------------------------------------------------------------
    @content.setter
    def content(self, value: Any) -> None:
        """
        Set the file's content by invoking the appropriate saver.

        Parameters
        ----------
        value : Any
            The value to encode and save to the file.
        """
        self.saver(self, value)

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def lines(self) -> Generator[str, None, None]:
        """
        Iterator over the text lines in a file.

        Yields
        ------
        str
            A line of text from the file.

        Notes
        -----
            This property bypasses the determined loader and instead directly
            reads the file as text. If used with binary files, undefined behaviour may result.
        """
        with open(self, 'r') as filp:
            for line in filp.readlines():
                yield strip_line_ending( line )


# =======================================================================================================================
# Class: Folder
# =======================================================================================================================
class Folder(Path):
    """ Class to simplify common folder operations. """

    # --------------------------------------------------------------------------------------------------------------------
    def exists(self) -> bool:
        """
        Test whether this path exists and refers to a folder.

        Returns
        -------
        bool
            True if the path refers to an existing folder.
        """
        return super().exists() and self.is_dir()

    # --------------------------------------------------------------------------------------------------------------------
    def search_subdirectories(
        self,
        pattern:   Optional[Pattern] = None,
        recursive: bool    = False
    ) -> Generator['Folder', None, None]:
        """
        Search for subdirectories of this folder, optionally recursive, optionally
        matching a regular expression.

        Parameters
        ----------
        pattern : Pattern, optional
            A regular expression to match against folder basenames, by default
            None. When omitted, every folder in the search folder will be returned.
        recursive : bool, optional
            When True, search recursively into all subfolders of the search
            folder, by default False.

        Yields
        -------
        Folder
            Any folders matching the constraints specified.
        """
        for fullpath in get_subdirs(self, pattern=pattern, recursive=recursive):
            yield Folder(fullpath)

    # --------------------------------------------------------------------------------------------------------------------
    def search_files(
        self,
        pattern:   Pattern = None,
        recursive: bool    = False
    ) -> Generator['File', None, None]:
        """
        Search for files within this folder, optionally recursive, optionally
        matching a regular expression.

        Parameters
        ----------
        pattern : Pattern, optional
            A regular expression to match against file basenames, by default
            None. When omitted, every files in the search folder will be returned.
        recursive : bool, optional
            When True, search recursively into all subfolders of the search
            folder, by default False.

        Yields
        -------
        Folder
            Any files matching the constraints specified.
        """
        for fullpath in get_subfiles(self, pattern=pattern, recursive=recursive):
            yield File(fullpath)

    # --------------------------------------------------------------------------------------------------------------------
    def child(self, name: PathLike) -> Path:
        """
        Return a a child path of this folder created by concatenating the provided
        `name` with this folder's path.

        Parameters
        ----------
        name : PathLike
            A name or relative path of the child.

        Returns
        -------
        Path
            A new `Path` object referring to the child path.
        """
        return Path(self / Path.path_of(name))

    # --------------------------------------------------------------------------------------------------------------------
    def child_file(self, name: PathLike) -> 'File':
        """
        Return a a child file of this folder created by concatenating the provided
        `name` with this folder's path.

        Parameters
        ----------
        name : PathLike
            A name or relative path of the child.

        Returns
        -------
        File
            A new `File` object referring to the child path.
        """
        return File(self / Path.path_of(name))

    # --------------------------------------------------------------------------------------------------------------------
    def child_folder(self, name: PathLike) -> 'Folder':
        """
        Return a a child folder of this folder created by concatenating the provided
        `name` with this folder's path.

        Parameters
        ----------
        name : PathLike
            A name or relative path of the child.

        Returns
        -------
        Folder
            A new `Folder` object referring to the child path.
        """
        return Folder(self / Path.path_of(name))

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def subdirectories(self) -> Generator['Folder', None, None]:
        """
        An iterator over this folder's subdirectories.

        Returns
        -------
        Folder
            Any child folder.
        """
        return self.search_subdirectories(self)

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def files(self) -> PathList:
        """
        An iterator over this folder's files.

        Returns
        -------
        Folder
            Any child file.
        """
        return self.search_files(self)


# =======================================================================================================================
# Class: FolderSet
# =======================================================================================================================
class FolderSet:
    """
    A convenience class to allow attribute/index-style traversal of folder structures.
    """

    def __init__(self, root: PathLike, structure: Optional[Dict[str, Any]] = None):
        """
        Create a new folder set.

        Parameters
        ----------
        root: PathLike
            The path to the folder.
        structure: Optional[Dict[str, Any]], optional
            A hierarchical structure used to limit traversal, by default None
        """
        self._root      = Folder(root)
        self._structure = structure
        self._cache     = dict()

    # --------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, name: PathLike) -> Union['FolderSet', 'File']:
        """
        Convenience method to allow using division operator to access child objects.

        Parameters
        ----------
        name: PathLike
            The relative path to the child.

        Returns
        -------
        Union['FolderSet', 'File']
            Either a file or folder set object depending on what the child path refers to.
        """
        return self[name]

    # --------------------------------------------------------------------------------------------------------------------
    @property
    def folder(self) -> Folder:
        """
        The root folder object of this folder set.

        Returns
        -------
        Folder
            The `Folder` referring to our root path.
        """
        return self._root

    # --------------------------------------------------------------------------------------------------------------------
    def __getattr__(self, name: str) -> Union['FolderSet', 'File']:
        """
        Access a child file or folder with attribute-style access of this folder object.

        Returns
        -------
        Union['FolderSet', 'File']
            Either a file or folder set object depending on what the child path refers to.

        Raises
        ------
        AttributeError
            When no such child file or folder exists.
        """
        try:
            return self[name]
        except Exception as e:
            raise AttributeError(f"Object of type {type(self)} has no '{name}' attribute.") from e

    # --------------------------------------------------------------------------------------------------------------------
    def __getitem__(self, name: str) -> Union['FolderSet', 'File']:
        """
        Access a child file or folder with index-style access of this folder object.

        Returns
        -------
        Union['FolderSet', 'File']
            Either a file or folder set object depending on what the child path refers to.

        Raises
        ------
        KeyError
            When no such child file or folder exists.
        """
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
