import importlib
import sys
import inspect
import logging
from typing import Dict, List

from .. import DrbNode

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points
from importlib.metadata import EntryPoint

from .factory import DrbFactory, DrbFactoryCategory
from ..exceptions import DrbFactoryException

logger = logging.getLogger('DrbFactoryResolver')


class DrbFactoryResolver(DrbFactory):
    """ The factory resolver

    The factory resolver aims to parametrize the selection of the factory
    able to resolves the nodes according to its physical input.
    """

    def valid(self, uri: str) -> bool:
        factories = self.resolve(uri)
        if factories is not None:
            return factories.valid(uri)

    def _create(self, node: DrbNode) -> DrbNode:
        return self.resolve(node.path.path).create(node)

    drb_plugin_section = 'drb.impl'

    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.RESOLVER

    __instance = None
    __factories: Dict[str, DrbFactory] = {}

    @classmethod
    def __find_factory(cls, entry: EntryPoint) -> DrbFactory:
        """
        Retrieves the factory node defined in the given entry point.
        :param entry: plugin entry point
        :type entry: EntryPoint plugin entry point
        :returns: the specific implemented factory
        :rtype: DrbFactory
        :raises:
            * DrbFactoryException If no DrbFactory is found in the entry point.
        """
        try:
            module = importlib.import_module(entry.value)
        except ModuleNotFoundError:
            raise DrbFactoryException(f'Module not found: {entry.value}')

        for name, obj in inspect.getmembers(module):
            if obj != DrbFactory and inspect.isclass(obj) \
                    and issubclass(obj, DrbFactory):
                return obj()
        raise DrbFactoryException(
            f'No DrbFactory found in plugin: {entry.name} -- {entry.value}')

    @classmethod
    def __load_drb_implementations(cls) -> Dict[str, DrbFactory]:
        """
        Loads all DRB plugin defined in the current environment
        :returns: A dict mapping factory names as key to the corresponding
            factory
        :rtype: dict
        """
        impls = {}
        plugins = entry_points(group=cls.drb_plugin_section)

        if not plugins:
            logger.warning('No DRB plugin found')
            return impls

        for name in plugins.names:
            if name not in impls.keys():
                try:
                    factory = DrbFactoryResolver.__find_factory(plugins[name])
                    impls[name] = factory
                except DrbFactoryResolver:
                    message = f'Invalid DRB plugin: {name}'
                    logger.error(message)
                    raise DrbFactoryException(message)
            else:
                logger.warning(f'DRB plugin already loaded: {name}')

        return impls

    def __init__(self):
        if DrbFactoryResolver.__instance is None:
            self.factories = DrbFactoryResolver.__load_drb_implementations()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DrbFactoryResolver, cls).__new__(cls)
            cls.__factories = cls.__load_drb_implementations()
        return cls.__instance

    @classmethod
    def _resolve_all_factories(cls, uri: str, factories: Dict[str, DrbFactory],
                               cat: DrbFactoryCategory = None)\
            -> List[DrbFactory]:
        """Resolves the factory related to the passed uri.

        :param uri: the URI to be resolved
        :param cat: the cat accepted
        : param factories
        :returns: the implemented factory
        :rtype: DrbFactory
        :raises:
            * DrbFactoryException when no factory matches this uri.
        """
        factory_found = []
        for factory in factories.values():
            if (cat is None or factory.category.value >= cat.value) and \
                    factory.valid(uri):

                factory_found.append(factory)
        factory_found.sort(key=lambda f_to_comp: f_to_comp.category.value)
        return factory_found

    @classmethod
    def resolve_all_factories(cls, uri: str, cat: DrbFactoryCategory = None) \
            -> List[DrbFactory]:
        return cls._resolve_all_factories(uri, cls.__factories, cat)

    @classmethod
    def resolve(cls, uri: str, cat: DrbFactoryCategory = None) -> DrbFactory:
        """Resolves the factory related to the passed uri.

        :param uri: the URI to be resolved
        :param cat: the cat accepted
        :returns: the implemented factory
        :rtype: DrbFactory
        :raises:
            * DrbFactoryException when no factory matches this uri.
        """
        factories = cls._resolve_all_factories(uri, cls.__factories, cat)
        if len(factories) > 0:
            return factories[0]
        return None

    @classmethod
    def resolve_all(cls, uri: str,
                    min_category_accepted: DrbFactoryCategory = None)\
            -> DrbNode:
        """Resolves the factory related to the passed uri.

        :param uri: the URI to be resolved
        :param min_category_accepted: the cat accepted
        :returns: the implemented factory
        :rtype: DrbFactory
        :raises:
            * DrbFactoryException when no factory matches this uri.
        """
        factories = cls.resolve_all_factories(uri, min_category_accepted)
        node = None
        for factory in factories:
            node = factory.create(uri)
            cls.resolve_children(node, factory.category.
                                 get_allowed_min_sub_category())
            uri = node

        return node

    @classmethod
    def resolve_children(cls, node: DrbNode,
                         min_category_accepted: DrbFactoryCategory = None):
        """Resolves the factory related to the passed uri.

        :param node: the URI to be resolved
        :param min_category_accepted
        :returns: the implemented factory
        :rtype: DrbFactory
        :raises:
            * DrbFactoryException when no factory matches this uri.
        """

        for idx, child in enumerate(node.children):
            # Here we consider that if we have found a implementation
            # with children
            # this node will be no more resolve ...
            if child.has_child():
                cls.resolve_children(child, min_category_accepted)
            else:
                factories = cls.resolve_all_factories(child.name,
                                                      min_category_accepted)
                child_impl = None
                for factory in factories:
                    child_impl = factory.create(child)
                    cls.resolve_children(child_impl, factory.category.
                                         get_allowed_min_sub_category())
                    child = child_impl
                if child_impl is not None:
                    node.replace_child(idx, child_impl)

    @classmethod
    def get_factory(cls, name) -> DrbFactory:
        if name in cls.__factories.keys():
            return cls.__factories[name]
        raise DrbFactoryException(f'Factory not found: {name}')
