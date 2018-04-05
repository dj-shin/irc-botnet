import importlib
import asyncio
import inspect
import types
import os
from bot.message import IRCMessageParser


class IRCProtocol(asyncio.Protocol):
    def __init__(self, loop, settings, handlerModule):
        self.loop = loop
        self.settings = settings
        self.parser = IRCMessageParser()
        self.handlerModule = handlerModule

    def connection_made(self, transport):
        self.handler = self.handlerModule.export_handler(transport, self.loop, self.settings)
        for command in self.settings.initial_commands:
            transport.write(command.encode())

    def data_received(self, data):
        self.parser.append(data)
        while self.parser.parsable():
            message = self.parser.parse()
            self.handler.handle(message)

    def connection_lost(self, exc):
        print(exc)
        self.loop.stop()

    def reload_handler(self):
        def _reload(package):
            assert(hasattr(package, '__package__'))
            fn = package.__file__
            fn_dir = os.path.dirname(fn) + os.sep
            print(fn)
            module_visit = {fn}
            del fn

            def reload_recursive_ex(module):
                print('reloading: %s' % module)
                importlib.reload(module)
                for module_child in vars(module).values():
                    if isinstance(module_child, types.ModuleType):
                        fn_child = getattr(module_child, '__file__', None)
                        if (fn_child is not None) and fn_child.startswith(fn_dir):
                            if fn_child not in module_visit:
                                module_visit.add(fn_child)
                                reload_recursive_ex(module_child)
                    elif inspect.isclass(module_child):
                        fn_child = getattr(module_child, '__module__', None)
                        if fn_child is not None:
                            module_child = importlib.import_module(fn_child)
                            fn_child = getattr(module_child, '__file__', None)
                            if fn_child not in module_visit:
                                module_visit.add(fn_child)
                                reload_recursive_ex(module_child)
            return reload_recursive_ex(package)
        _reload(self.handlerModule)
        self.handler = self.handlerModule.export_handler(self.handler.transport, self.loop, self.settings)
