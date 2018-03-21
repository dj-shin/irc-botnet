import importlib
import asyncio
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
        importlib.reload(self.handlerModule)
        self.handler = self.handlerModule.export_handler(self.handler.transport, self.loop, self.settings)
