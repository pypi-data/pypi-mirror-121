"""Dataset paths, identifiers, and filenames"""
import abc
import pathlib
import re
import sys
from urllib.parse import urlparse, uses_netloc

from .exceptions import DrbPathException

# Supported URI schemes.
# TODO: extend for other cloud platforms.
SCHEMES = {
    'ftp': 'curl',
    'gzip': 'gzip',
    'http': 'curl',
    'https': 'curl',
    's3': 's3',
    'tar': 'tar',
    'zip': 'zip',
    'file': 'file',
    'oss': 'oss',
    'gs': 'gs',
    'az': 'az',
}

CURLSCHEMES = set([k for k, v in SCHEMES.items() if v == 'curl'])

# TODO: extend for other cloud platforms.
REMOTESCHEMES = set([k for k, v in SCHEMES.items()
                     if v in ('curl', 's3', 'oss', 'gs', 'az',)])


class Path(abc.ABC):
    """Base class for dataset paths"""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Abstract method not implemented")

    @property
    def filename(self) -> str:
        """
        Computes the filename of this path if any
        :return:
        """
        return self.name.split(":")[-1].split("/")[-1].split("?")[0]


class ParsedPath(Path):
    """Result of parsing a dataset URI/Path

    Attributes
    ----------
    complete_path : str
        Path to parse the other param are ignored if not None
    archive : str
        Parsed path.
    archive : str
        Parsed archive path.
    scheme : str
        URI scheme such as "https" or "zip+s3".
   netloc : str
        netloc such as "localhost or www.toot.dom".
    query : str
        query like such as 'count'
    fragment : str
        arg of query
    """

    def __init__(self, complete_path: str = None,  path: str = None,
                 archive: str = None, scheme: str = None,
                 netloc: str = None, query: str = None,
                 fragment: str = None):

        if complete_path is not None:
            self.original_path = complete_path
            url_with_scheme = urlparse(complete_path)
            self.scheme = url_with_scheme.scheme
            self.path = url_with_scheme.path
            self.netloc = url_with_scheme.netloc
            self.query = url_with_scheme.query
            self.fragment = url_with_scheme.fragment
            parts = self.path.split('!')
            self.path_without_archive = parts.pop() if parts else self.path
            self.archive = parts.pop() if parts else None

        else:
            self.archive = archive
            self.path_without_archive = path
            if self.archive:
                self.path = path + '/' + self.archive
            else:
                self.path = path
            self.original_path = self.path
            self.scheme = scheme
            self.netloc = netloc
            self.query = query
            self.fragment = fragment

    @classmethod
    def _add_scheme_and_netloc_to_url(cls, path, schemes, netloc):
        url_use_netloc = False
        if schemes:
            for scheme in schemes.split('+'):
                if scheme in uses_netloc:
                    url_use_netloc = True
                    break
        url = path
        if netloc or (url_use_netloc and url[:2] != '//'):
            if url and url[:1] != '/':
                url = '/' + url
            url = '//' + (netloc or '') + url
        if schemes:
            url = schemes + ':' + url

        return url

    @classmethod
    def _add_query_to_url(cls, path_to_complete, query, fragment):
        url = path_to_complete
        if query:
            url = url + '?' + query
        if fragment:
            url = url + '#' + fragment
        return url

    def _create_url(self, path_to_complete):

        url = self._add_scheme_and_netloc_to_url(path_to_complete,
                                                 self.scheme, self.netloc)
        url = self._add_query_to_url(url,
                                     self.query,
                                     self.fragment)
        return url

    @property
    def name(self) -> str:
        """The complete parsed path"""
        if not self.scheme:
            return self.path
        else:
            return self._create_url(self.path)

    def uri_with_netloc(self) -> str:
        """The parsed path's with netloc without scheme"""
        url = self.path
        if self.netloc:
            url = self.netloc + url
        url = self._add_query_to_url(url, self.query, self.fragment)
        return url

    @property
    def is_remote(self):
        """Test if the path is a remote, network URI"""
        if not self.scheme:
            return False
        return self.scheme.split("+")[-1] in REMOTESCHEMES

    @property
    def is_local(self):
        """Test if the path is a local URI"""
        if not self.scheme:
            return True
        return self.scheme.split('+')[-1] not in REMOTESCHEMES

    def create_child_path(self, child_name: str):
        child_path = self.path + '/' + child_name

        child = ParsedPath(None, path=child_path,
                           archive=self.archive, scheme=self.scheme,
                           netloc=self.netloc, query=self.query,
                           fragment=self.fragment)
        return child


def parse_path(path):
    """Parse a dataset's identifier or path into its parts

    Parameters
    ----------
    path : str or path-like object
        The path to be parsed.

    Returns
    -------
    ParsedPath or raise exception


    """
    if isinstance(path, Path):
        return path

    elif pathlib and isinstance(path, pathlib.PurePath):
        return ParsedPath(path.as_posix())

    elif isinstance(path, str):
        if sys.platform == "win32" and re.match(r"^[a-zA-Z]:", path):
            if pathlib:
                return ParsedPath(pathlib.Path(path).as_posix())

        return ParsedPath(path)
    else:
        raise DrbPathException("invalid path '{!r}'".format(path))
