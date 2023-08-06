import os
import unittest
from drb.path import parse_path, ParsedPath, UnparsedPath


class TestPath(unittest.TestCase):
    def test_parse_path_from_url_string(self):
        uris = [
            {
                'url': 'file:///my/path/to/my_file/',
                'type': ParsedPath,
                'path': "/my/path/to/my_file/",
                'scheme': 'file',
                'archive': None,
                'is_local': True,
                'is_remote': False
            },
            {
                'url': '/my/path/to/my_file/',
                'type': ParsedPath,
                'path': "/my/path/to/my_file/",
                'scheme': None,
                'archive': None,
                'is_local': True,
                'is_remote': False
            },
            {
                'url': 'http://avp.wikia.com/wiki/ht_file',
                'type': ParsedPath,
                'path': "avp.wikia.com/wiki/ht_file",
                'scheme': 'http',
                'archive': None,
                'is_local': False,
                'is_remote': True
            },
            {
                'url': 'http://avp.wikia.com/wiki/ht_file?q=*',
                'type': ParsedPath,
                'path': "avp.wikia.com/wiki/ht_file?q=*",
                'scheme': 'http',
                'archive': None,
                'is_local': False,
                'is_remote': True
            },
            {
                'url': 'ftp://ftp.fe.fr/ms/fp.cs.org/7.2.15/ft_file',
                'type': ParsedPath,
                'path': "ftp.fe.fr/ms/fp.cs.org/7.2.15/ft_file",
                'scheme': 'ftp',
                'archive': None,
                'is_local': False,
                'is_remote': True
            },
            {
                'url': 'mailto:billg@microsoft.com',
                'type': ParsedPath,
                'path': "billg@microsoft.com",
                'scheme': 'mailto',
                'archive': None,
                'is_local': True,
                'is_remote': False
            }]

        for uri in uris:
            url = uri['url']
            path_name = uri['path']
            path = parse_path(url)
            self.assertIsInstance(path, uri['type'])
            self.assertEqual(path.path, path_name,
                             msg=f"Wrong path for URI={url}")
            self.assertEqual(path.name, url,
                             msg=f"Wrong name for URI={url}")
            if isinstance(path, ParsedPath):
                self.assertEqual(path.scheme, uri['scheme'],
                                 msg=f"Wrong scheme for URI={url}")
                self.assertEqual(path.archive, uri['archive'],
                                 msg=f"Wrong archive for URI={url}")
                self.assertEqual(path.is_local, uri['is_local'],
                                 msg=f"Wrong archive for URI={url}")
                self.assertEqual(path.is_remote, uri['is_remote'],
                                 msg=f"Wrong archive for URI={url}")

    def test_parse_path_from_vfs_string(self):
        vfss = [
            {
                'url': 'file+zip:///my/path/to/my_file/file.zip',
                'type': ParsedPath,
                'path': "/my/path/to/my_file/file.zip",
                'scheme': 'file+zip',
                'archive': None,
                'is_local': True
            },
            {
                'url': 'zip+https://avp.wikia.com/wiki/ht_file/file.zip',
                'type': ParsedPath,
                'path': "avp.wikia.com/wiki/ht_file/file.zip",
                'scheme': 'zip+https',
                'archive': None,
                'is_local': False
            },
            {
                'url': 'https+zip://avp.wikia.com/wiki/ht_file/file.zip',
                'type': ParsedPath,
                'path': "avp.wikia.com/wiki/ht_file/file.zip",
                'scheme': 'https+zip',
                'archive': None,
                'is_local': True
            },
            {
                'url': 'zip+https://avp.wikia.com/wiki/ht_file/file.zip!'
                       '/content/of/zip',
                'type': ParsedPath,
                'path': "/content/of/zip",
                'scheme': 'zip+https',
                'archive': 'avp.wikia.com/wiki/ht_file/file.zip',
                'is_local': False
            },
        ]

        for uri in vfss:
            url = uri['url']
            path_name = uri['path']
            path = parse_path(url)
            self.assertIsInstance(path, uri['type'])
            if isinstance(path, ParsedPath):
                self.assertEqual(path.name, url,
                                 msg=f"Wrong name for URI={url}")
                self.assertEqual(path.path, path_name,
                                 msg=f"Wrong path for URI={url}")
                self.assertEqual(path.scheme, uri['scheme'],
                                 msg=f"Wrong scheme for URI={url}")
                self.assertEqual(path.archive, uri['archive'],
                                 msg=f"Wrong archive for URI={url}")
                self.assertEqual(path.is_local, uri['is_local'],
                                 msg=f"Wrong archive for URI={url}")
            elif isinstance(path, UnparsedPath):
                self.assertEqual(path.name, url,
                                 msg=f"Wrong name for URI={url}")
                self.assertEqual(path.path, path_name,
                                 msg=f"Wrong path for URI={url}")
            else:
                self.fail(f"Wrong type {type(path).__name__}")

    def test_parse_path_from_path(self):
        my_path = ParsedPath(path='/path/value',
                             archive='www.gael.fr/archive/path.zip',
                             scheme='http')
        parsed_path = parse_path(my_path)
        self.assertEqual(my_path, parsed_path)

    def test_parse_path_from_pathlib(self):
        import pathlib
        cwd = os.getcwd()
        path = pathlib.Path(cwd)
        parsed_path = parse_path(path)
        self.assertEqual(parsed_path.name, cwd)

    def test_path_filename(self):
        _pathes = [
            {
                'path': '/path/to/filename',
                'filename': 'filename'
            },
            {
                'path': '/path/to/filename/',
                'filename': ''
            },
            {
                'path': 'file:/path/to/filename',
                'filename': 'filename'
            },
            {
                'path': 's3+zip:/path/to/filename',
                'filename': 'filename'
            },
            {
                'path': 'https:/path/to/filename?query=*&row=5',
                'filename': 'filename'
            },
            {
                'path': 'https:/path/to/filename/?query=*&row=5',
                'filename': ''
            },
            {
                'path': 'https:/path/to/data.zip!/filename?query=*&row=5',
                'filename': 'filename'
            },
        ]
        for p in _pathes:
            pp = parse_path(p['path'])
            self.assertEqual(pp.filename, p['filename'])
