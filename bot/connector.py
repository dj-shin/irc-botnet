import asyncio
from bot.message import IRCMessageParser


class IRCProtocol(asyncio.Protocol):
    def __init__(self, loop, settings):
        self.loop = loop
        self.settings = settings
        self.parser = IRCMessageParser()

    def connection_made(self, transport):
        self.transport = transport
        for command in self.settings.initial_commands:
            self.transport.write(command.encode())

    def data_received(self, data):
        self.parser.append(data)
        while self.parser.parsable():
            message = self.parser.parse()
            self.handle_message(message)

    def connection_lost(self, exc):
        print(exc)
        self.loop.stop()

    def handle_message(self, message):
        print(message)
        if message.command == 'PING':
            self.transport.write('PONG :pingis\n'.encode())
