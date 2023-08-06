import os
import pathlib
import unittest
from typing import List

from drb import DrbNode
from drb.utils.logical_node import DrbLogicalNode
from drb.exceptions import DrbException


class TestLogicalNode(unittest.TestCase):
    def test_init(self):
        node = DrbLogicalNode(source="/path/to/data")
        self.assertEqual(node.path.path, "/path/to/data")
        self.assertEqual(node.name, "data")
        node.close()

        node = DrbLogicalNode(source="http://www.gael.fr/path/to/data")
        self.assertEqual(node.path.path, "www.gael.fr/path/to/data")
        self.assertEqual(node.name, "data")
        node.close()

        node = DrbLogicalNode(
            source="http://www.gael.fr/path/to/data.zip!/content/data")
        self.assertEqual(node.path.path, "/content/data")
        self.assertEqual(node.path.archive, "www.gael.fr/path/to/data.zip")
        self.assertEqual(node.name, "data")
        node.close()

        node = DrbLogicalNode(source=pathlib.Path("/path/to/data"))
        self.assertEqual(node.path.name, "/path/to/data")
        self.assertEqual(node.name, "data")
        node.close()

        new_node = DrbLogicalNode(source=node)
        self.assertEqual(new_node.path.name, "/path/to/data")
        self.assertEqual(new_node.name, node.name)
        node.close()

    def test_attributes(self):
        attributes = {
            ('name1', 'namespace1'): 'value1',
            ('name2', 'namespace2'): 'value2',
            ('name3', 'namespace3'): 'value3',
            ('name4', 'namespace4'): 'value4',
        }
        w = DrbLogicalNode(source="/path/to/data")
        node = DrbLogicalNode(w)
        node.attributes = attributes

        self.assertEqual(node.attributes, attributes)

        self.assertEqual(node.get_attribute('name1', 'namespace1'), 'value1')
        self.assertEqual(node.get_attribute('name4', 'namespace4'), 'value4')
        with self.assertRaises(DrbException):
            node.get_attribute('name4', 'namespace5')

        pass

    def test_children_path(self):
        child1 = DrbLogicalNode(source="/path/to/data/child1")
        child2 = DrbLogicalNode(source="/path/to/data/child2")
        child3 = DrbLogicalNode(source="/path/to/data/child3")
        child4 = DrbLogicalNode(source="/path/to/data/child4")

        node = DrbLogicalNode(source="/path/to/data")
        self.assertEqual(node.get_children_count(), 0)

        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('child'), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_first_child(), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_last_child(), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_child_at(2), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.remove_child(2), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.replace_child(2, child1), None)

        self.assertEqual(node.has_child(), False)

        # Shall not raise exception
        node.insert_child(5, child1)
        self.assertEqual(node.get_children_count(), 1)
        node.insert_child(10, child2)
        self.assertEqual(node.get_children_count(), 2)
        node.insert_child(0, child3)
        self.assertEqual(node.get_children_count(), 3)

        node.replace_child(2, child4)
        self.assertEqual(node.get_children_count(), 3)

        node.remove_child(0)
        self.assertEqual(node.get_children_count(), 2)
        node.remove_child(0)
        node.remove_child(0)

        with self.assertRaises(DrbException):
            node.remove_child(0)

        node.children = [child1, child2, child3, child4]

        self.assertEqual(node.get_children_count(), 4)
        self.assertEqual(node.has_child(), True)
        self.assertEqual(node.get_named_child("child1", occurrence=1), child1)
        self.assertEqual(node.get_named_child("child2", occurrence=1), child2)
        self.assertEqual(node.get_named_child("child3", occurrence=1), child3)
        self.assertEqual(node.get_named_child("child4", occurrence=1), child4)
        self.assertEqual(node.get_named_child("child1")[0], child1)

        self.assertEqual(node.get_child_at(0), child1)
        self.assertEqual(node.get_child_at(3), child4)
        self.assertEqual(node.get_child_at(-1), child4)

        self.assertEqual(node.get_first_child(), child1)
        self.assertEqual(node.get_last_child(), child4)

        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('child1',
                                                  occurrence=0), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('childen123',
                                                  occurrence=1), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('childen123'), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_child_at(15), None)

    def test_children_node(self):
        wrapped = DrbLogicalNode(source="/path/to/data/node")
        child1 = DrbLogicalNode(source="/path/to/data/node/child1")
        child2 = DrbLogicalNode(source="/path/to/data/node/child2")

        node = DrbLogicalNode(source=wrapped)

        self.assertEqual(node.get_children_count(), 0)

        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('child1'), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_first_child(), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_last_child(), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_child_at(2), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.remove_child(2), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.replace_child(2, child1), None)

        self.assertEqual(node.has_child(), False)

        self.assertEqual(node.name, "node")
        self.assertEqual(node.namespace_uri, None)
        self.assertEqual(node.value, None)

        # Shall not raise exception
        node.insert_child(5, child1)
        self.assertEqual(node.get_children_count(), 1)

        node.replace_child(0, child1)
        self.assertEqual(node.get_children_count(), 1)

        node.remove_child(0)
        self.assertEqual(node.get_children_count(), 0)
        with self.assertRaises(DrbException):
            node.remove_child(0)

        children = [child1, child2]
        node.children = children

        self.assertEqual(node.children, children)

        self.assertEqual(node.get_children_count(), 2)
        self.assertEqual(node.has_child(), True)
        self.assertEqual(node.get_named_child("child1", occurrence=1), child1)
        self.assertEqual(node.get_named_child("child2", occurrence=1), child2)
        with self.assertRaises(DrbException):
            self.assertEqual(node.
                             get_named_child("child2", occurrence=10), None)

        self.assertEqual(node.get_named_child("child1")[0], child1)

        self.assertEqual(node.get_child_at(0), child1)
        self.assertEqual(node.get_child_at(-1), child2)
        self.assertEqual(node.get_child_at(1), child2)

        with self.assertRaises(DrbException):
            self.assertEqual(node.get_child_at(3), child2)

        self.assertEqual(node.get_first_child(), child1)
        self.assertEqual(node.get_last_child(), child2)

        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('child1',
                                                  occurrence=0), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('childen123',
                                                  occurrence=1), None)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_named_child('childen123'), None)

    def test_str_repr(self):
        child1 = DrbLogicalNode(source="/path/to/data/child1")
        child2 = DrbLogicalNode(source="/path/to/data/child2")
        child3 = DrbLogicalNode(source="/path/to/data/child3")
        node = DrbLogicalNode(source="/path/to/data")

        node.insert_child(5, child1)
        node.insert_child(10, child2)
        node.insert_child(0, child3)

        self.assertEqual(str(node.children),
                         '[<child3/>, <child1/>, <child2/>]')

        attributes = {
            ('name1', 'nsa'): 'value1',
            ('name2', 'nsa'): 'value2',
        }

        child1.attributes = attributes
        child1.namespace_uri = "ns"
        child2.value = "value"
        self.assertEqual(str(node.children),
                         '[<child3/>, <ns:child1 "nsa:name1"="value1" '
                         '"nsa:name2"="value2"/>, <child2>value</child2>]')

    def test_parent(self):
        parent = DrbLogicalNode(source="/path/to/data")
        child = DrbLogicalNode(source="/path/to/data/node/child")
        w = DrbLogicalNode(source="/path/to/data/node")
        node = DrbLogicalNode(w)

        node.parent = parent
        self.assertEqual(node.parent, parent)
        parent.append_child(node)
        node.append_child(child)

        self.assertEqual(parent.get_named_child("node", occurrence=1), node)
        self.assertEqual(node.parent, parent)

    def test_name(self):
        w = DrbLogicalNode(source="/path/to/data/node")
        node = DrbLogicalNode(w)
        self.assertEqual(node.name, 'node')
        node.name = "new_name"
        self.assertEqual(node.name, 'new_name')

    def test_namespace(self):
        w = DrbLogicalNode(source="/path/to/data/node")
        node = DrbLogicalNode(w)
        self.assertEqual(node.namespace_uri, None)
        node.namespace_uri = 'http://www.gael.fr#'
        self.assertEqual(node.namespace_uri, 'http://www.gael.fr#')

    def test_value(self):
        w = DrbLogicalNode(source="/path/to/data/node")
        node = DrbLogicalNode(w)
        self.assertEqual(node.value, None)
        node.value = "value"
        self.assertEqual(node.value, 'value')

    def test_close(self):
        w = DrbLogicalNode(source="/path/to/data/node")
        node = DrbLogicalNode(w)
        node.close()

    def test_impl(self):
        w = DrbLogicalNode(source="/path/to/data/node")
        node = DrbLogicalNode(w)
        self.assertEqual(node.has_impl(str), False)
        with self.assertRaises(DrbException):
            self.assertEqual(node.get_impl(str), None)

    def test_unimplemented(self):
        w = DrbLogicalNode(source="/path/to/data/node")
        node = DrbLogicalNode(w)
        with self.assertRaises(NotImplementedError):
            node.add_attribute("name", "value", "ns")
        with self.assertRaises(NotImplementedError):
            node.remove_attribute("name", "ns")

    def test_append_child_son(self):
        class SonDrbLogicalNode(DrbLogicalNode):
            def __init__(self, path, parent: DrbNode = None):
                DrbLogicalNode.__init__(self, source=path)
                self._parent: DrbNode = parent

            @property
            def children(self) -> List[DrbNode]:
                if self._children is None:
                    self._children = []
                return self._children

        node = SonDrbLogicalNode("/path/to/data/node")
        node_child = DrbLogicalNode(source="/path/to/data/node.child")

        node.append_child(node_child)
        self.assertEqual(node.get_children_count(), 1)

    def test_insert_child_son(self):
        class SonDrbLogicalNode(DrbLogicalNode):
            def __init__(self, path, parent: DrbNode = None):
                DrbLogicalNode.__init__(self, source=path)
                self._parent: DrbNode = parent

            @property
            def children(self) -> List[DrbNode]:
                if self._children is None:
                    self._children = []
                return self._children

        node = SonDrbLogicalNode("/path/to/data/node")
        node_child = DrbLogicalNode(source="/path/to/data/node.child")

        node.insert_child(0, node_child)
        self.assertEqual(node.get_children_count(), 1)
