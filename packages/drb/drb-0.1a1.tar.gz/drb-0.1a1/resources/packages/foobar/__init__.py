from typing import Optional, Any, Union, List, Dict, Tuple

from drb.factory.factory import DrbNode, DrbFactory
from drb.path import Path, parse_path


class DrbFoobarNode(DrbNode):
    def __init__(self, name):
        self._name = f'Foobar_{name}'

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        pass

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def children(self) -> List[DrbNode]:
        return []

    @property
    def path(self) -> Optional[Path]:
        return None

    def has_child(self) -> bool:
        pass

    def get_named_child(self, name: str, namespace_uri: str = None,
                        occurrence: int = 0) -> Union[DrbNode, List[DrbNode]]:
        pass

    def get_first_child(self) -> Optional[DrbNode]:
        pass

    def get_last_child(self) -> Optional[DrbNode]:
        pass

    def get_child_at(self, index: int) -> DrbNode:
        pass

    def get_children_count(self) -> int:
        pass

    def insert_child(self, node: DrbNode, index: int) -> None:
        pass

    def append_child(self, node: DrbNode) -> None:
        pass

    def replace_child(self, index: int, new_node: DrbNode) -> None:
        pass

    def remove_child(self, index: int) -> None:
        pass

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        pass

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type) -> Any:
        return None

    def close(self) -> None:
        pass


class DrbFoobarFactory(DrbFactory):
    def valid(self, uri: str) -> bool:
        return uri.startswith('foobar:')

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbFoobarNode(node.path.filename)
