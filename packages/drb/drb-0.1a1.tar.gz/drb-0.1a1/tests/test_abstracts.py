import unittest
from typing import Optional, Any, Union, List, Dict, Tuple

from drb import DrbItem, DrbNode
from drb.node_impl import NodeImpl
from drb.path import Path
from drb.factory.factory import DrbFactory


class DrbItemTest(DrbItem):
    @property
    def name(self) -> Optional[str]:
        return super().name

    @property
    def namespace_uri(self) -> Optional[str]:
        return super().namespace_uri

    @property
    def value(self) -> Optional[Any]:
        return super().value


class DrbNodeImplTest(NodeImpl):
    def has_impl(self, impl: type) -> bool:
        return super().has_impl(impl)

    def get_impl(self, impl: type) -> Any:
        return super().get_impl(impl)


class DrbFactoryTest(DrbFactory):
    def valid(self, uri: str) -> bool:
        return super(DrbFactoryTest, self).valid(uri)

    def _create(self, node: Union[DrbNode, str, Any]) -> DrbNode:
        return super(DrbFactoryTest, self)._create(node)


class DrbNodeTest(DrbNode, DrbItemTest, DrbNodeImplTest):
    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return super().attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return super(DrbNodeTest, self).get_attribute(name, namespace_uri)

    @property
    def parent(self) -> Optional[DrbNode]:
        return super(DrbNodeTest, self).parent

    @property
    def path(self) -> Path:
        return super(DrbNodeTest, self).path

    @property
    def children(self) -> List[DrbNode]:
        return super(DrbNodeTest, self).children

    def has_child(self) -> bool:
        return super(DrbNodeTest, self).has_child()

    def get_named_child(self, name: str, namespace_uri: str = None,
                        occurrence: int = 0) -> Union[DrbNode, List[DrbNode]]:
        return super(DrbNodeTest, self).get_named_child(name, namespace_uri,
                                                        occurrence)

    def get_first_child(self) -> Optional[DrbNode]:
        return super(DrbNodeTest, self).get_first_child()

    def get_last_child(self) -> Optional[DrbNode]:
        return super(DrbNodeTest, self).get_last_child()

    def get_child_at(self, index: int) -> DrbNode:
        return super(DrbNodeTest, self).get_child_at(index)

    def get_children_count(self) -> int:
        return super(DrbNodeTest, self).get_children_count()

    def insert_child(self, index: int, node: DrbNode) -> None:
        super(DrbNodeTest, self).insert_child(index, node)

    def append_child(self, node: DrbNode) -> None:
        super(DrbNodeTest, self).append_child(node)

    def replace_child(self, index: int, new_node: DrbNode) -> None:
        super(DrbNodeTest, self).replace_child(index, new_node)

    def remove_child(self, index: int) -> None:
        super(DrbNodeTest, self).remove_child(index)

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        super(DrbNodeTest, self).add_attribute(name, value, namespace_uri)

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        super(DrbNodeTest, self).remove_attribute(name, namespace_uri)

    def close(self) -> None:
        super(DrbNodeTest, self).close()


class TestEvent(unittest.TestCase):
    def test_abstract_drb_item(self):
        item = DrbItemTest()
        with self.assertRaises(NotImplementedError):
            self.assertEqual(item.name, None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(item.namespace_uri, None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(item.value, None)

    def test_abstract_node_impl(self):
        impl = DrbNodeImplTest()
        with self.assertRaises(NotImplementedError):
            self.assertEqual(impl.get_impl(str), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(impl.has_impl(str), None)

    def test_abstract_drb_node(self):
        node = DrbNodeTest()
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.attributes, None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.get_attribute("aa"), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.parent, None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.path, None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.children, None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.has_child(), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.get_named_child("aa"), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.get_first_child(), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.get_last_child(), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.get_child_at(0), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.get_children_count(), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.append_child(DrbNodeTest()), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.insert_child(0, DrbNodeTest()), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.replace_child(0, DrbNodeTest()), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.remove_child(0), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.add_attribute("None", None, None), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.remove_attribute("None", None), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.replace_child(0, DrbNodeTest()), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(node.close(), None)

    def test_abstract_factory(self):
        factory = DrbFactoryTest()
        with self.assertRaises(NotImplementedError):
            self.assertEqual(factory.valid('uri=None'), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(factory.create('uri=None'), None)
        with self.assertRaises(NotImplementedError):
            self.assertEqual(factory.create(DrbNodeTest()), None)
