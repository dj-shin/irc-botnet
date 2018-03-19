from bot.connector import IRCProtocol
import asyncio


class IRCSetting:
    def __init__(self):
        self.botname = 'test-bot'
        self.botnick = 'test-bot'
        self.initial_commands = [
            'USER ' + (self.botname + ' ') * 3 + ':' + self.botnick + '\n',
            'NICK ' + self.botnick + '\n',
            'JOIN ' + '#maronet' + '\n',
        ]

if __name__ == '__main__':
    host = 'moe.uriirc.org'
    port = '16667'
    loop = asyncio.get_event_loop()
    conn = loop.create_connection(
        lambda: IRCProtocol(loop, IRCSetting()),
        host=host,
        port=port)
    loop.run_until_complete(conn)
    loop.run_forever()
    loop.close()
