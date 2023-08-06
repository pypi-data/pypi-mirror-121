from typing import Optional, Any, Union, List, Dict, Tuple

from drb.node import DrbNode
from drb.path import Path, parse_path, ParsedPath
from drb.exceptions import DrbException
from drb.events import Event
from pathlib import PurePath


class DrbLogicalNode(DrbNode):
    """Logical Node for Drb
    This node implements a in-memory logical node, It can be used as default
    node for virtual nodes hierarchy. It can also be used as a wrapper of
    the source node, in this case, the source node is clone.
    """
    def __init__(self, source: Union[DrbNode, str, Path, PurePath]):
        self.changed = Event()
        self._wrapped_node = None
        # case of source is an url string
        if isinstance(source, (str, Path, PurePath)):
            self._path = parse_path(source)
            self._name = self._path.filename
            self._namespace_uri = None
            self._value = None
            self._attributes = None
            self._parent = None
            self._children = None
        elif isinstance(source, DrbNode):
            self._wrapped_node = source

    @property
    def name(self) -> str:
        if self._wrapped_node:
            return self._wrapped_node.name
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        if self._wrapped_node:
            return self._wrapped_node.namespace_uri
        return self._namespace_uri

    @property
    def value(self) -> Optional[Any]:
        if self._wrapped_node:
            return self._wrapped_node.value
        return self._value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._wrapped_node:
            return self._wrapped_node.attributes
        return self._attributes

    @property
    def parent(self) -> Optional[DrbNode]:
        if self._wrapped_node:
            return self._wrapped_node.parent
        return self._parent

    @property
    def path(self) -> ParsedPath:
        if self._wrapped_node:
            return self._wrapped_node.path
        return self._path

    @property
    def children(self) -> List[DrbNode]:
        if self._wrapped_node:
            return self._wrapped_node.children
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type) -> Any:
        raise DrbException(
            f"Implementation for {impl.__name__} not supported.")

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        try:
            return self.attributes[(name, namespace_uri)]
        except (IndexError, TypeError, KeyError) as error:
            raise DrbException(f'No attribute {name} found') from error

    def has_child(self) -> bool:
        if not self.children:
            return False
        return len(self.children) > 0

    def get_named_child(self, name: str, namespace_uri: str = None,
                        occurrence: int = None) -> Union[DrbNode,
                                                         List[DrbNode]]:
        try:
            named_children = [x for x in self.children if x.name == name]
            if occurrence is None and len(named_children) > 0:
                # test on len avoid to return a empty list
                return named_children
            elif occurrence > 0:
                # test avoid to get the last element if occurrence is 0..
                return named_children[occurrence-1]
            else:
                raise DrbException(f'Child ({name},{occurrence}) not found')
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child ({name},{occurrence}) not found') \
                from error

    def get_first_child(self) -> Optional[DrbNode]:
        try:
            return self.children[0]
        except (IndexError, TypeError) as error:
            raise DrbException(f'First child not found') from error

    def get_last_child(self) -> Optional[DrbNode]:
        try:
            return self.children[-1]
        except (IndexError, TypeError) as error:
            raise DrbException(f'Last child not found') from error

    def get_child_at(self, index: int) -> DrbNode:
        try:
            return self.children[index]
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child index {index} not found') from error

    def get_children_count(self) -> int:
        if not self.children:
            return 0
        return len(self.children)

    def insert_child(self, index: int, node: DrbNode) -> None:
        if self.children is None:
            self.children = []
        self.children.insert(index, node)

    def append_child(self, node: DrbNode) -> None:
        if self.children is None:
            self.children = []
        self.children.append(node)

    def replace_child(self, index: int, new_node: DrbNode) -> None:
        try:
            old_node = self.children[index]
            self.children.insert(index, new_node)
            self.children.remove(old_node)
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child index {index} not found') from error

    def remove_child(self, index: int) -> None:
        try:
            self.children.remove(self.children[index])
        except (IndexError, TypeError, AttributeError) as error:
            raise DrbException(f'Child index {index} not found') from error

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        raise NotImplementedError

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        raise NotImplementedError

    def close(self) -> None:
        """
        The wrapped not (if any) is not closed here: This class only wraps
        the values of given node. Nothing is to be closed here.
        """
        if self._wrapped_node:
            return self._wrapped_node.close()

    def __str__(self):
        string = '<'
        if self.namespace_uri:
            string = string + f"{self.namespace_uri}:"
        string = string + f"{self.name}"
        if self.attributes:
            for name, namespace in self.attributes.keys():
                string = string + ' "'
                if namespace:
                    string = string + f'{namespace}:'
                string = string + f'{name}"="'
                string = \
                    string + f'{str(self.attributes.get((name, namespace)))}"'
        if self.value:
            string = string + f'>{str(self.value)}</{self.name}>'
        else:
            string = string + '/>'
        return string

    def __repr__(self):
        return self.__str__()

    @attributes.setter
    def attributes(self, value):
        if self._wrapped_node:
            self._wrapped_node.attributes = value
        else:
            self._attributes = value
        self.changed.notify(self, 'attributes', value)

    @children.setter
    def children(self, value):
        if self._wrapped_node:
            self._wrapped_node.children = value
        else:
            self._children = value
        self.changed.notify(self, 'children', value)

    @parent.setter
    def parent(self, value):
        if self._wrapped_node:
            self._wrapped_node.parent = value
        else:
            self._parent = value
        self.changed.notify(self, 'parent', value)

    @name.setter
    def name(self, value):
        if self._wrapped_node:
            self._wrapped_node.name = value
        else:
            self._name = value
        self.changed.notify(self, 'name', value)

    @namespace_uri.setter
    def namespace_uri(self, value):
        if self._wrapped_node:
            self._wrapped_node.namespace_uri = value
        else:
            self._namespace_uri = value
        self.changed.notify(self, 'namespace_uri', value)

    @value.setter
    def value(self, value):
        if self._wrapped_node:
            self._wrapped_node.value = value
        else:
            self._value = value
        self.changed.notify(self, 'value', value)
