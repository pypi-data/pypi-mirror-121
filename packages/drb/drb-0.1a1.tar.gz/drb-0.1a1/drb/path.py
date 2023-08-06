"""Dataset paths, identifiers, and filenames"""
import abc
import pathlib
import re
import sys
from urllib.parse import urlparse
import attr

from .exceptions import DrbPathException

# Supported URI schemes and their mapping to GDAL's VSI suffix.
# TODO: extend for other cloud plaforms.
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

# TODO: extend for other cloud plaforms.
REMOTESCHEMES = set([k for k, v in SCHEMES.items()
                     if v in ('curl', 's3', 'oss', 'gs', 'az',)])


@attr.s(slots=True)
class Path(abc.ABC):
    """Base class for dataset paths"""
    path = attr.ib()

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


@attr.s(slots=True)
class ParsedPath(Path):
    """Result of parsing a dataset URI/Path

    Attributes
    ----------
    path : str
        Parsed path. Includes the hostname and query string in the case
        of a URI.
    archive : str
        Parsed archive path.
    scheme : str
        URI scheme such as "https" or "zip+s3".
    """
    archive = attr.ib()
    scheme = attr.ib()

    @classmethod
    def from_uri(cls, uri):
        parts = urlparse(uri)
        path = parts.path
        scheme = parts.scheme or None

        if parts.query:
            path += "?" + parts.query

        if parts.scheme and parts.netloc:
            path = parts.netloc + path

        parts = path.split('!')
        path = parts.pop() if parts else None
        archive = parts.pop() if parts else None
        return ParsedPath(path, archive, scheme)

    @property
    def name(self) -> str:
        """The parsed path's original URI"""
        slash_slash = ''
        if self.scheme and all(p in SCHEMES for p in self.scheme.split('+')):
            slash_slash = '//'

        if not self.scheme:
            return self.path
        elif self.archive:
            return f"{self.scheme}:{slash_slash}{self.archive}!{self.path}"
        else:
            return f"{self.scheme}:{slash_slash}{self.path}"

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


@attr.s(slots=True)
class UnparsedPath(Path):
    """Encapsulates legacy GDAL filenames

    Attributes
    ----------
    path : str
        The legacy GDAL filename.
    """

    @property
    def name(self):
        """The unparsed path's original path"""
        return self.path


def parse_path(path):
    """Parse a dataset's identifier or path into its parts

    Parameters
    ----------
    path : str or path-like object
        The path to be parsed.

    Returns
    -------
    ParsedPath or UnparsedPath

    Notes
    -----
    When legacy GDAL filenames are encountered, they will be returned
    in a UnparsedPath.

    """
    if isinstance(path, Path):
        return path

    elif pathlib and isinstance(path, pathlib.PurePath):
        return ParsedPath(path.as_posix(), None, None)

    elif isinstance(path, str):
        if sys.platform == "win32" and re.match(r"^[a-zA-Z]:", path):
            if pathlib:
                return ParsedPath(pathlib.Path(path).as_posix(), None, None)
            else:
                return UnparsedPath(path)
        elif path.startswith('/vsi'):
            return UnparsedPath(path)
    else:
        raise DrbPathException("invalid path '{!r}'".format(path))

    return ParsedPath.from_uri(path)
