import importlib
import sys
import inspect
import logging
from typing import Dict

from .. import DrbNode

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points
from importlib.metadata import EntryPoint

from .factory import DrbFactory
from ..exceptions import DrbFactoryException

logger = logging.getLogger('DrbFactoryResolver')


class DrbFactoryResolver(DrbFactory):
    """ The factory resolver

    The factory resolver aims to parametrize the selection of the factory
    able to resolves the nodes according to its physical input.
    """

    def valid(self, uri: str) -> bool:
        return self.resolve(uri).valid(uri)

    def _create(self, node: DrbNode) -> DrbNode:
        return self.resolve(node.path.path).create(node)

    drb_plugin_section = 'drb.impl'
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
    def resolve(cls, uri: str) -> DrbFactory:
        """Resolves the factory related to the passed uri.

        :param uri: the URI to be resolved
        :returns: the implemented factory
        :rtype: DrbFactory
        :raises:
            * DrbFactoryException when no factory matches this uri.
        """
        for factory in cls.__factories.values():
            if factory.valid(uri):
                return factory

    @classmethod
    def get_factory(cls, name) -> DrbFactory:
        if name in cls.__factories.keys():
            return cls.__factories[name]
        raise DrbFactoryException(f'Factory not found: {name}')
