import sys
import unittest
import os
from drb.node import DrbNode
from drb.factory.factory import DrbFactory
from drb.factory.factory_resolver import DrbFactoryResolver
from drb.exceptions import DrbFactoryException
from .utils import DrbTestNode


class DefaultFactory(DrbFactory):
    def valid(self, uri: str) -> bool:
        return True

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbTestNode(f"DefaultNode_{node.name}")


class TestDrbFactory(unittest.TestCase):
    system_path = os.path.join(os.getcwd(), 'resources', 'packages')

    @classmethod
    def setUpClass(cls) -> None:
        sys.path.append(TestDrbFactory.system_path)

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(TestDrbFactory.system_path)

    def test_drb_factory(self):
        resolver = DrbFactoryResolver()

        uri = "foobar:my/path/to/my_file"
        factory = resolver.resolve(uri)
        self.assertEqual("Foobar_my_file", factory.create(uri).name)

        uri = "mem:/my/path/to/my_file/"
        factory = resolver.resolve(uri)
        self.assertEqual(factory.create(uri).name, "Mem_")

    def test_drb_factory_check_uri(self):
        uris = [
            ("file://my/path/to/my_file/", "DefaultNode_"),
            ("/my/path/to/my_file/", "DefaultNode_"),
            ("file://my/path/to/my_file", "DefaultNode_my_file"),
            ("/my/path/to/my_file", "DefaultNode_my_file"),
            ("http://avp.wikia.com/wiki/ht_file", "DefaultNode_ht_file"),
            ("AAA", "DefaultNode_AAA"),
            ("ftp://ftp.fe.fr/ms/fp.cs.org/7.2.15/ft_file",
             "DefaultNode_ft_file")]

        factory = DefaultFactory()
        for uri, expected_name in uris:
            self.assertEqual(factory.create(uri).name, expected_name,
                             f'Uri not supported: {uri}')

    def test_get_factory(self):
        factory = DrbFactoryResolver.get_factory("mem")
        self.assertIsNotNone(factory)
        self.assertFalse(factory.valid("file://foobar"))
        self.assertTrue(factory.valid("mem:///foobar"))
        self.assertTrue(factory.valid("mem:foobar"))
        self.assertEqual(factory.create("mem:foobar").name, "Mem_foobar")

        with self.assertRaises(DrbFactoryException):
            DrbFactoryResolver.get_factory('bar')
