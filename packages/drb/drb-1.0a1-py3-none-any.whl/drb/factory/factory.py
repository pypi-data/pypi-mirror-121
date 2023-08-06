from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Union, Any
from ..node import DrbNode
from ..utils.logical_node import DrbLogicalNode


class DrbFactoryCategory(Enum):
    RESOLVER = auto()
    SECURITY = auto()
    PROTOCOL = auto()
    CONTAINER = auto()
    FORMATTING = auto()
    UNKNOWN = auto()

    def get_allowed_min_sub_category(self):
        if self == DrbFactoryCategory.SECURITY:
            return DrbFactoryCategory.PROTOCOL
        if self == DrbFactoryCategory.PROTOCOL:
            return DrbFactoryCategory.CONTAINER
        if self == DrbFactoryCategory.CONTAINER:
            return DrbFactoryCategory.CONTAINER
        if self == DrbFactoryCategory.FORMATTING:
            return DrbFactoryCategory.FORMATTING


class DrbFactory(ABC):
    """
    The Factory class defines the abstract class to be implemented in order to
    build drb nodes according to their physical form.
    The factory shall be aware of the implementations available to build nodes
    and build a relation between the physical data and its virtual node
    representation.
    """
    @abstractmethod
    def valid(self, uri: str) -> bool:
        """ Checks the given uri is supported by this factory implementation.
        :param uri: the uri to be checked
        :return: true if this factory is applicable, false otherwise.
        """
        raise NotImplementedError("Call impl method")

    @abstractmethod
    def _create(self, node: DrbNode) -> DrbNode:
        """ Build a DrbNode thanks to this factory implementation.
        :param : The DrbNode of the physical data.
        :type node: DrbNode
        :return: a drb node representing the passed node
        :rtype: DrbNode
        :raises:
            DrbFactoryException: if the factory cannot build the node
        """
        raise NotImplementedError("Call impl method")

    def create(self, source: Union[DrbNode, str, Any]) -> DrbNode:
        """ Build a DrbNode thanks to this factory implementation.
        :param source: the URI or the DrbNode of the physical data.
        :type source: str, DrbNode
        :return: a drb node representing the passed source
        :rtype: DrbNode
        :raises:
            DrbFactoryException: if the given source is not valid
        """
        if isinstance(source, DrbNode):
            return self._create(source)
        else:
            return self._create(DrbLogicalNode(source))

    @property
    @abstractmethod
    def category(self) -> DrbFactoryCategory:
        raise NotImplementedError("Call impl method")
